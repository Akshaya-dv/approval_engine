from django.urls import path

from .views import ProjectGeneration,ProjectApprover
from .applicant_views import ApplicantRequest,Application_approver


urlpatterns = [
   

   path('project-generate/',ProjectGeneration.as_view(), name='EmployeeLeaves'),   
   path('project-approver/',ProjectApprover.as_view(), name='EmployeeLeaves'),   
   path('apply-gemsapplication/',ApplicantRequest.as_view(), name='EmployeeLeaves'),  
   path('gemsapplication-approver/',Application_approver.as_view(), name='EmployeeLeaves'),    

    
]