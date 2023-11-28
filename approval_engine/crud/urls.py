from django.urls import path
from .views import empLeave,LeaveApprovalStatus

urlpatterns = [
   
    path('empleaves',empLeave.as_view(), name='EmployeeLeaves'),
    path('leaveapproval',LeaveApprovalStatus.as_view(), name='LeaveApprovalStatus'),
    

      
]