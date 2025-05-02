from django.test import TestCase
from django.contrib.auth.models import User
from company.models import Company
from deal.models import Deal
from datetime import date, timedelta


class DealModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.company = Company.objects.create(
            name='Test Company',
            owner=self.user,
            industry='IT',
            annual_revenue=1000000,
            website='https://test.com',
            address='Test address'
        )

        self.deal = Deal.objects.create(
            company=self.company,
            title='Test Deal',
            description='Test description',
            amount=5000,
            currency='USD',
            stage='LEAD',
            expected_closing_date=date.today() + timedelta(days=30),
            assigned_to=self.user
        )

    def test_deal_creation(self):
        self.assertEqual(self.deal.title, 'Test Deal')
        self.assertEqual(self.deal.company.name, 'Test Company')
        self.assertEqual(self.deal.assigned_to.username, 'testuser')
        self.assertEqual(self.deal.stage, 'LEAD')
        self.assertEqual(self.deal.currency, 'USD')

    def test_is_closed_property(self):
        self.assertFalse(self.deal.is_closed)
        self.deal.stage = 'WON'
        self.assertTrue(self.deal.is_closed)
        self.deal.stage = 'LOST'
        self.assertTrue(self.deal.is_closed)
        self.deal.stage = 'NEGOTIATION'
        self.assertFalse(self.deal.is_closed)

    def test_str_representation(self):
        self.assertEqual(str(self.deal), 'Test Deal (Test Company)')

    def test_meta_options(self):
        self.assertEqual(Deal._meta.verbose_name, 'Bitim')
        self.assertEqual(Deal._meta.verbose_name_plural, 'Bitimlar')
        self.assertEqual(Deal._meta.ordering, ['-expected_closing_date'])