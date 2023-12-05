import json
from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from approval_engine.applier import Applier
from approval_engine.models import ApprovalEngMasterData
from approval_engine.constants import POST_PARAMETER_CHECK
from gems.models import GemsProjectGeneration
 
# Create your views here.
 
# class ApprovalEngMasterData(models.Model):
#     approvalEngUniqueID =models.AutoField(primary_key=True)
#     status=JSONField()
#     approvalReason = JSONField()
#     rejectionReason=JSONField()
#     description =JSONField()
#     justification =JSONField()
#     remarks =JSONField()
#     comments =JSONField()
#     latestUpdateDate =models.DateTimeField(max_length=255)
#     flow=models.ForeignKey(ApprovalFlow,null=False,on_delete=models.CASCADE)
#     isDeleted=models.BooleanField(default=False)
#     class Meta:
#         db_table="ApprovalEngMasterData"
 
class ProjectGeneration(APIView):
    def post(self,request):
        try:
            request1= request if isinstance(request,dict) else json.loads(request.body)
            return_object={}
            if request1.get('pgtitle') and request1.get('pgdescription') and request1.get('skills') and all(key in request1 for key in POST_PARAMETER_CHECK):
                print("0000000000")
                approvalId = Applier.post(request)['result']
                print(type(approvalId))
                GemsProjectGeneration(pgTitle=request1.get('pgtitle'),pgDescription=request1.get('pgdescription'),skils=request1.get('skills'),created_by=request1.get('empId'),approvalEngUniqueID_id=approvalId).save()
                
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
                project_status = Applier.get(request)
                return_object={
                    "status":200,
                    "message":"Data retrieved successfully",
                    "result":{
                        "project_details":project_data,
                        "project_status":project_status
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
    def put(self,request):
        try:
            request= request if isinstance(request,dict) else json.loads(request.body)
            return_object={}
            
            pass
        except (Exception) as error:
            print("Project generation post issue is ------->"+str(error))
            return_object={
                "status":500,
                "message":"Internal server error issue is "+str(error)
            }
        return JsonResponse(return_object)
            
 