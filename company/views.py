from rest_framework import generics
from rest_framework.response import Response
from rest_framework import filters
from .models import Company
from .serializers import CompanySerializer
from contact.serializers import ContactSerializer
from deal.serializers import DealSerializer
from activity.serializers import ActivitySerializer
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import HttpResponse
import pandas as pd
from reportlab.pdfgen import canvas
from io import BytesIO

class CompanyListCreateView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    parser_classes = (MultiPartParser, FormParser)

    def list(self, request, *args, **kwargs):
        format = request.query_params.get('format', None)

        if format in ['csv', 'excel', 'pdf']:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data

            if format == 'csv':
                df = pd.DataFrame(data)
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="companies.csv"'
                df.to_csv(path_or_buf=response, index=False)
                return response

            elif format == 'excel':
                df = pd.DataFrame(data)
                response = HttpResponse(content_type='application/vnd.ms-excel')
                response['Content-Disposition'] = 'attachment; filename="companies.xlsx"'
                df.to_excel(response, index=False)
                return response

            elif format == 'pdf':
                buffer = BytesIO()
                p = canvas.Canvas(buffer)
                p.drawString(100, 800, "Companies List")
                y = 780
                for company in data:
                    p.drawString(100, y,
                                 f"ID: {company['id']}, Name: {company['name']}, Industry: {company['industry']}")
                    y -= 20
                    if y < 50:
                        p.showPage()
                        y = 800

                p.showPage()
                p.save()

                pdf = buffer.getvalue()
                buffer.close()
                response = HttpResponse(pdf, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="companies.pdf"'
                return response

        return super().list(request, *args, **kwargs)


class CompanyRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        format = request.query_params.get('format', None)

        if format == 'pdf':
            data = serializer.data
            buffer = BytesIO()
            p = canvas.Canvas(buffer)

            p.drawString(100, 800, f"Company Details - {data['name']}")
            p.drawString(100, 780, f"ID: {data['id']}")
            p.drawString(100, 760, f"Name: {data['name']}")
            p.drawString(100, 740, f"Industry: {data['industry']}")
            p.drawString(100, 720, f"Employees: {data['employees_count']}")
            p.drawString(100, 700, f"Annual Revenue: {data['annual_revenue']}")
            p.drawString(100, 680, f"Website: {data['website']}")
            p.drawString(100, 660, f"Address: {data['address']}")

            p.showPage()
            p.save()

            pdf = buffer.getvalue()
            buffer.close()
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="company_{data["id"]}.pdf"'
            return response

        return super().retrieve(request, *args, **kwargs)


class CompanyContactsView(generics.GenericAPIView):
    queryset = Company.objects.all()
    serializer_class = ContactSerializer

    def get(self, request, *args, **kwargs):
        company = self.get_object()
        contacts = company.contacts.all()
        serializer = self.get_serializer(contacts, many=True)
        data = serializer.data

        format = request.query_params.get('format', None)

        if format == 'csv':
            df = pd.DataFrame(data)
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="company_{company.id}_contacts.csv"'
            df.to_csv(path_or_buf=response, index=False)
            return response

        elif format == 'excel':
            df = pd.DataFrame(data)
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = f'attachment; filename="company_{company.id}_contacts.xlsx"'
            df.to_excel(response, index=False)
            return response

        return Response(data)


class CompanyDealsView(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = DealSerializer
    def get(self, request, *args, **kwargs):
        company = self.get_object()
        deals = company.deals.all()
        serializer = self.get_serializer(deals, many=True)
        format = request.query_params.get('format', None)
        if format == 'csv':
            df = pd.DataFrame(serializer.data)
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="company_{company.id}_deals.csv"'
            df.to_csv(path_or_buf=response, index=False)
            return response
        elif format == 'excel':
            df = pd.DataFrame(serializer.data)
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = f'attachment; filename="company_{company.id}_deals.xlsx"'
            df.to_excel(response, index=False)
            return response

        return Response(serializer.data)


class CompanyActivitiesView(generics.GenericAPIView):
    queryset = Company.objects.all()
    serializer_class = ActivitySerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['due_date']

    def get(self, request, *args, **kwargs):
        company = self.get_object()
        activities = company.activities.all()
        serializer = self.get_serializer(activities, many=True)
        data = serializer.data

        format = request.query_params.get('format', None)

        if format == 'csv':
            df = pd.DataFrame(data)
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="company_{company.id}_activities.csv"'
            df.to_csv(path_or_buf=response, index=False)
            return response

        elif format == 'excel':
            df = pd.DataFrame(data)
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = f'attachment; filename="company_{company.id}_activities.xlsx"'
            df.to_excel(response, index=False)
            return response

        return Response(data)