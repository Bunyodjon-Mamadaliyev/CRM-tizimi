from django.test import TestCase
from django.contrib.auth.models import User
from company.models import Company
from contact.models import Contact
from deal.models import Deal
from activity.models import Activity
from datetime import timedelta
from django.utils import timezone


class ActivityModelTest(TestCase):
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

        self.contact = Contact.objects.create(
            company=self.company,
            owner=self.user,
            first_name='John',
            last_name='Doe',
            position='CEO',
            email='john@test.com',
            phone='+1234567890'
        )

        self.deal = Deal.objects.create(
            company=self.company,
            title='Test Deal',
            description='Test description',
            amount=5000,
            currency='USD',
            stage='LEAD',
            expected_closing_date=timezone.now().date() + timedelta(days=30),
            assigned_to=self.user
        )

        self.activity = Activity.objects.create(
            company=self.company,
            contact=self.contact,
            deal=self.deal,
            activity_type='CALL',
            subject='Test Call',
            description='Test call description',
            due_date=timezone.now() + timedelta(days=1),
            status='PLANNED',
            assigned_to=self.user
        )

    def test_activity_creation(self):
        self.assertEqual(self.activity.subject, 'Test Call')
        self.assertEqual(self.activity.company.name, 'Test Company')
        self.assertEqual(self.activity.contact.first_name, 'John')
        self.assertEqual(self.activity.deal.title, 'Test Deal')
        self.assertEqual(self.activity.activity_type, 'CALL')
        self.assertEqual(self.activity.status, 'PLANNED')

    def test_is_overdue_property(self):
        self.assertFalse(self.activity.is_overdue)

        self.activity.due_date = timezone.now() - timedelta(days=1)
        self.activity.save()
        self.assertTrue(self.activity.is_overdue)

        self.activity.status = 'COMPLETED'
        self.activity.save()
        self.assertFalse(self.activity.is_overdue)

        self.activity.status = 'CANCELED'
        self.activity.save()
        self.assertFalse(self.activity.is_overdue)

    def test_str_representation(self):
        self.assertEqual(str(self.activity), "Qo'ng'iroq: Test Call (Test Company)")

    def test_meta_options(self):
        self.assertEqual(Activity._meta.verbose_name, 'Aktivlik')
        self.assertEqual(Activity._meta.verbose_name_plural, 'Aktivliklar')
        self.assertEqual(Activity._meta.ordering, ['-due_date'])

    def test_activity_without_contact_or_deal(self):
        activity = Activity.objects.create(
            company=self.company,
            activity_type='EMAIL',
            subject='Test Email',
            due_date=timezone.now() + timedelta(days=1),
            status='PLANNED',
            assigned_to=self.user
        )
        self.assertIsNone(activity.contact)
        self.assertIsNone(activity.deal)