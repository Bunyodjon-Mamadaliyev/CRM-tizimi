from rest_framework import serializers
from .models import Activity
from company.models import Company
from contact.models import Contact
from deal.models import Deal
from django.contrib.auth import get_user_model

User = get_user_model()

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name']
        ref_name = 'ActivityCompanySerializer'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'first_name', 'last_name']
        ref_name = 'ActivityContactSerializer'

class DealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = ['id', 'title']
        ref_name = 'ActivityDealSerializer'

class ActivitySerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    company_id = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), source='company', write_only=True)

    contact = ContactSerializer(read_only=True)
    contact_id = serializers.PrimaryKeyRelatedField(queryset=Contact.objects.all(), source='contact', write_only=True, allow_null=True, required=False)

    deal = DealSerializer(read_only=True)
    deal_id = serializers.PrimaryKeyRelatedField(queryset=Deal.objects.all(), source='deal', write_only=True, allow_null=True, required=False)

    assigned_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Activity
        fields = [
            'id',
            'company', 'company_id',
            'contact', 'contact_id',
            'deal', 'deal_id',
            'activity_type', 'subject', 'description',
            'due_date', 'status',
            'assigned_to',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
