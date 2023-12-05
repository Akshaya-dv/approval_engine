from django.urls import path
from .views import ApplyLeaves,Leave_approver

urlpatterns = [
   
    path('applyleaves/',ApplyLeaves.as_view(), name='EmployeeLeaves'),    
    path('leave-approver/',Leave_approver.as_view(), name='EmployeeLeaves'),    
]