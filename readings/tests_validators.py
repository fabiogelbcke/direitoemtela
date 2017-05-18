from django.test import TestCase
from django.core.exceptions import ValidationError
import os
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from .forms import ReadingForm

class ReadingValidatorTestCase(TestCase):

    def test_reading_validator(self):
        valid_reading = open(os.path.join(
            settings.PROJECT_ROOT, 'testfiles/reading.pdf'), 'rb')
        data = {}
        file_data = {
            'name': 'reading',
            'reading_file': SimpleUploadedFile(valid_reading.name,
                                           valid_reading.read()),
        }
        valid = ReadingForm(data, file_data)
        print valid.errors
        self.assertEqual(valid.is_valid(), True)

    def test_reading_validator_wrong_extension(self):
        wrong_extension = open(os.path.join(
            settings.PROJECT_ROOT, 'testfiles/reading.png'), "rb")
        data = {}
        file_data = {
            'name': 'reading',
            'reading_file': SimpleUploadedFile(wrong_extension.name,
                                           wrong_extension.read()),
        }
        invalid = ReadingForm(data, file_data)
        self.assertEqual(invalid.is_valid(), False)

    def test_reading_validator_wrong_format(self):
        wrong_format = open(os.path.join(
            settings.PROJECT_ROOT, 'testfiles/reading_renamed.pdf'), 'rb')
        data = {}
        file_data = {
            'name': 'reading',
            'reading_file': SimpleUploadedFile(wrong_format.name,
                                           wrong_format.read(),
                                           content_type='application/pdf'),
        }
        invalid = ReadingForm(data, file_data)
        self.assertEqual(invalid.is_valid(), False)
