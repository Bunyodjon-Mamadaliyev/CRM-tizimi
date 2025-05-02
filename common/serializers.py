from rest_framework import serializers

class SalesByCompanySerializer(serializers.Serializer):
    company = serializers.CharField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    percentage = serializers.FloatField()


class SalesReportSerializer(serializers.Serializer):
    total_sales = serializers.DecimalField(max_digits=12, decimal_places=2)
    sales_by_month = serializers.DictField(child=serializers.CharField())
    sales_by_company = SalesByCompanySerializer(many=True)
    sales_by_stage = serializers.DictField(child=serializers.CharField())


class ActivitiesByCompanySerializer(serializers.Serializer):
    company = serializers.CharField()
    count = serializers.IntegerField()
    percentage = serializers.FloatField()


class ActivitiesByUserSerializer(serializers.Serializer):
    user = serializers.CharField()
    count = serializers.IntegerField()
    percentage = serializers.FloatField()


class ActivitiesReportSerializer(serializers.Serializer):
    total_activities = serializers.IntegerField()
    activities_by_type = serializers.DictField(child=serializers.IntegerField())
    activities_by_status = serializers.DictField(child=serializers.IntegerField())
    activities_by_company = ActivitiesByCompanySerializer(many=True)
    activities_by_user = ActivitiesByUserSerializer(many=True)


class CompaniesReportSerializer(serializers.Serializer):
    total_companies = serializers.IntegerField()
    companies_by_industry = serializers.DictField(child=serializers.IntegerField())
    companies_by_employees = serializers.DictField(child=serializers.IntegerField())
    companies_by_revenue = serializers.DictField(child=serializers.IntegerField())
    new_companies_by_month = serializers.DictField(child=serializers.IntegerField())


class DealStageDataSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)


class DealMonthDataSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)


class DealsByUserSerializer(serializers.Serializer):
    user = serializers.CharField()
    count = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)


class DealsReportSerializer(serializers.Serializer):
    total_deals = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    deals_by_stage = serializers.DictField(child=DealStageDataSerializer())
    deals_by_month = serializers.DictField(child=DealMonthDataSerializer())
    deals_by_user = DealsByUserSerializer(many=True)
