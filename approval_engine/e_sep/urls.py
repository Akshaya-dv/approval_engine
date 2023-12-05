from django.urls import path
from .views import Empsep1,sep_approver

urlpatterns = [
   

   path('apply-sep/',Empsep1.as_view(), name='EmployeeLeaves'),   
    path('sep-approver/',sep_approver.as_view(), name='EmployeeLeaves'),    
    
]