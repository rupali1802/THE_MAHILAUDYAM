from django.urls import path
from . import views

urlpatterns = [
    # Diagnostics
    path('diagnostics/', views.DiagnosticsView.as_view(), name='diagnostics'),

    # User
    path('user/', views.UserProfileView.as_view(), name='user-profile'),

    # Income
    path('income/', views.IncomeListView.as_view(), name='income-list'),
    path('income/add/', views.IncomeAddView.as_view(), name='income-add'),
    path('income/<int:pk>/', views.IncomeDetailView.as_view(), name='income-detail'),

    # Expense
    path('expense/', views.ExpenseListView.as_view(), name='expense-list'),
    path('expense/add/', views.ExpenseAddView.as_view(), name='expense-add'),
    path('expense/<int:pk>/', views.ExpenseDetailView.as_view(), name='expense-detail'),

    # Sales
    path('sales/', views.SalesListView.as_view(), name='sales-list'),
    path('sales/add/', views.SalesAddView.as_view(), name='sales-add'),
    path('sales/<int:pk>/', views.SalesDetailView.as_view(), name='sales-detail'),

    # Profit
    path('profit/', views.ProfitView.as_view(), name='profit'),

    # Market Prices
    path('market-prices/', views.MarketPriceListView.as_view(), name='market-prices'),
    path('market-analysis/', views.MarketAnalysisView.as_view(), name='market-analysis'),
    path('price-history/', views.PriceHistoryView.as_view(), name='price-history'),
    path('price-trends/', views.PriceTrendsView.as_view(), name='price-trends'),
    path('market-comparative/', views.MarketComparativeAnalysisView.as_view(), name='market-comparative'),
    path('market-realtime/', views.RealtimeMarketAnalysisView.as_view(), name='market-realtime'),

    # Schemes
    path('schemes/', views.SchemeListView.as_view(), name='schemes'),

    # Mentors
    path('mentors/', views.MentorListView.as_view(), name='mentors'),
    path('mentor-chat/', views.MentorChatView.as_view(), name='mentor-chat'),
    path('mentor-ai/', views.MentorAIView.as_view(), name='mentor-ai'),

    # Voice / ML
    path('predict-intent/', views.PredictIntentView.as_view(), name='predict-intent'),
    
    # Prediction Monitoring & Feedback (NEW)
    path('prediction-feedback/', views.PredictionFeedbackView.as_view(), name='prediction-feedback'),
    path('prediction-accuracy/', views.PredictionAccuracyView.as_view(), name='prediction-accuracy'),
    path('prediction/<int:prediction_id>/', views.PredictionDetailView.as_view(), name='prediction-detail'),
    path('predictions/', views.PredictionListView.as_view(), name='prediction-list'),

    # Dashboard
    path('dashboard/', views.DashboardSummaryView.as_view(), name='dashboard'),
]
