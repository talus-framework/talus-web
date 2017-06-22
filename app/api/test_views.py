# encoding: utf-8
import os
import tempfile

import django
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.http import HttpResponseServerError
from django.test import RequestFactory

import talus_web.settings
from util.test_util import *


def set_up_django():
    talus_web.settings.MONGO_HOST = os.environ.get('MONGO_TEST_HOST', 'localhost')
    django.setup()


@with_setup(setup=set_up_django, teardown=unstub)
def test_temp_file_upload_checks_if_a_file_was_successfully_uploaded():
    request_factory = RequestFactory()
    req = request_factory.post('upload')
    from api.views import TmpFileUpload
    the_view = TmpFileUpload()
    response = the_view.post(req)
    assert_is_instance(response, HttpResponseServerError)


@with_setup(setup=set_up_django, teardown=unstub)
def test_temp_file_upload_checks_if_a_file_was_successfully_uploaded_2():
    request_factory = RequestFactory()
    req = request_factory.post('upload')
    tmp_file_path = '/tmp/file.txt'
    clean_up_db(tmp_file_path)
    from api.views import TmpFileUpload
    the_view = TmpFileUpload()
    uploaded_file = mock(TemporaryUploadedFile)
    uploaded_file_path = '/tmp/uploaded_file'
    when(uploaded_file).temporary_file_path().thenReturn(uploaded_file_path)
    req.FILES['file'] = uploaded_file
    when(tempfile).mktemp(dir="/tmp").thenReturn(tmp_file_path)
    allow(os).rename(uploaded_file_path, tmp_file_path)
    response = the_view.post(req)
    verify(os).rename(uploaded_file_path, tmp_file_path)
    assert_equal(response.status_code, 200)


@with_setup(setup=set_up_django, teardown=unstub)
def test_amount_of_free_disk_space_can_be_requested():
    from api.views import DiskFree
    the_view = DiskFree()
    num_free_blocks = 123 * 1024
    block_size = 4096
    when(os).statvfs('/tmp').thenReturn(AttrDict(f_bsize=block_size, f_bfree=num_free_blocks))
    response = the_view.get({})
    assert_equal(response.status_code, 200)
    assert_equal(response.data, block_size * num_free_blocks)


def clean_up_db(tmp_file_path):
    from api.models import TmpFile
    prev_temp_files = TmpFile.objects(path=tmp_file_path)
    for prev_temp_file in prev_temp_files:
        prev_temp_file.delete()
