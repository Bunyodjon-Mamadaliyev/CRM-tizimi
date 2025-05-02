from django.test import TestCase
from django.contrib.auth.models import User
from company.models import Company
from django.core.exceptions import ValidationError
from .models import Contact


class ContactModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.company = Company.objects.create(name='Test Company', owner=self.user)

    def test_create_contact(self):
        contact = Contact.objects.create(
            company=self.company,
            owner=self.user,
            first_name='John',
            last_name='Doe',
            position='Manager',
            email='john.doe@example.com',
            phone='+12345678901',
            is_primary=True
        )
        self.assertEqual(contact.first_name, 'John')
        self.assertEqual(contact.last_name, 'Doe')
        self.assertEqual(contact.position, 'Manager')
        self.assertEqual(contact.email, 'john.doe@example.com')
        self.assertEqual(contact.phone, '+12345678901')
        self.assertTrue(contact.is_primary)

    def test_unique_together(self):
        contact1 = Contact.objects.create(
            company=self.company,
            owner=self.user,
            first_name='Alice',
            last_name='Smith',
            position='Developer',
            email='alice.smith@example.com',
            phone='+12345678902',
            is_primary=False
        )

        with self.assertRaises(Exception):
            Contact.objects.create(
                company=self.company,
                owner=self.user,
                first_name='Bob',
                last_name='Johnson',
                position='Designer',
                email='alice.smith@example.com',
                phone='+12345678903',
                is_primary=False
            )

    def test_primary_contact(self):
        contact1 = Contact.objects.create(
            company=self.company,
            owner=self.user,
            first_name='John',
            last_name='Doe',
            position='Manager',
            email='john.doe@example.com',
            phone='+12345678901',
            is_primary=True
        )
        contact2 = Contact.objects.create(
            company=self.company,
            owner=self.user,
            first_name='Jane',
            last_name='Doe',
            position='Assistant',
            email='jane.doe@example.com',
            phone='+12345678904',
            is_primary=False
        )
        self.assertTrue(contact1.is_primary)
        self.assertFalse(contact2.is_primary)
        contact2.is_primary = True
        contact2.save()

        contact1.refresh_from_db()
        contact2.refresh_from_db()

        self.assertFalse(contact1.is_primary)
        self.assertTrue(contact2.is_primary)

    def test_full_name_method(self):
        contact = Contact.objects.create(
            company=self.company,
            owner=self.user,
            first_name='John',
            last_name='Doe',
            position='Manager',
            email='john.doe@example.com',
            phone='+12345678901',
            is_primary=False
        )
        self.assertEqual(contact.get_full_name(), 'John Doe')

    def test_phone_number_validation(self):
        contact = Contact(
            company=self.company,
            owner=self.user,
            first_name="Invalid",
            last_name="Phone",
            position="Tester",
            email="invalid.phone@test.com",
            phone="12345",
            is_primary=False
        )
        with self.assertRaises(ValidationError):
            contact.full_clean()

    def test_ordering(self):
        contact1 = Contact.objects.create(
            company=self.company,
            owner=self.user,
            first_name='John',
            last_name='Doe',
            position='Manager',
            email='john.doe@example.com',
            phone='+12345678901',
            is_primary=False
        )
        contact2 = Contact.objects.create(
            company=self.company,
            owner=self.user,
            first_name='Jane',
            last_name='Smith',
            position='Assistant',
            email='jane.smith@example.com',
            phone='+12345678902',
            is_primary=True
        )

        contacts = Contact.objects.all()
        self.assertEqual(contacts.first(), contact2)
        self.assertEqual(contacts.last(), contact1)
