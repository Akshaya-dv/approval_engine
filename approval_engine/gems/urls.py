from django.urls import path
from .views import ProjectGeneration

urlpatterns = [
   

   path('project-generate/',ProjectGeneration.as_view(), name='EmployeeLeaves'),   
    
]