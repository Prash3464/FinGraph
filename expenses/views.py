from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from django.db.models.functions import TruncMonth
import json
from django.http import JsonResponse
from .models import Expense
from datetime import datetime
from .utils import generate_csv, generate_pdf ,generate_excel


# Create your views here.


def base(request):
    return render(request, 'home.html')

def home_view(request):
    user = request.user

    # Group expenses by month for the current user
    monthly_expenses = (
        Expense.objects.filter(user=user)
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )

    # Format data for Plotly: month names and totals
    labels = []
    totals = []

    for item in monthly_expenses:
        month_name = item['month'].strftime('%b')  # e.g., Jan, Feb
        labels.append(month_name)
        totals.append(float(item['total']))  # Ensure JSON serializable

    recent_expenses = Expense.objects.filter(user=request.user).order_by('-date')[:5]

    context = {
        "recent_expenses": recent_expenses,
        "graph_labels": json.dumps(labels),
        "graph_totals": json.dumps(totals),
    }

    return render(request, 'home.html',context)



def add_expense_view(request):
    if request.method == "POST":
        title = request.POST.get('title')
        category = request.POST.get('category')
        amount = request.POST.get('amount')
        date = request.POST.get('date')
        description = request.POST.get('description')
        payment_method = request.POST.get('method')

        if not (title and category and amount and date and description):
            messages.error(request, 'Please fill all fields')
            return redirect(add_expense_view)

        try:
            amount = float(amount)
        except ValueError:
            messages.error(request, 'Invalid amount')
            return redirect(add_expense_view)

        Expense.objects.create(
            user=request.user,
            title=title,
            category=category,
            amount=amount,
            date=date,
            description=description,
            payment_method=payment_method,
        )

        messages.success(request, 'Expense Added')
        return redirect(home_view)


    return render(request, 'add-expenses.html')

@login_required
def edit_expense_page(request):
    return render(request, "edit_expenses.html")

@login_required
def search_expense(request):
    if request.method == "GET":
        title = request.GET.get('title', '').strip()
        date = request.GET.get('date', '').strip()

        expenses = Expense.objects.filter(user=request.user)
        if title:
            expenses = expenses.filter(title__icontains=title)
        if date:
            expenses = expenses.filter(date__icontains=date)

        if expenses.exists():
            expense_list = []
            for expense in expenses:
                expense_list.append({
                    'id': expense.id,
                    'title': expense.title,
                    'category': expense.category,
                    'amount': str(expense.amount),
                    'date': expense.date.isoformat(),
                    'description': expense.description,
                    'payment_method': expense.payment_method,
                })

            return JsonResponse({'success': True, 'expenses': expense_list})
        else:
            return JsonResponse({'success': False, 'message': 'No expense found'})

@csrf_exempt
@login_required()
def update_expense_view(request, id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            expense = Expense.objects.get(pk=id, user=request.user)

            expense.title = data.get("title")
            expense.category = data.get("category")
            expense.amount = data.get("amount")
            expense.date = data.get("date")
            expense.description = data.get("description")
            expense.payment_method = data.get("payment_method")
            expense.save()

            return JsonResponse({'success': True})

        except Expense.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Expense not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'No expense found'})

@login_required
@csrf_exempt
def delete_expense_view(request, id):
    if request.method == "DELETE":
        try:
            expense = Expense.objects.get(pk=id, user=request.user)
            expense.delete()
            return JsonResponse({'success': True})
        except Expense.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Expense not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid method'})


@login_required
def analytics_view(request):
    selected_month = request.GET.get("month")  # Format: "2025-08"
    view_type = request.GET.get("view_type", "daily")

    # Filter expenses by user
    expenses = Expense.objects.filter(user=request.user)

    if selected_month:
        expenses = expenses.filter(date__startswith=selected_month)

    if view_type == "monthly":
        from django.db.models.functions import TruncMonth
        groups = (
            expenses
            .annotate(month=TruncMonth('date'))
            .values("month")
            .annotate(total=Sum("amount"))
            .order_by("month")
        )
        labels = []
        totals =[]
        for item in groups:
            month_name = item["month"].strftime("%B")
            labels.append(month_name)
            totals.append(item["total"])

    elif view_type == "yearly":
        from django.db.models.functions import TruncMonth
        if selected_month:
            selected_year = selected_month.split("-")[0]
            expenses = expenses.filter(date__year=selected_year)
        groups = (
            expenses
            .annotate(month=TruncMonth('date'))
            .values("month")
            .annotate(total=Sum("amount"))
            .order_by("month")
        )
        labels = [item["month"].strftime("%B") for item in groups]
    else:
        from django.db.models.functions import TruncDay
        groups = (
            expenses
            .annotate(day=TruncDay('date'))
            .values("day")
            .annotate(total=Sum("amount"))
            .order_by("day")
        )
        labels = [item["day"].strftime("%Y-%m-%d") for item in groups]

    totals = [float(item["total"]) for item in groups]

    context = {
        "labels": labels,
        "totals": totals,
        "selected_month": selected_month or datetime.today().strftime("%Y-%m"),
        "selected_view": view_type,
        "expenses_list": expenses.order_by("-date"),
        "now": datetime.now(),
    }

    return render(request, "analytics.html", context)
@login_required
def export_expenses(request):
    format = request.GET.get("format")
    export_option = request.GET.get("export_option")
    month = request.GET.get("month")

    expenses = Expense.objects.filter(user=request.user)

    if export_option == "month" and month:
        expenses = expenses.filter(date__startswith=month)

    if format == "pdf":
        return generate_pdf(expenses)
    elif format == "excel":
        return generate_excel(expenses)
    else:
        return generate_csv(expenses)


@login_required
def settings_view(request):
    return render(request, 'settings.html')