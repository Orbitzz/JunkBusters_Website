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


class OmniHQCallsIdentifyThemselvesTests(TestCase):
    """Cloudflare 403s the default Python-urllib User-Agent; every OmniHQ call must send ours
    and go to OMNIHQ_EMBED_URL (https in prod), never a hard-coded http://host:8000."""

    def _capture(self):
        from unittest import mock
        seen = []

        class _Resp:
            status = 200
            def read(self):
                return b'{"success": true, "messages": []}'
            def __enter__(self):
                return self
            def __exit__(self, *a):
                return False

        def fake_urlopen(req, timeout=None):
            seen.append(req)
            return _Resp()
        return seen, mock.patch('urllib.request.urlopen', side_effect=fake_urlopen)

    def test_all_embed_calls_send_named_user_agent_to_configured_url(self):
        from django.test import override_settings
        from django.test.client import RequestFactory
        from website import views
        from website.omnihq_client import USER_AGENT
        seen, patcher = self._capture()
        url = 'https://ohq.example/marketing/api/embed/{endpoint}/'
        with override_settings(OMNIHQ_EMBED_URL=url), patcher:
            views._call_fc('availability', {'month': '2026-11'})
            views._post_to_fc('quote', {'name': 'x'})
            views._call_fc_multipart('chat', {'name': 'x'}, {'attachment': ('a.png', b'123', 'image/png')})
            views.chat_poll(RequestFactory().get('/api/chat/poll/', {'thread_id': '5'}))
        self.assertEqual(len(seen), 4)
        for req in seen:
            self.assertEqual(req.get_header('User-agent'), USER_AGENT)
            self.assertTrue(req.full_url.startswith('https://ohq.example/marketing/api/embed/'), req.full_url)
        self.assertIn('/embed/chat/poll/?', seen[3].full_url)


class ReferralSpamGateTests(TestCase):
    def _post(self, **kw):
        data = {'referrer_first_name': 'Jane', 'referrer_last_name': 'Doe', 'referrer_email': 'jane@example.com',
                'referrer_phone': '6155550142', 'referred_name': 'Bob Smith', 'referred_phone': '6155550199',
                'referred_email': 'bob@example.com'}
        data.update(kw)
        return self.client.post('/referral/', data)

    def test_random_bot_names_never_reach_omnihq(self):
        with mock.patch('website.views.verify_turnstile', return_value=True), \
             mock.patch('website.views._post_to_fc') as fwd:
            r = self._post(referrer_first_name='OZQSOZJzHyxxnfQjqrdfwpq', referred_name='pXJfFSpnKPTdrTNrTBd')
            self.assertEqual(r.status_code, 200)
            fwd.assert_not_called()

    def test_honeypot_and_failed_turnstile_blocked(self):
        with mock.patch('website.views.verify_turnstile', return_value=True), mock.patch('website.views._post_to_fc') as fwd:
            self._post(website_url='http://spam')
            fwd.assert_not_called()
        with mock.patch('website.views.verify_turnstile', return_value=False), mock.patch('website.views._post_to_fc') as fwd:
            self._post()
            fwd.assert_not_called()

    def test_real_referral_forwarded(self):
        with mock.patch('website.views.verify_turnstile', return_value=True), mock.patch('website.views._post_to_fc') as fwd:
            self._post(referrer_first_name='McKenzie', referred_name='DeShawn MacDonald')
            fwd.assert_called_once()
