from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Deal
from .serializers import DealSerializer
from django.db.models import Sum, Count
from rest_framework.permissions import IsAuthenticated
import tablib
from django.http import HttpResponse
from datetime import date

class DealViewSet(viewsets.ModelViewSet):
    queryset = Deal.objects.select_related('company', 'assigned_to').all()
    serializer_class = DealSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().order_by('-expected_closing_date')

    def export_dataset(self, dataset, format):
        if format == 'csv':
            content = dataset.export('csv')
            content_type = 'text/csv'
            filename = 'deals.csv'
        elif format == 'xls':
            content = dataset.export('xls')
            content_type = 'application/vnd.ms-excel'
            filename = 'deals.xls'
        elif format == 'json':
            content = dataset.export('json')
            content_type = 'application/json'
            filename = 'deals.json'
        elif format == 'pdf':
            return HttpResponse("PDF export not implemented", status=501)
        else:
            return HttpResponse("Invalid format", status=400)

        response = HttpResponse(content, content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    def list(self, request, *args, **kwargs):
        format = request.query_params.get('format')
        queryset = self.filter_queryset(self.get_queryset())

        if format in ['csv', 'xls', 'json']:
            dataset = tablib.Dataset()
            dataset.headers = [
                'ID', 'Company', 'Title', 'Description',
                'Amount', 'Currency', 'Stage',
                'Expected Closing Date', 'Closed Date',
                'Assigned To', 'Created At', 'Updated At'
            ]
            for deal in queryset:
                dataset.append([
                    deal.id, deal.company.name, deal.title, deal.description,
                    deal.amount, deal.currency, deal.stage,
                    deal.expected_closing_date, deal.closed_date,
                    str(deal.assigned_to), deal.created_at, deal.updated_at
                ])
            return self.export_dataset(dataset, format)

        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_path='by-stage')
    def by_stage(self, request):
        deals = self.get_queryset()
        grouped = deals.values('stage').annotate(count=Count('id'), total_amount=Sum('amount'))

        format = request.query_params.get('format')
        if format in ['csv', 'xls', 'json']:
            dataset = tablib.Dataset()
            dataset.headers = ['Stage', 'Count', 'Total Amount']
            for item in grouped:
                dataset.append([item['stage'], item['count'], item['total_amount']])
            return self.export_dataset(dataset, format)

        return Response(grouped)

    @action(detail=False, methods=['get'], url_path='forecast')
    def forecast(self, request):
        today = date.today()
        upcoming_deals = self.get_queryset().filter(
            expected_closing_date__gte=today,
            stage__in=['LEAD', 'NEGOTIATION']
        )
        total = upcoming_deals.aggregate(total_amount=Sum('amount'))
        format = request.query_params.get('format')

        if format in ['csv', 'xls', 'json']:
            dataset = tablib.Dataset()
            dataset.headers = ['Stage', 'Expected Closing', 'Amount']
            for deal in upcoming_deals:
                dataset.append([
                    deal.stage, deal.expected_closing_date, deal.amount
                ])
            return self.export_dataset(dataset, format)

        return Response({
            "forecast_total": total['total_amount'],
            "count": upcoming_deals.count()
        })
