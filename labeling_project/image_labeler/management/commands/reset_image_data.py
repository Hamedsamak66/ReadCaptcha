# your_app_name/management/commands/reset_image_data.py

from django.core.management.base import BaseCommand
from django.db import connection
from image_labeler.models import ImageData

class Command(BaseCommand):
    help = 'Deletes all records from ImageData table and resets the auto-increment id to 1'

    def handle(self, *args, **kwargs):
        ImageData.objects.all().delete()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='image_labeler_imagedata';")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='image_labeler';")
        # اگر در PostgreSQL هستید این خط را جایگزین کنید
        # cursor.execute("ALTER SEQUENCE your_app_name_imagedata_id_seq RESTART WITH 1;")
        self.stdout.write('تمام رکوردها پاک شدند و شمارنده خودکار بازنشانی شد.')
