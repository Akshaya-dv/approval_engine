from django.urls import path
from .views import ProjectGeneration
from .applicant_views import ApplicantRequest,Application_approver

urlpatterns = [
   

#    path('apply-gemspg/',ProjectGeneration.as_view(), name='gemsProjectgeneration'),   
#    path('gemspg-approver/',ProjectGeneration.as_view(), name='gemsProjectgeneration'),   
   path('apply-gemsapplication/',ApplicantRequest.as_view(), name='EmployeeLeaves'),  
    path('gemsapplication-approver/',Application_approver.as_view(), name='EmployeeLeaves'),    
    
]