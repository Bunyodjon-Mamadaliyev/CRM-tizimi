from rest_framework import serializers
from .models import Deal
from company.models import Company
from django.contrib.auth import get_user_model

User = get_user_model()

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name']
        ref_name = 'DealCompanySerializer'

class DealSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), source='company', write_only=True
    )
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Deal
        fields = ['id', 'company', 'company_id', 'title', 'description', 'amount',
                  'currency', 'stage', 'expected_closing_date', 'closed_date',
                  'assigned_to', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
        ref_name = 'DealSerializer'