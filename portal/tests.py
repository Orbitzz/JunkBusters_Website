"""Smoke tests for the customer portal.

Minimal on purpose — status codes only. Their job is to catch bugs like the
NameError in dashboard() that hid for three months (unresolved OmniHQ-helper
rename from commit 3419358, May 2026) — a single GET would have failed the
build.
"""
from unittest import mock

from django.contrib.auth.models import User
from django.test import TestCase

from portal.models import CustomerProfile


class PortalSmokeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='smoke@example.com',
            email='smoke@example.com',
            password='smoke-pw-1234',
            first_name='Smoke',
            last_name='Test',
            is_active=True,
        )
        CustomerProfile.objects.create(user=self.user, phone='555-0100')

    def test_dashboard_returns_200_for_logged_in_user(self):
        """/portal/dashboard/ must render even when OmniHQ is unreachable."""
        self.client.force_login(self.user)
        with mock.patch('portal.views._call_ohq', return_value=None):
            resp = self.client.get('/portal/dashboard/')
        self.assertEqual(resp.status_code, 200)

    def test_referral_submit_redirects(self):
        """/portal/referral/ POST must succeed and redirect back to dashboard."""
        self.client.force_login(self.user)
        with mock.patch('portal.views._call_ohq', return_value=None):
            resp = self.client.post('/portal/referral/', {
                'referred_name':  'A Friend',
                'referred_phone': '555-0200',
                'referred_email': 'friend@example.com',
            })
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/portal/dashboard/', resp.url)

    def test_dashboard_redirects_anonymous_to_login(self):
        """Sanity: unauthenticated GET must not 200 the dashboard."""
        resp = self.client.get('/portal/dashboard/')
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/portal/', resp.url)
