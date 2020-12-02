from django.db import models
import os
from transliterate import slugify
from time import strftime


# Create your models here.

def get_upload_path(folder, filename):
    file_name, file_extension = os.path.splitext(filename)
    return os.path.join('media', folder, strftime("%Y/%m/%d/"), slugify(file_name, 'ru') + file_extension)
