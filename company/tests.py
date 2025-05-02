from django.test import TestCase
from django.contrib.auth.models import User
from company.models import Company
from django.core.exceptions import ValidationError

class CompanyModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.company = Company.objects.create(
            name='Test Company',
            owner=self.user,
            industry='IT',
            employees_count=50,
            annual_revenue=1000000,
            website='https://test.com',
            address='Test address'
        )

    def test_company_creation(self):
        self.assertEqual(self.company.name, 'Test Company')
        self.assertEqual(self.company.owner.username, 'testuser')
        self.assertEqual(self.company.industry, 'IT')
        self.assertEqual(self.company.employees_count, 50)
        self.assertEqual(float(self.company.annual_revenue), 1000000.00)

    def test_str_representation(self):
        self.assertEqual(str(self.company), 'Test Company')

    def test_employees_count_validation(self):
        with self.assertRaises(ValidationError):
            company = Company(
                name='Invalid Company',
                owner=self.user,
                industry='IT',
                employees_count=-1,
                annual_revenue=1000000,
                website='https://invalid.com',
                address='Invalid address'
            )
            company.full_clean()

    def test_meta_options(self):
        self.assertEqual(Company._meta.verbose_name, 'Kompaniya')
        self.assertEqual(Company._meta.verbose_name_plural, 'Kompaniyalar')