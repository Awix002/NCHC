from django.urls import path
from .views import (
    DashboardData,
    DashboardDoughnutChart,
    DashboardPieChart,
    DashboardLineGraph,
    DashboardLabLineGraph,
    DashboardInventoryBarChart,
    DashboardLabBarChart,
    
)

urlpatterns = [
    path('dashboard/', DashboardData.as_view(), name='dashboard_data'),
    path('doughnut-chart/', DashboardDoughnutChart.as_view(), name='doughnut_chart'),
    path('pie-chart/', DashboardPieChart.as_view(), name='pie_chart'),
    path('line-graph/', DashboardLineGraph.as_view(), name='line_graph'),
    path('lab-line-graph/', DashboardLabLineGraph.as_view(), name='lab_line_graph'),
    path('inventory-bar-chart/', DashboardInventoryBarChart.as_view(), name='dashboard-inventory-bar-chart'),
    path('lab-bar-chart/', DashboardLabBarChart.as_view(), name='bar_chart_data'),
]
