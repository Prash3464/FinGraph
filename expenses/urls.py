from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='home'),
    path('home/', views.home_view, name='home'),
    path('add/', views.add_expense_view, name='add'),
    path('search/', views.search_expense, name='search_expense'),
    path('edit/', views.edit_expense_page, name='edit'),
    path('update-expense/<int:id>/', views.update_expense_view, name='update-expense'),
    path('delete-expense/<int:id>/', views.delete_expense_view, name='delete-expense'),
    path('export_expenses', views.export_expenses, name='export_expenses'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('settings/', views.settings_view, name='settings'),
]
