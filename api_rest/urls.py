from django.urls import path
from .views import *

urlpatterns = [
    path('employee/', EmployeeView.as_view()),
    path('employee/<int:pk>/', EmployeeDetailView.as_view()),
    path('employee_logout/',EmployeeLogoutView.as_view()),
    path('employee_login/', EmployeeLoginView.as_view()),
    path('extra_services/', ExtraServicesView.as_view()),
    path('extra_services/add/', AddExtraServicesView.as_view()),
    path('department/', DepartmentView.as_view()),
    path('department/add/', AddDepartment.as_view()),
    path('department/id/',DepartmentViewById.as_view()),
    path('department/available/', MarkDepartmentAsAvailable.as_view()),
    path('department/add/maintenance/', AddDepartmentMaintenance.as_view()),
    path('department_inventory/', DepartmentInventoryView.as_view()),
    path('department_inventory/add/', AddDepartmentInventoryView.as_view()),
    path('all_communes/', CommuneView.as_view()),
    path('product/', ProductView.as_view()),
    path('product_type/', ProductTypeView.as_view()),
    path('product_by_category/', ProductViewByCategory.as_view()),
    path('not_available_dates/', getNotaVailableDates.as_view()),
    path('reservation/id/', ReservationByIdView.as_view()),
    path('reservation/status/', ReservationStatusView.as_view()),
    path('reservation/payment/', AddTransactionView.as_view()),
    path('reservation/', ReservationView.as_view()),
]
