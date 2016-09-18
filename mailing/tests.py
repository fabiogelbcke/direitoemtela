from django.test import TestCase
from .models import MailingEmail
# Create your tests here.

class AddEmailTestCase(TestCase):

    def test_adds_email(self):
        r = self.client.post('/addtolist', {'email': 'fabio@det.com'})
        self.assertEqual(r.status_code, 200)
        email_count = MailingEmail.objects.filter(email='fabio@det.com').count()
        self.assertEqual(email_count, 1)

    def test_doesnt_add_no_email(self):
        r = self.client.post('/addtolist')
        self.assertEqual(r.status_code, 400)
        self.assertEqual(MailingEmail.objects.all().count(), 0)

    def test_doesnt_add_invalid_email(self):
        r = self.client.post('/addtolist', {'email': 'fafafafa@oi'})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(MailingEmail.objects.all().count(), 0)
