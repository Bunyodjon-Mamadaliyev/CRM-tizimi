from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Activity
from .serializers import ActivitySerializer
from rest_framework.permissions import IsAuthenticated
import tablib
from django.http import HttpResponse


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.select_related('company', 'contact', 'deal', 'assigned_to').all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().order_by('-due_date')

    def export_dataset(self, dataset, format):
        if format == 'csv':
            content = dataset.export('csv')
            content_type = 'text/csv'
            filename = 'activities.csv'
        elif format == 'xls':
            content = dataset.export('xls')
            content_type = 'application/vnd.ms-excel'
            filename = 'activities.xls'
        elif format == 'json':
            content = dataset.export('json')
            content_type = 'application/json'
            filename = 'activities.json'
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
                'ID', 'Company', 'Contact', 'Deal',
                'Activity Type', 'Subject', 'Description',
                'Due Date', 'Status', 'Assigned To',
                'Created At', 'Updated At'
            ]
            for activity in queryset:
                dataset.append([
                    activity.id,
                    activity.company.name if activity.company else '',
                    f"{activity.contact.first_name} {activity.contact.last_name}" if activity.contact else '',
                    activity.deal.title if activity.deal else '',
                    activity.get_activity_type_display(),
                    activity.subject,
                    activity.description,
                    activity.due_date,
                    activity.get_status_display(),
                    str(activity.assigned_to),
                    activity.created_at,
                    activity.updated_at,
                ])
            return self.export_dataset(dataset, format)

        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_path='calendar')
    def calendar(self, request):
        format = request.query_params.get('format')
        queryset = self.filter_queryset(self.get_queryset())

        if format in ['csv', 'xls', 'json']:
            dataset = tablib.Dataset()
            dataset.headers = [
                'ID', 'Company', 'Subject',
                'Due Date', 'Status', 'Assigned To'
            ]
            for activity in queryset:
                dataset.append([
                    activity.id,
                    activity.company.name,
                    activity.subject,
                    activity.due_date,
                    activity.get_status_display(),
                    str(activity.assigned_to),
                ])
            return self.export_dataset(dataset, format)

        return Response([
            {
                "id": act.id,
                "title": act.subject,
                "start": act.due_date,
                "status": act.status,
                "company": act.company.name,
                "assigned_to": str(act.assigned_to)
            }
            for act in queryset
        ])
