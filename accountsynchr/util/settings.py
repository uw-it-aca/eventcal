import os
from django.conf import settings


def get_csv_file_path():
    return getattr(settings, 'CSV_FILE_PATH', None)
