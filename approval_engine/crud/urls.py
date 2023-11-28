from django.urls import path
from .views import empLeave

urlpatterns = [
   
    path('empleaves',empLeave.as_view(), name='EmployeeLeaves'),

      
]