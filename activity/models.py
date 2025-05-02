from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Activity(models.Model):
    class ActivityType(models.TextChoices):
        CALL = 'CALL', _('Qo\'ng\'iroq')
        EMAIL = 'EMAIL', _('Email')
        MEETING = 'MEETING', _('Uchrashuv')
        TASK = 'TASK', _('Vazifa')
        OTHER = 'OTHER', _('Boshqa')

    class Status(models.TextChoices):
        PLANNED = 'PLANNED', _('Rejalashtirilgan')
        IN_PROGRESS = 'IN_PROGRESS', _('Jarayonda')
        COMPLETED = 'COMPLETED', _('Yakunlangan')
        CANCELED = 'CANCELED', _('Bekor qilingan')

    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, related_name='activities',
                                verbose_name=_('Kompaniya'))
    contact = models.ForeignKey('contact.Contact', on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='activities', verbose_name=_('Kontakt'))
    deal = models.ForeignKey('deal.Deal', on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='activities', verbose_name=_('Bitim'))
    activity_type = models.CharField(max_length=20, choices=ActivityType.choices,
                                     default=ActivityType.CALL, verbose_name=_('Aktivlik turi'))
    subject = models.CharField(max_length=255, verbose_name=_('Mavzu'))
    description = models.TextField(verbose_name=_('Tavsif'), blank=True)
    due_date = models.DateTimeField( verbose_name=_('Bajarilish sanasi'))
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLANNED,
                              verbose_name=_('Holat'))
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                null=True, related_name='activities', verbose_name=_('Mas\'ul xodim'))
    created_at = models.DateTimeField( auto_now_add=True, verbose_name=_('Yaratilgan vaqt'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Yangilangan vaqt'))

    class Meta:
        verbose_name = _('Aktivlik')
        verbose_name_plural = _('Aktivliklar')
        ordering = ['-due_date']
        indexes = [
            models.Index(fields=['company', 'status']),
            models.Index(fields=['due_date']),
        ]

    def __str__(self):
        return f"{self.get_activity_type_display()}: {self.subject} ({self.company.name})"

    @property
    def is_overdue(self):
        from django.utils import timezone
        if self.due_date is None:
            return False
        return self.due_date < timezone.now() and self.status not in [
            self.Status.COMPLETED,
            self.Status.CANCELED
        ]
