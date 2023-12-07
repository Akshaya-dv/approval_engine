import json
from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from approval_engine.constants import POST_PARAMETER_CHECK
from approval_engine.applier import Applier
from approval_engine.approver import Approver
from gems.models import GemsApplication,GemsProjectGeneration


class ApplicantRequest(APIView):
    def post(self,request):
        try:
            body= request if isinstance(request,dict) else json.loads(request.body)
            return_object={}
            
            if  body.get('projectId') and body.get('attachment') and all(key in body for key in POST_PARAMETER_CHECK):
                projectData = list(GemsProjectGeneration.objects.filter(pgId=body.get('projectId')).values('pgId'))
                if(projectData):
                    approvalId=Applier.post(request)['result']
                    insert_gemsApplication(body.get('empId'),body.get('projectId'),body.get('requestRaisedDatetime'),body.get('attachment'),body.get('status'),approvalId)
                    return_object={
                        "status":200,
                        "message":"Inserted successfully"
                    }  
                else:
                    return_object={
                        "status":400,
                        "message":"Their is no project with corresponding projectId "
                    }  

                
            else:
                return_object={
                "status":400,
                "message":"invalid request body"
                }    
                return JsonResponse(return_object)
        except (Exception) as error:
            print("Project generation post issue is ------->"+str(error))
            return_object={
                "status":500,
                "message":"Internal server error issue is "+str(error)
            }
        return JsonResponse(return_object)
    
    def get(self,request):
        try:
            body=request if isinstance(request,dict) else json.loads(request.body)
            return_object={}
            if body.get('empId') and body.get('flowName'):
                approvaldata=Applier.get(request)
                
                gemsApplicationData=get_gemsApplication(body.get('empId'))
                data_dict={}
                for data in gemsApplicationData:
                    data_dict[data['approvalEngUniqueID_id']]=data
                for data in approvaldata:
                    data['applicantion_data']=data_dict.get(data['approvalEngUniqueID']) if data_dict.get(data['approvalEngUniqueID']) else ""
                    # gemsApplicationDatadict=dict(data)
                  
                return_object={
                        "status":200,
                        "message": 'Gems Application data retrieved successfully',
                        "result":approvaldata
                    }
                return JsonResponse(return_object)
            else:
                return_object={
                "status":400,
                "message":"invalid request body"
                }    
                return JsonResponse(return_object)

        except (Exception) as error:
            print("Project generation post issue is ------->"+str(error))
            return_object={
                "status":500,
                "message":"Internal server error issue is "+str(error)
            }

class Application_approver(APIView):
    def put(self,request):
        try:
            request= request if isinstance(request,dict) else json.loads(request.body)
            return_obj={}
            return_obj=Approver.put(request)
            if request.get('applicantionRequestID')  and request.get('attachment'):
                GemsApplication.objects.filter(applicantion_request_ID=request.get('applicantionRequestID')).update(attachment=request.get('attachment'))
            
            return return_obj
        except (Exception) as error:
            print("-------->approver-put",str(error))
            return JsonResponse(return_obj)
        
    def get(self,request):
        try:
            request= request if isinstance(request,dict) else json.loads(request.body)
            return_obj={}
            return_obj=Approver.get(request)
            return return_obj
        except (Exception) as error:
            print("-------->approver-get",str(error))
            return JsonResponse(return_obj)
                


def insert_gemsApplication(ApplicantId,ProjectId,Request_raised_datetime,Attachment,Status,ApprovalEngUniqueID):
    data=GemsApplication(applicantId=ApplicantId,projectId_id=ProjectId,request_raised_datetime=Request_raised_datetime,attachment=Attachment,status=Status,approvalEngUniqueID_id=ApprovalEngUniqueID,isDeleted=False)
    data.save()


def get_gemsApplication(EmpId):
        applicationData = list(GemsApplication.objects.filter(applicantId=EmpId).values())
        return applicationData