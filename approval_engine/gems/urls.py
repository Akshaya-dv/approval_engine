from django.urls import path
from .views import ProjectGeneration,ProjectApprover

urlpatterns = [
   

   path('project-generate/',ProjectGeneration.as_view(), name='EmployeeLeaves'),   
   path('project-approver/',ProjectApprover.as_view(), name='EmployeeLeaves'),   
    
]