from django.shortcuts import render
import csv
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import Student

def generate_csv_response(request):
    queryset = Student.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="student_data.csv"'
    writer = csv.writer(response)
    writer.writerow([field.name for field in queryset.model._meta.fields])

    for obj in queryset:
        writer.writerow([getattr(obj,field.name) for field in queryset.model._meta.fields])
    return response

def generate_pdf_response(request):
    queryset = Student.objects.all()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="student_pdfdata.pdf"'
    pdf = canvas.Canvas(response)
    y = 800
    pdf.setFont("Helvetica-Bold",12)
    pdf.drawString(180,y,"Student Data")

    pdf.setFont("Helvetica",10)
    y-=30

    for obj in queryset:
        data = f"name:{obj.name},Email{obj.email}"
        if(y<50):
            pdf.showPage()
            y = 800
            pdf.setFont("Helvetica",10)

        pdf.drawString(100,y,data)
        y-=15
    pdf.showPage()
    pdf.save()
    return response