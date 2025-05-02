from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name="Kompaniya nomi")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='companies', default=1)
    industry = models.CharField(max_length=255, verbose_name="Faoliyat sohasi")
    employees_count = models.IntegerField(validators=[MinValueValidator(0)],
                                          verbose_name="Xodimlar soni", default=0)
    annual_revenue = models.DecimalField(max_digits=15, decimal_places=2,
                                         verbose_name="Yillik daromad", null=True, blank=True)
    website = models.URLField(max_length=255, verbose_name="Veb-sayt")
    address = models.TextField(verbose_name="Manzil")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqt")

    class Meta:
        verbose_name = "Kompaniya"
        verbose_name_plural = "Kompaniyalar"

    def __str__(self):
        return self.name