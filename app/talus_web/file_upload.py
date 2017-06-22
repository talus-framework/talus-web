# encoding: utf-8

import logging
import os

from django.core.files.uploadhandler import TemporaryFileUploadHandler, StopUpload

log = logging.getLogger(__file__)

MINIMUM_FREE_SPACE = 100 * 1024 * 1024


def get_free_space(f):
    stats = os.fstatvfs(f)
    return stats.f_bsize * stats.f_bfree


def human_size(num):
    for unit in ['', 'k', 'm', 'g']:
        if abs(num) < 1024.0:
            return "%.2f%sb" % (num, unit)
        num /= 1024.0
    return "%.2ftb" % num


class SpaceEnsuringUploadHandler(TemporaryFileUploadHandler):
    def receive_data_chunk(self, raw_data, start):
        free_space_left = get_free_space(self.file.fileno())
        if free_space_left < MINIMUM_FREE_SPACE:
            log.error('not enough free space left. %s < %s', human_size(free_space_left), human_size(MINIMUM_FREE_SPACE))
            raise StopUpload(connection_reset=True)
        super(SpaceEnsuringUploadHandler, self).receive_data_chunk(raw_data, start)
