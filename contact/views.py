from rest_framework import generics, response, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from django.http import HttpResponse
from .models import Contact
from rest_framework.permissions import IsAuthenticated
from .serializers import ContactSerializer
from company.models import Company


class ContactListCreateView(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    parser_classes = [MultiPartParser, FormParser]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        company_id = self.request.query_params.get('company_id')
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        return queryset

    def list(self, request, *args, **kwargs):
        format = request.query_params.get('format', 'json')

        if format.lower() == 'json':
            return super().list(request, *args, **kwargs)

        queryset = self.filter_queryset(self.get_queryset())

        if format.lower() == 'csv':
            import csv
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="contacts.csv"'

            writer = csv.writer(response)
            writer.writerow(
                ['ID', 'Company', 'First Name', 'Last Name', 'Position', 'Email', 'Phone', 'Is Primary', 'Created At'])

            for contact in queryset:
                writer.writerow([
                    contact.id,
                    contact.company.name,
                    contact.first_name,
                    contact.last_name,
                    contact.position,
                    contact.email,
                    contact.phone,
                    contact.is_primary,
                    contact.created_at
                ])
            return response

        elif format.lower() in ['excel', 'xlsx']:
            import pandas as pd
            data = list(queryset.values(
                'id', 'company__name', 'first_name', 'last_name',
                'position', 'email', 'phone', 'is_primary', 'created_at'
            ))
            df = pd.DataFrame(data)
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="contacts.xlsx"'
            df.to_excel(response, index=False)
            return response

        elif format.lower() == 'pdf':
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
            from reportlab.lib import colors

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="contacts.pdf"'

            doc = SimpleDocTemplate(response, pagesize=letter)
            elements = []

            data = [
                ['ID', 'Company', 'First Name', 'Last Name', 'Position', 'Email', 'Phone', 'Is Primary', 'Created At']]

            for contact in queryset:
                data.append([
                    str(contact.id),
                    contact.company.name,
                    contact.first_name,
                    contact.last_name,
                    contact.position,
                    contact.email,
                    contact.phone,
                    "Yes" if contact.is_primary else "No",
                    contact.created_at.strftime("%Y-%m-%d %H:%M:%S")
                ])

            t = Table(data)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))

            elements.append(t)
            doc.build(elements)
            return response

        return super().list(request, *args, **kwargs)


class ContactRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        format = request.query_params.get('format', 'json')
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        if format.lower() == 'pdf':
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib import colors

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="contact_{instance.id}.pdf"'

            doc = SimpleDocTemplate(response, pagesize=letter)
            styles = getSampleStyleSheet()
            elements = []

            title = Paragraph(f"Contact Details - {instance.get_full_name()}", styles['Title'])
            elements.append(title)
            elements.append(Spacer(1, 12))

            data = [
                ["Field", "Value"],
                ["ID", instance.id],
                ["Company", instance.company.name],
                ["Full Name", instance.get_full_name()],
                ["Position", instance.position],
                ["Email", instance.email],
                ["Phone", instance.phone],
                ["Is Primary", "Yes" if instance.is_primary else "No"],
                ["Created At", instance.created_at.strftime("%Y-%m-%d %H:%M:%S")]
            ]

            from reportlab.platypus import Table, TableStyle
            t = Table(data)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))

            elements.append(t)
            doc.build(elements)
            return response

        return Response(serializer.data)