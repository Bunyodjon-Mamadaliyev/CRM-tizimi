from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'industry', 'employees_count', 'annual_revenue',
                  'website', 'address', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        ref_name = 'CompanySerializer'