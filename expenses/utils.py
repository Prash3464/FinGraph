from django.http import HttpResponse



def generate_csv(expenses):
    import csv

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses.csv"'

    writer = csv.writer(response)
    writer.writerow(["Title", "Category", "Amount", "Date", "Description", "Payment Method"])

    for expense in expenses:
        writer.writerow(
            expense.title,
            expense.category if hasattr(expense, "category") else "",
            expense.amount,
            expense.date.strftime("%d-%m-%Y")  if expense.date else "",
            expense.description if hasattr(expense, "description") else "",
            expense.payment_method
        )

    return response


from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, Spacer, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
def generate_pdf(expenses):

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="expenses.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # title
    elements.append(Paragraph("Expenses Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    # table data(colamns name)
    data = [["Title", "Category", "Amount", "Date", "Description", "Payment Method"]]
    for expense in expenses:
        data.append([
            expense.title,
            expense.category if hasattr(expense, "category") else "",
            f"₹{expense.amount}",
            expense.date.strftime("%d-%m-%Y")  if expense.date else "",
            expense.description if hasattr(expense, "description") else "",
            expense.payment_method
        ])

    # table formating
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1, -1), colors.gray),
        ('TEXTCOLOR', (0,0), (-1, 0), colors.whitesmoke),

        ('ALIGN', (-1,-1), (-1,-1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)
    doc.build(elements)
    return response


from openpyxl import Workbook
def generate_excel(expenses):
    wb = Workbook()
    ws = wb.active
    ws.title = "Expenses"

    # header row
    ws.append(["Title", "Category", "Amount", "Date", "Description", "Payment Method"])

    for expense in expenses:
        ws.append([
            expense.title,
            expense.category if hasattr(expense, "category") else "",
            expense.amount,
            expense.date.strftime("%d-%m-%Y")  if expense.date else "",
            expense.description if hasattr(expense, "description") else "",
            expense.payment_method
        ])


    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="expenses.xlsx"'
    wb.save(response)
    return response

