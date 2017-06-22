# encoding: utf-8
import os

from django.core.files.uploadhandler import StopUpload

from talus_web.file_upload import SpaceEnsuringUploadHandler
from util.test_util import *


@with_setup(teardown=unstub)
def test_upload_handler_allows_upload_when_there_is_enough_disk_space():
    the_file, upload_handler = set_up_file_upload_handler(num_free_blocks=1024 * 1024 * 1024)
    raw_data = ["raw", 'data']
    upload_handler.receive_data_chunk(raw_data=raw_data, start=1337)
    verify(the_file).write(raw_data)


@with_setup(teardown=unstub)
def test_upload_handler_does_not_allow_disk_to_be_filled():
    _, upload_handler = set_up_file_upload_handler(num_free_blocks=123)
    assert_that(calling(upload_handler.receive_data_chunk).with_args(raw_data=["raw", 'data'], start=1337), raises(StopUpload))


def set_up_file_upload_handler(num_free_blocks):
    upload_handler = SpaceEnsuringUploadHandler()
    the_file = mock()
    upload_handler.file = the_file
    uploaded_file_no = 555
    when(the_file).fileno().thenReturn(uploaded_file_no)
    when(os).fstatvfs(uploaded_file_no).thenReturn(AttrDict(f_bsize=4096, f_bfree=num_free_blocks))
    return the_file, upload_handler
