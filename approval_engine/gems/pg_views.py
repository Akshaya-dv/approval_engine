import json
from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from approval_engine.applier import Applier
from approval_engine.approver import Approver
from approval_engine.models import ApprovalEngMasterData
from approval_engine.constants import POST_PARAMETER_CHECK
from gems.models import GemsProjectGeneration
 
class ProjectGeneration(APIView):
    def post(self,request):
        try:
            request1= request if isinstance(request,dict) else json.loads(request.body)
            return_object={}
            if request1.get('pgtitle') and request1.get('pgdescription') and request1.get('skills') and all(key in request1 for key in POST_PARAMETER_CHECK):
                approvaldata=Applier.post(request)
                if 'result' not in approvaldata.keys():
                    return_object=approvaldata
                else:     
                    approvalId = Applier.post(request)['result']
                    GemsProjectGeneration(pgTitle=request1.get('pgtitle'),pgDescription=request1.get('pgdescription'),skils=request1.get('skills'),created_by=request1.get('empId'),approvalEngUniqueID_id=approvalId).save()
                    return_object = {
                        "status":200,
                        "message":"Project generated successfully"
                    }
                
            else:
                return_object={
                    "status":400,
                    "message":"Invalid request body"
                }
        except (Exception) as error:
            print("Project generation post issue is ------->"+str(error))
            return_object={
                "status":500,
                "message":"Internal server error issue is "+str(error)
            }
        return JsonResponse(return_object)
    def get(self,request):
        try:
            request1= request if isinstance(request,dict) else json.loads(request.body)
            return_object={}
            if request1.get('empId') and request1.get('flowName'):
                project_data=list(GemsProjectGeneration.objects.filter(created_by=request1.get('empId')).values())
                project_status = Applier.get(request)['result']
                project_data_dict={}
                for approvalEngUniqueID_id_data in project_data:
                    project_data_dict[approvalEngUniqueID_id_data['approvalEngUniqueID_id']]=approvalEngUniqueID_id_data
                
                for data in project_status:
                    data['project_status']=project_data_dict[data['approvalEngUniqueID']] if project_data_dict.get(data.get('approvalEngUniqueID')) else ""
                return_object={
                    "status":200,
                    "message":"Data retrieved successfully",
                    "result":{
                        "project_details":project_status
                    }
                }
            else:
                return_object={
                    "status":400,
                    "message":"Invalid request body"
                }
        except (Exception) as error:
            print("Project generation post issue is ------->"+str(error))
            return_object={
                "status":500,
                "message":"Internal server error issue is "+str(error)
            }
        return JsonResponse(return_object)

    
class ProjectApprover(APIView):        
    def put(self,request):
        try:
            request1= request if isinstance(request,dict) else json.loads(request.body)
            return_object={}
            if request1.get('pgtitle') and request1.get('approvalEngUniqueID_id') and request1.get('pgId') and request1.get('pgdescription') and request1.get('skills'):
                return_object=Approver.put(request)
                GemsProjectGeneration.objects.filter(pgId=request1.get('pgId')).update(pgTitle=request1.get('pgtitle'),pgDescription=request1.get('pgdescription'),skils=request1.get('skills'),created_by=request1.get('empId'))
                return return_object
            else:
                return_object={
                    "status":400,
                    "message":"Invalid request body"
                }
                
        except (Exception) as error:
            print("Project generation post issue is ------->"+str(error))
            return_object={
                "status":500,
                "message":"Internal server error issue is "+str(error)
            }
        return JsonResponse(return_object)

    def get(self,request):
        try:
            request= request if isinstance(request,dict) else json.loads(request.body)
            return_obj={}
            return_obj=Approver.get(request)
            return return_obj
        except (Exception) as error:
            print("-------->Pg-approver-get",str(error))
            return JsonResponse(return_obj)
    
            
 