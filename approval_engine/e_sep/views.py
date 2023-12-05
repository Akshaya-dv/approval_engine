import datetime
import json
from django.http import JsonResponse
from approval_engine.constants import POST_PARAMETER_CHECK
from approval_engine.approver import Approver
from e_sep.models import EmpSep
from rest_framework.views import APIView
from approval_engine.applier import Applier


# Create your views here.
class Empsep1(APIView):
    def post(self,request):
            try:
                data = request if isinstance(request,dict) else json.loads(request.body)
                return_object = {}
                EmpId = data.get('empId')
                if not all(key in data for key in POST_PARAMETER_CHECK):
                    return_object={
                    "status":400,
                    "message":"invalid request body"
                    }    
                    return JsonResponse(return_object)
        

                approvalId=0

                RequestRaisedDatetime = data.get('requestRaisedDatetime')
                PositionCode=data.get('positionCode')
                RequestRaisedBy=data.get('requestRaisedBy')
                ActualRequestDatetime=data.get('actualRequestDatetime')
                LWDPerPolicy=data.get('lwdPerPolicy')
                LWDRequested=data.get('lwdRequested')
                NPDays=data.get('npDays')
                NPShortfallDays=data.get('npShortfallDays')
                RecoveryAmount=data.get('recoveryAmount')
                ShortfallDays=data.get('shortfallDays')
                tataGrpJoiningDate=data.get('tataGrpJoiningDate')
                TmlGrpJoiningDate =data.get('tmlGrpJoiningDate')
                IsPosted=data.get('IsPosted')
                Attachment=data.get('attachment')

                approvalId = Applier.post(request)['result']
                
                insert_ESep(EmpId,PositionCode,RequestRaisedBy,RequestRaisedDatetime,ActualRequestDatetime,LWDPerPolicy,LWDRequested,NPDays,
                NPShortfallDays,'[{}]',RecoveryAmount,ShortfallDays,tataGrpJoiningDate,TmlGrpJoiningDate ,
                IsPosted,Attachment,approvalId)
                return_object={
                    "status":200,
                    "message": 'E-sep submitted successfully',
                    }
            except json.JSONDecodeError as error:
                return_object={
                    "status":500,
                    "message": 'Internal Error '+str(error),
                    }
            return JsonResponse(return_object)

    def get(self, request):
            try:
                data = request if isinstance(request,dict) else json.loads(request.body)
                return_object={}
                if data.get('empId') and data.get('flowName'):
                    EmpId=data.get('empId')
                    
                    approvaldata=Applier.get(request)
                    
                    eSepData=get_empSep(EmpId)
                    
                    return_object={
                        "status":200,
                        "message": 'E-sep data retrieved successfully',
                        "result":{'E-sep-Data':eSepData,"ApprovalData":approvaldata}
                    }
                else:
                    return_object={
                        "status":400,
                        "message": "Invalid request body"
                            }
            except json.JSONDecodeError as error:
                return_object={
                    "status":500,
                    "message": "Internal error "+str(error)
                }
            return JsonResponse(return_object)
            
    
def insert_ESep(EmpId,PositionCode,RequestRaisedBy,RequestRaisedDatetime,ActualRequestDatetime,LWDPerPolicy,LWDRequested,NPDays,
                NPShortfallDays,PendingActionFrom,RecoveryAmount,ShortfallDays,tataGrpJoiningDate,TmlGrpJoiningDate ,
                IsPosted,Attachment,ApprovalEngUniqueID):
 
    data = EmpSep(empId=EmpId,position_code=PositionCode,request_raised_by=RequestRaisedBy,request_raised_datetime=RequestRaisedDatetime,actual_request_datetime=ActualRequestDatetime,lwd_per_policy=LWDPerPolicy,lwd_requested =LWDRequested,np_days=NPDays ,np_shortfall_days=NPShortfallDays ,pending_action_from=PendingActionFrom,isDeleted=False,recovery_amount=RecoveryAmount,shortfall_days=ShortfallDays ,tataGrp_joining_date=tataGrpJoiningDate ,tmlGrp_joining_date=TmlGrpJoiningDate ,isPosted=IsPosted,attachment=Attachment ,approvalEngUniqueID_id=ApprovalEngUniqueID)
    data.save()
    
def get_empSep(EmpId):
        employeeseparation = list(EmpSep.objects.filter(empId=EmpId).values())
        return employeeseparation



class sep_approver(APIView):
    def put(self,request):
        try:
            request= request if isinstance(request,dict) else json.loads(request.body)
            return_obj={}
            return_obj=Approver.put(request)
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
            