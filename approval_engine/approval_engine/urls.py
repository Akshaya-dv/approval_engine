"""
URL configuration for approval_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from .flow_hirarchy import FlowName,Hirarchy
from .approval_flow_status import ApprovalFlowStatus
from .applier import Applier
from .approver import Approver


urlpatterns = [
    # path('applicant',Applier.as_view()),
    # path('approver',Approver.as_view()),
    
    path('flow',FlowName.as_view()),
    path('flow_hirarchy',Hirarchy.as_view()) ,
    path('approval_flow_status',ApprovalFlowStatus.as_view()),
    path('sep/',include('e_sep.urls')),
    path('leave/',include('e_leave.urls')),
    path('gems/',include('gems.urls')),

 
]
