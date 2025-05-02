from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

class Deal(models.Model):
    STAGE_CHOICES = [
        ('LEAD', 'Lead'),
        ('NEGOTIATION', 'Negotiation'),
        ('WON', 'Won'),
        ('LOST', 'Lost'),
    ]
    CURRENCY_CHOICES = [
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('UZS', 'UZS'),
    ]
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE,
                                related_name='deals', verbose_name="Kompaniya")
    title = models.CharField(max_length=255, verbose_name="Bitim nomi")
    description = models.TextField(verbose_name="Bitim tavsifi")
    amount = models.DecimalField(max_digits=15, decimal_places=2,
                    validators=[MinValueValidator(0)], verbose_name="Bitim summasi")
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES,
                                default='UZS', verbose_name="Valyuta")
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='LEAD',
                             verbose_name="Bitim bosqichi")
    expected_closing_date = models.DateField(verbose_name="Kutilayotgan yopilish sanasi")
    closed_date = models.DateField( null=True, blank=True, verbose_name="Yopilgan sana")
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                        null=True, related_name='deals', verbose_name="Mas'ul xodim")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqt")

    class Meta:
        verbose_name = "Bitim"
        verbose_name_plural = "Bitimlar"
        ordering = ['-expected_closing_date']

    def __str__(self):
        return f"{self.title} ({self.company.name})"

    @property
    def is_closed(self):
        return self.stage in ['WON', 'LOST']