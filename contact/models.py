from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Contact(models.Model):
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE,
                        related_name='contacts', verbose_name="Kompaniya")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, verbose_name="Ism")
    last_name = models.CharField(max_length=100, verbose_name="Familiya")
    position = models.CharField(max_length=255, verbose_name="Lavozim")
    email = models.EmailField(max_length=255, verbose_name="Elektron pochta")
    phone = models.CharField(max_length=20, validators=[RegexValidator(regex=r'^\+?[0-9]{9,15}$',
        message="Telefon raqami '+' bilan boshlanishi va 9-15 ta raqamdan iborat bo'lishi kerak" )],
        verbose_name="Telefon raqami")
    is_primary = models.BooleanField( default=False, verbose_name="Asosiy kontakt")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")

    class Meta:
        verbose_name = "Kontakt"
        verbose_name_plural = "Kontaktlar"
        ordering = ['-is_primary', 'last_name', 'first_name']
        unique_together = ['company', 'email']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.position})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.owner:
            raise ValueError("Owner must be set for the contact.")
        if self.is_primary:
            Contact.objects.filter(company=self.company, is_primary=True).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)
