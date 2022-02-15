from django.core import mail
from django.test import TestCase


class EmailTest(TestCase):
    def test_send_email(self):
        mail.send_mail(
            subject='Subject here',
            message='Here is the message.',
            from_email='info@ituscheduler.com',
            recipient_list=['doruk@ituscheduler.com'],
            fail_silently=False,
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Subject here')
