import datetime
import json
from django.shortcuts import render
from approval_engine.constants import *
from approval_engine.applier import Applier
from approval_engine.approver import Approver
from rest_framework.views import APIView
from django.http import JsonResponse
from django.db import connection
from approval_engine.common_function import formating_response
from .models import EmpLeave
# Create your views here.

class ApplyLeaves(APIView):
    def post(self,request):
            try:
                
                data = request if isinstance(request,dict) else json.loads(request.body)
                return_object={}
                if not all(key in data for key in POST_PARAMETER_CHECK):
                    return_object={
                    "status":400,
                    "message":"invalid request body"
                    }    
                    return JsonResponse(return_object)
                
                EmpId = data.get('empId')
                RequestRaisedDatetime = data.get('requestRaisedDatetime')
                FlowName = data.get('flowName')
                ActionDatetime =data.get('actionDatetime')
                RequestRaisedDatetime = data.get('requestRaisedDatetime')
                FlowName = data.get('flowName')
                ActionDatetime =data.get('actionDatetime')

                approvalEngUniqueId=Applier.post(request)['result']
                
                if FlowName=='leave':
                  insert_empLeave(EmpId,'[{}]',RequestRaisedDatetime,ActionDatetime,approvalEngUniqueId)
                  return_object={
                    "status":200,
                    "message": 'Leave submitted successfully',
                    
                    }
                  return JsonResponse(return_object)
            except json.JSONDecodeError as error:
                print("-----------leave-post issue is ",str(error))
                return_object={
                    "status":500,
                    'message': 'Issue is '+str(error)
                }
                return JsonResponse(return_object)
               
    def delete(self,request):
        try:
            return_object={}
            request = request if isinstance(request,dict) else json.loads(request.body)
            return_object = Applier.delete(request)
        except:
            return_object={
                        "status":400,
                        "message":"Invalid Request Body"
                    }
        return JsonResponse(return_object)
    

    def get(self, request):
        try:
            data = request if isinstance(request,dict) else json.loads(request.body)
            return_obj={}
            EmpId=data.get('empId')
            approvaldata=Applier.get(request)
            
            leaveData=get_empLeave(EmpId)
            return_obj={
                "status":200,
                "message":"Data retrieved successfully",
                "result":{'LeaveData':leaveData,"ApprovalData":approvaldata}
            }
            
        except json.JSONDecodeError as error:
            return_obj={
                "status":200,
                "message":"Internal error "+str(error),
            }
            
        return JsonResponse(return_obj)


def insert_empLeave(EmpId,PendingActionFrom,RequestRaisedDatetime,ActionDatetime,ApprovalEngUniqueID):
    data = EmpLeave(empId=EmpId, pendingActionFrom=PendingActionFrom, requestRaisedDatetime=RequestRaisedDatetime,actionDatetime= ActionDatetime,approvalEngUniqueID_id = ApprovalEngUniqueID)
    data.save()


def get_empLeave(EmpId):
        employeeleave = list(EmpLeave.objects.filter(empId=EmpId).values())
        return employeeleave


class Leave_approver(APIView):
    def put(self,request):
        try:
            request= request if isinstance(request,dict) else json.loads(request.body)
            return_obj={}
            return_obj=Approver.put(request)
            return return_obj
        except (Exception) as error:
            print("-------->leave-approver-put",str(error))
            return JsonResponse(return_obj)
        
    def get(self,request):
        try:
            request= request if isinstance(request,dict) else json.loads(request.body)
            return_obj={}
            return_obj=Approver.get(request)
            return return_obj
        except (Exception) as error:
            print("-------->leave-approver-get",str(error))
            return JsonResponse(return_obj)
            
            
         
            
