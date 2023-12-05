import json
from rest_framework.views import APIView
from django.http import JsonResponse
from django.db import connection
from approval_engine.models import ApprovalFlow,ApprovalFlowHirarchies

class FlowName(APIView):
    def get(self,request):
        try:
            request = request if isinstance(request,dict) else json.loads(request.body)
            return_object={}
            if request.get('flowName'):
                flow=list(ApprovalFlow.objects.filter(approvalFlowName=request.get('flowName')).values())
                return_object={
                    "status":200,
                    "message":"flowname retrieved successfully",
                    "result":flow
                }
            else:
                flow=list(ApprovalFlow.objects.all().values())
                return_object={
                    "status":200,
                    "message":"flowname retrieved successfully",
                    "result":flow
                }
                
        except (Exception) as error:
            print("Flowname get api issue is "+str(error))
            return_object={
                "status":500,
                "message":"Internal server error "+str(error),
            }
        return JsonResponse(return_object)
                
    def post(self,request):
        try:
            request = request if isinstance(request,dict) else json.loads(request.body)
            return_object={}
            if request.get('flowName'):
                flow_exist=ApprovalFlow.objects.filter(approvalFlowName=request.get('flowName')).values()
                if flow_exist:
                    return_object={
                    "status":200,
                    "message":"flowname already exist"
                }    
                else:
                    ApprovalFlow(approvalFlowName=request.get('flowName')).save()
                    return_object={
                    "status":200,
                    "message":"flowname inserted successfully"
                }    
                    
            else:
                return_object={
                    "status":400,
                    "message":"Invalid request body"
                }    
        except (Exception) as error:
            print("Flow Name insertion issue "+str(error))
            return_object={
                "status":500,
                "message":"Issue is "+str(error)
            }
        return JsonResponse(return_object)

class Herarchy(APIView):
    def get(self,request):
        try:
            request = request if isinstance(request,dict) else json.loads(request.body)
            return_object={} 
            if request.get('flowName'):
                flow_id=ApprovalFlow.objects.filter(approvalFlowName=request.get('flowName')).values_list('approvalFlowId').first()
                hirarchy= list(ApprovalFlowHirarchies.objects.filter(approvalFlowId=flow_id[0]).values())
                return_object={
                    "status":200,
                    "message":"flowname inserted successfully",
                    "result":hirarchy
                }    
            else:
                return_object={
                    "status":400,
                    "message":"Invalid request body"
                }    
                
        except (Exception) as error:
            print("Flow Name insertion issue "+str(error))
            return_object={
                "status":500,
                "message":"Issue is "+str(error)
            }
        return JsonResponse(return_object)
    def post(self,request):
        try:
            request = request if isinstance(request,dict) else json.loads(request.body)
            return_object={} 
            if request.get('hirarchy') and len(request.get('hirarchy'))>0 and request.get('flowName'):
                flow_id=ApprovalFlow.objects.filter(approvalFlowName=request.get('flowName')).values_list('approvalFlowId').first()[0]
                if flow_id or flow_id==0:
                    for hirarchy in request.get('hirarchy'):
                        if hirarchy.get('empId') and hirarchy.get('hirarchy'):
                            ApprovalFlowHirarchies(empId=request.get('empId'),hirarchy=request.get('hirarchy'),approvalFlowId=flow_id)
                            ApprovalFlowHirarchies.save()
                            return_object={
                            "status":200,
                            "message":"FLow inserted successfully"
                            }
                else:
                    return_object={
                        "status":200,
                        "message":"FLow doesn't exist"
                    }
            else:
                return_object={
                        "status":400,
                        "message":"Invalid request body"
                    }
        except (Exception) as error:
            print("Hirarchy post method issue is "+str(error))
            return_object={
                        "status":500,
                        "message":"Internal server error"
                    }
        return JsonResponse(return_object)
    
    def put(self,request):
        try:
            request = request if isinstance(request,dict) else json.loads(request.body)
            return_object={} 
            if request.get('flowName') and request.get('empId') and request.get('hirarchy'):
                flow_id=ApprovalFlow.objects.filter(approvalFlowName=request.get('flowName')).values_list('approvalFlowId').first()
                
                ApprovalFlowHirarchies.objects.filter(approvalFlowId=flow_id[0],hirarchy=request.get('hirarchy')).update(empId=request.get('empId'))
                return_object={
                    "status":200,
                    "message":"flowname updated successfully"
                }
            
        except (Exception) as error:
            print("Flow Name insertion issue "+str(error))
            return_object={
                "status":500,
                "message":"Issue is "+str(error)
            }
        return JsonResponse(return_object)
    