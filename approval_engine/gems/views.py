import json
from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from approval_engine.applier import Applier
from gems.models import GemProjectGeneration
 
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
            request= request if isinstance(request,dict) else json.loads(request.body)
            return_object={}
            if request.get('pgtitle') and request.get('pgdescription') and request.get('skills'):
                approvalId = Applier.post(request)['result']
                
                GemProjectGeneration(pgTitle=request.get('pgtitle'),pgDescription=request.get('pgdescription'),skills=request.get('skills'))
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
            return_object={}
            
            pass
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
            
 