from django.urls import path

from app import views

urlpatterns = [
    path('transactions/', views.TransactionView.as_view(), name='create_transaction'),
    path('stats/', views.StatsView.as_view(), name='transaction_stats'),
]
