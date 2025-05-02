from rest_framework import serializers
from .models import Contact
from company.models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name']
        ref_name = 'ContactCompanySerializer'


class ContactSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    company_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Contact
        fields = [ 'id', 'company', 'company_id', 'first_name', 'last_name',
                   'position', 'email', 'phone', 'is_primary', 'created_at']
        read_only_fields = ['created_at']
        ref_name = 'ContactSerializer'

    def validate_company_id(self, value):
        try:
            Company.objects.get(pk=value)
        except Company.DoesNotExist:
            raise serializers.ValidationError("Bunday kompaniya mavjud emas")
        return value

    def validate(self, attrs):
        company_id = attrs.get('company_id')
        email = attrs.get('email')

        if self.instance:
            existing = Contact.objects.filter(
                company_id=company_id,
                email=email
            ).exclude(id=self.instance.id)
        else:
            existing = Contact.objects.filter(
                company_id=company_id,
                email=email
            )

        if existing.exists():
            raise serializers.ValidationError({
                'email': 'Bu kompaniyada bu email bilan kontakt allaqachon mavjud.'
            })

        return attrs

    def get_name(self, obj):
        return obj.get_full_name()

    def create(self, validated_data):
        company_id = validated_data.pop('company_id')
        company = Company.objects.get(pk=company_id)
        contact = Contact.objects.create(company=company, **validated_data)
        return contact

    def update(self, instance, validated_data):
        if 'company_id' in validated_data:
            company_id = validated_data.pop('company_id')
            instance.company = Company.objects.get(pk=company_id)
        return super().update(instance, validated_data)
