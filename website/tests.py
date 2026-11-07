from unittest import mock

from django.test import TestCase, override_settings

from website.models import BookingRequest


@override_settings(RATELIMIT_ENABLE=False)
class QuoteSavesLongDescriptionTests(TestCase):
    """Sentry JUNKBUSTERS-9: service_type + ' - ' + description went into a
    CharField(200); long descriptions raised DataError and the lead was never
    saved on the site (it still reached OmniHQ and email)."""

    @mock.patch('website.views.verify_turnstile', return_value=True)
    @mock.patch('website.views._post_to_fc')
    @mock.patch('website.views.notify_lead')
    def test_long_description_still_saves(self, _notify, _fc, _ts):
        from website.forms import SERVICE_CHOICES
        long_text = 'Old couch, two mattresses and a broken treadmill in the basement. ' * 8
        r = self.client.post('/quote/', {
            'first_name': 'Pat', 'last_name': 'Lee', 'email': 'pat@example.com', 'phone': '6155550100',
            'service_type': SERVICE_CHOICES[1][0], 'address': ('1428 Maple Ridge Drive, Building C ' * 7)[:240],
            'city': 'Springfield', 'state': 'TN', 'zip_code': '37172', 'description': long_text,
        }, HTTP_CF_CONNECTING_IP='203.0.113.9')
        self.assertIn(r.status_code, (200, 302))
        b = BookingRequest.objects.get(email='pat@example.com')
        self.assertLessEqual(len(b.service_requested), 200)
        self.assertLessEqual(len(b.address), 200)
        self.assertEqual(b.notes, long_text.strip())  # full description kept
