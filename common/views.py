from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
import csv
import io
import xlsxwriter
from reportlab.pdfgen import canvas
from .serializers import (
    SalesReportSerializer, ActivitiesReportSerializer,
    CompaniesReportSerializer, DealsReportSerializer)


class ReportBaseView(APIView):
    def get_format(self, request):
        return request.query_params.get("format", "json").lower()

    def render_csv(self, headers, rows, filename):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
        writer = csv.writer(response)
        writer.writerow(headers)
        for row in rows:
            writer.writerow(row)
        return response

    def render_excel(self, headers, rows, filename):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()

        worksheet.write_row(0, 0, headers)
        for idx, row in enumerate(rows, start=1):
            worksheet.write_row(idx, 0, row)

        workbook.close()
        output.seek(0)
        response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'
        return response

    def render_pdf(self, title, headers, rows, filename):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}.pdf"'

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, 800, title)

        p.setFont("Helvetica", 12)
        y = 770
        p.drawString(100, y, " | ".join(headers))
        y -= 20

        for row in rows:
            p.drawString(100, y, " | ".join(str(item) for item in row))
            y -= 20
            if y < 40:
                p.showPage()
                y = 800

        p.showPage()
        p.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

class SalesReportView(ReportBaseView):
    def get(self, request):
        data = {
            "total_sales": "60000.00",
            "sales_by_month": {
                "2023-01": "0.00", "2023-02": "0.00", "2023-03": "0.00",
                "2023-04": "0.00", "2023-05": "0.00", "2023-06": "0.00", "2023-07": "60000.00"
            },
            "sales_by_company": [
                {"company": "Techno Solutions", "amount": "60000.00", "percentage": 100}
            ],
            "sales_by_stage": {
                "Lead": "0.00", "Negotiation": "0.00", "Won": "60000.00", "Lost": "0.00"
            }
        }

        fmt = self.get_format(request)
        if fmt == "csv":
            return self.render_csv(
                ["Company", "Amount", "Percentage"],
                [[c["company"], c["amount"], c["percentage"]] for c in data["sales_by_company"]],
                "sales_report"
            )
        elif fmt == "excel":
            return self.render_excel(
                ["Company", "Amount", "Percentage"],
                [[c["company"], c["amount"], c["percentage"]] for c in data["sales_by_company"]],
                "sales_report"
            )
        elif fmt == "pdf":
            return self.render_pdf(
                "Sales Report",
                ["Company", "Amount", "Percentage"],
                [[c["company"], c["amount"], c["percentage"]] for c in data["sales_by_company"]],
                "sales_report"
            )

        serializer = SalesReportSerializer(data)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class ActivitiesReportView(ReportBaseView):
    def get(self, request):
        data = {
            "total_activities": 3,
            "activities_by_type": {"Meeting": 1, "Call": 1, "Email": 1, "Task": 0},
            "activities_by_status": {"Planned": 0, "In Progress": 0, "Completed": 3, "Canceled": 0},
            "activities_by_company": [
                {"company": "Techno Solutions", "count": 2, "percentage": 66.67},
                {"company": "Global Trade", "count": 1, "percentage": 33.33}
            ],
            "activities_by_user": [
                {"user": "Admin User", "count": 2, "percentage": 66.67},
                {"user": "Sales Manager", "count": 1, "percentage": 33.33}
            ]
        }

        fmt = self.get_format(request)
        if fmt == "csv":
            return self.render_csv(
                ["Company", "Count", "Percentage"],
                [[c["company"], c["count"], c["percentage"]] for c in data["activities_by_company"]],
                "activities_report"
            )
        elif fmt == "excel":
            return self.render_excel(
                ["Company", "Count", "Percentage"],
                [[c["company"], c["count"], c["percentage"]] for c in data["activities_by_company"]],
                "activities_report"
            )
        elif fmt == "pdf":
            return self.render_pdf(
                "Activities Report",
                ["Company", "Count", "Percentage"],
                [[c["company"], c["count"], c["percentage"]] for c in data["activities_by_company"]],
                "activities_report"
            )

        serializer = ActivitiesReportSerializer(data)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class CompaniesReportView(ReportBaseView):
    def get(self, request):
        data = {
            "total_companies": 2,
            "companies_by_industry": {"IT": 1, "Retail": 1},
            "companies_by_employees": {"1-50": 0, "51-100": 1, "101-500": 1, "501+": 0},
            "companies_by_revenue": {"< 1M": 0, "1M - 5M": 1, "5M - 10M": 1, "> 10M": 0},
            "new_companies_by_month": {
                "2023-01": 0, "2023-02": 0, "2023-03": 0, "2023-04": 0,
                "2023-05": 0, "2023-06": 2, "2023-07": 0
            }
        }

        fmt = self.get_format(request)
        if fmt == "csv":
            return self.render_csv(
                ["Industry", "Count"],
                [[k, v] for k, v in data["companies_by_industry"].items()],
                "companies_report"
            )
        elif fmt == "excel":
            return self.render_excel(
                ["Industry", "Count"],
                [[k, v] for k, v in data["companies_by_industry"].items()],
                "companies_report"
            )
        elif fmt == "pdf":
            return self.render_pdf(
                "Companies Report",
                ["Industry", "Count"],
                [[k, v] for k, v in data["companies_by_industry"].items()],
                "companies_report"
            )

        serializer = CompaniesReportSerializer(data)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


class DealsReportView(ReportBaseView):
    def get(self, request):
        data = {
            "total_deals": 2,
            "total_amount": "95000.00",
            "deals_by_stage": {
                "Lead": {"count": 1, "amount": "35000.00"},
                "Negotiation": {"count": 0, "amount": "0.00"},
                "Won": {"count": 1, "amount": "60000.00"},
                "Lost": {"count": 0, "amount": "0.00"}
            },
            "deals_by_month": {
                "2023-06": {"count": 1, "amount": "50000.00"},
                "2023-07": {"count": 1, "amount": "45000.00"}
            },
            "deals_by_user": [
                {"user": "Admin User", "count": 1, "amount": "60000.00"},
                {"user": "Sales Manager", "count": 1, "amount": "35000.00"}
            ]
        }

        fmt = self.get_format(request)
        if fmt == "csv":
            return self.render_csv(
                ["User", "Count", "Amount"],
                [[u["user"], u["count"], u["amount"]] for u in data["deals_by_user"]],
                "deals_report"
            )
        elif fmt == "excel":
            return self.render_excel(
                ["User", "Count", "Amount"],
                [[u["user"], u["count"], u["amount"]] for u in data["deals_by_user"]],
                "deals_report"
            )
        elif fmt == "pdf":
            return self.render_pdf(
                "Deals Report",
                ["User", "Count", "Amount"],
                [[u["user"], u["count"], u["amount"]] for u in data["deals_by_user"]],
                "deals_report"
            )

        serializer = DealsReportSerializer(data)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
