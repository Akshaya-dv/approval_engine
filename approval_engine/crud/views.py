
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.views import APIView
from django.db import connection
import json
import datetime
from .models import  ApprovalEngMasterData,ApprovalFlow,ApprovalFlowHirarchies
from .leaveModel_to_be_deleted import EmpLeave
from .e_sepModel_to_be_deleted import EmpSep
from .serializer import EmpSeparation,EmpLeaveSerializer,ApprovalEngMasterDataSerializer,ApprovalFlow,ApprovalFlowHirarchies
from rest_framework import status
import psycopg2
from psycopg2.extras import Json




# Create your views here.
class empLeave(APIView):
    def post(self,request):
        if 'application/json' in request.content_type:
            try:
                data = json.loads(request.body.decode('utf-8'))
                EmpId = data.get('empId')

                RequestRaisedDatetime = data.get('requestRaisedDatetime', None)
                FlowName = data.get('flowName',None)
                Description =data.get('description',None)
                ActionDatetime =data.get('actionDatetime',None)
                status =data.get('status',None)
                approvalReason=data.get('approvalReason',None)
                rejectionReason=data.get('rejectionReason',None)
                justification =data.get('justification',None)
                comment =data.get('comment',None)
                remark=data.get('remark',None)
                approvalId=0

                PositionCode=data.get('positionCode',None)
                RequestRaisedBy=data.get('requestRaisedBy',None)
                ActualRequestDatetime=data.get('actualRequestDatetime',None)
                LWDPerPolicy=data.get('lwdPerPolicy',None)
                LWDRequested=data.get('lwdRequested',None)
                NPDays=data.get('npDays',None)
                NPShortfallDays=data.get('npShortfallDays',None)
                RecoveryAmount=data.get('recoveryAmount',None)
                ShortfallDays=data.get('shortfallDays',None)
                tataGrpJoiningDate=data.get('tataGrpJoiningDate',None)
                TmlGrpJoiningDate =data.get('tmlGrpJoiningDate',None)
                IsPosted=data.get('IsPosted',None)
                Attachment=data.get('attachment',None)

                LatestUpdateDate =datetime.datetime.now()

                with connection.cursor() as cursor:
                    try:
                        print(LatestUpdateDate, FlowName, EmpId, RequestRaisedDatetime, ActionDatetime, status,approvalReason,rejectionReason,Description,justification ,comment, remark,approvalId)
                        cursor.execute('CALL public.post_approvaldata(%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s)', [ LatestUpdateDate, FlowName, EmpId, RequestRaisedDatetime, ActionDatetime, status,approvalReason,rejectionReason,Description,justification ,comment, remark,approvalId])
                        results = cursor.fetchall()
                    finally:
                        cursor.close()
                        for item in results:
                            approvalId = item[0]
                if FlowName=='LeaveApproval':
                  insert_empLeave(EmpId,'[{}]',RequestRaisedDatetime,ActionDatetime,approvalId)
                  return JsonResponse({'message': 'Data processed successfully'})
                elif FlowName=='E-sep':
                  insert_ESep(EmpId,PositionCode,RequestRaisedBy,RequestRaisedDatetime,ActualRequestDatetime,LWDPerPolicy,LWDRequested,NPDays,
                NPShortfallDays,'[{}]',RecoveryAmount,ShortfallDays,tataGrpJoiningDate,TmlGrpJoiningDate ,
                IsPosted,Attachment,approvalId)
                  return JsonResponse({'message': 'Data processed successfully'})
            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'Invalid JSON format'}, status=400)
#                 StatusArr =[{'ActionBy':EmpId,'status':status,'date':LatestUpdateDate.isoformat()}]
#                 ApprovalReasonArr =[{'ActionBy':EmpId,'approvalReason':'na','date':LatestUpdateDate.isoformat()}]
#                 RejectionReasonArr=[{'ActionBy':EmpId,'rejectionReason':'na','date':LatestUpdateDate.isoformat()}]
#                 DescriptionArr=[{'ActionBy':EmpId,'description':Description,'date':LatestUpdateDate.isoformat()}]
#                 JustificationArr =[{'ActionBy':EmpId,'justification':'na','date':LatestUpdateDate.isoformat()}]
#                 RemarksArr =[{'ActionBy':EmpId,'remark':'na','date':LatestUpdateDate.isoformat()}]
#                 CommentsArr =[{'ActionBy':EmpId,'comment':'na','date':LatestUpdateDate.isoformat()}]
#             #  getting approval flow id from approval flow
#                 approvalFlowId=ApprovalFlow.objects.filter(approvalFlowName=FlowName).values_list('approvalFlowId')
#             #  getting the approval hirarchy form hirarchy table
#                 approvalHirarchies=list(ApprovalFlowHirarchies.objects.filter( approvalFlowId=approvalFlowId[0][0]).values( 'empId','hirarchy'))
#                 sortedApprovalHirarchies=sorted(approvalHirarchies, key=lambda x: x['hirarchy'])
#                 print(sortedApprovalHirarchies)
#                 for i in sortedApprovalHirarchies:
#                     Statusobj={'ActionBy':i['empId'],'status':'ApprovalPending','date':'na'}
#                     StatusArr.append(Statusobj)
#                     ApprovalReasonobj={'ActionBy':i['empId'],'approvalReason':'na','date':'na'}
#                     ApprovalReasonArr.append(ApprovalReasonobj)
#                     RejectionReasonobj={'ActionBy':EmpId,'rejectionReason':'na','date':'na'}
#                     RejectionReasonArr.append(RejectionReasonobj)
#                     Descriptionobj={'ActionBy':i['empId'],'description':'na','date':'na'}
#                     DescriptionArr.append(Descriptionobj)
#                     Justificationobj ={'ActionBy':i['empId'],'justification':'na','date':'na'}
#                     JustificationArr.append(Justificationobj)
#                     Remarksobj ={'ActionBy':i['empId'],'remark':'na','date':'na'}
#                     RemarksArr.append(Remarksobj)
#                     Commentsobj ={'ActionBy':i['empId'],'comment':'na','date':'na'}
#                     CommentsArr.append(Commentsobj)
                

#                 PendingActionFrom = sortedApprovalHirarchies[0]
#                 approvalId=0
# # stored procedure
                # ApprovalEngMasterData_record = ApprovalEngMasterData.objects.create(status=StatusArr,approvalReason=ApprovalReasonArr,rejectionReason=RejectionReasonArr,description=DescriptionArr,justification=JustificationArr,remarks=RemarksArr,comments=CommentsArr,latestUpdateDate=LatestUpdateDate,flowName=FlowName)
                # ApprovalEngUniqueID = ApprovalEngMasterData.objects.get(pk=ApprovalEngMasterData_record.pk)
                # # flow name condition
               
    

    def get(self, request):
        if 'application/json' in request.content_type:
            try:
                data = json.loads(request.body.decode('utf-8'))
                EmpId=data.get('empId')
                FlowName=data.get('flowName')
                with connection.cursor() as cursor:
                    cursor.execute("BEGIN;")
                    # Call the stored procedure
                    cursor.execute(' CALL get_approvaldata(%s,%s); ',[EmpId,FlowName])
                    # Fetch all from the result cursor
                    cursor.execute('FETCH ALL FROM "rs_approvaldata";')
                    approvaldata = cursor.fetchall()
                    # Commit the transaction
                    cursor.execute("COMMIT;")
                   # Fetch the results from the result_cursor
                    # employeeleave = EmpLeave.objects.filter(empId=EmpId)
                    # empLeavedataserializer = EmpLeaveSerializer(employeeleave, many=True)
                    # approvaldataserializer = ApprovalEngMasterDataSerializer(approvaldata, many=True)
                    # print(approvaldataserializer)
                    formatedApprovalData=[]
                    print(approvaldata) 
                    for data in approvaldata:
                        objFormatedApprovalData={}
                        objFormatedApprovalData['approvalEngUniqueID']=data[0]
                        status=json.loads(data[1])
                       
                        approvalReason = json.loads(data[2])
                        rejectionReason=json.loads(data[3])
                        description =json.loads(data[4])
                        justification =json.loads(data[5])
                        remarks =json.loads(data[6])
                        comments =json.loads(data[7])
                        objFormatedApprovalData['latestUpdateDate'] =data[8]
                        objFormatedApprovalData['flow']=data[9]
                        objFormatedApprovalData['isDeleted']=data[10]
                        
                        for i in range(len(status)):
                            print(status[i]['Actionby'])
                            objFormatedApprovalData[status[i]['Actionby']]={
                                "level":status[i]['level'],
                                "status": status[i]['status'],
                                "statusUpdatedDate":status[i]['date'],
                                "approvalReason":approvalReason[i]['approvalReason'],
                                "approvalReasonUpdatedDate":approvalReason[i]['date'],
                                "rejectionReason":rejectionReason[i]['rejectionReason'],
                                "rejectionReasonUpdatedDate":rejectionReason[i]['date'],
                                "description":description[i]['description'],
                                "descriptionUpdatedDate":description[i]['date'],
                                "justification":justification[i]['justification'],
                                "justificationUpdatedDate":justification[i]['date'],
                                "remarks":remarks[i]['remark'],
                                "remarksUpdatedDate":remarks[i]['date'],
                                "comments":comments[i]['comment'],
                                "commentsUpdatedDate":comments[i]['date'],
                            }
                        formatedApprovalData.append(objFormatedApprovalData)
                if FlowName=='LeaveApproval':
                  leaveData=get_empLeave(EmpId)
                  return JsonResponse({'LeaveData':leaveData,"ApprovalData":formatedApprovalData})
                elif FlowName=='E-sep':
                  separationData=get_empSep(EmpId)
                  return JsonResponse({'SeparationData':separationData,"ApprovalData":formatedApprovalData})
            except json.JSONDecodeError as e:
                return JsonResponse({'error': e}, status=400)
        
        
        
        
        
        # employeeleave = EmpLeave.objects.filter(empId=EmpId)
        # empLeavedataserializer = EmpLeaveSerializer(employeeleave, many=True)
        # approvaldata = ApprovalEngMasterData.objects.all()
        # approvaldataserializer = ApprovalEngMasterDataSerializer(approvaldata, many=True)
        # # Organize approval data into a dictionary for easy access
        # approval_data_dict = {entry['approvalEngUniqueID']: entry for entry in approvaldataserializer.data}
        # # Combine data based on the common field (approvalid)
        # combined_data = []
        # for emp_leave_entry in empLeavedataserializer.data:
        #     approval_id = emp_leave_entry.get('approvalEngUniqueID')
        #     approval_data = approval_data_dict.get(approval_id)
        #     # print(type(emp_leave_entry))
        #     emp_leave_entry['status']=approval_data['status']
        #     emp_leave_entry['approvalReason']=approval_data['approvalReason']
        #     emp_leave_entry['rejectionReason']=approval_data['rejectionReason']
        #     emp_leave_entry['description']=approval_data['description']
        #     emp_leave_entry['justification']=approval_data['justification']
        #     emp_leave_entry['remarks']=approval_data['remarks']
        #     emp_leave_entry['comments']=approval_data['comments']
        
        #     combined_data.append(emp_leave_entry)
        # return Response(approvaldataserializer)


       


def insert_empLeave(EmpId,PendingActionFrom,RequestRaisedDatetime,ActionDatetime,ApprovalEngUniqueID):
    data = EmpLeave(empId=EmpId, pendingActionFrom=PendingActionFrom, requestRaisedDatetime=RequestRaisedDatetime,actionDatetime= ActionDatetime,approvalEngUniqueID_id = ApprovalEngUniqueID)
    data.save()
def insert_ESep(EmpId,PositionCode,RequestRaisedBy,RequestRaisedDatetime,ActualRequestDatetime,LWDPerPolicy,LWDRequested,NPDays,
                NPShortfallDays,PendingActionFrom,RecoveryAmount,ShortfallDays,tataGrpJoiningDate,TmlGrpJoiningDate ,
                IsPosted,Attachment,ApprovalEngUniqueID):
    data = EmpSep(empId=EmpId,position_code=PositionCode,request_raised_by=RequestRaisedBy,request_raised_datetime=RequestRaisedDatetime,actual_request_datetime=ActualRequestDatetime,lwd_per_policy=LWDPerPolicy,lwd_requested =LWDRequested,np_days=NPDays ,np_shortfall_days=NPShortfallDays ,pending_action_from=PendingActionFrom,isDeleted=False,recovery_amount=RecoveryAmount,shortfall_days=ShortfallDays ,tataGrp_joining_date=tataGrpJoiningDate ,tmlGrp_joining_date=TmlGrpJoiningDate ,isPosted=IsPosted,attachment=Attachment ,approvalEngUniqueID_id=ApprovalEngUniqueID)
    data.save()

def get_empLeave(EmpId):
        employeeleave = EmpLeave.objects.filter(empId=EmpId)
        empLeavedataserializer = EmpLeaveSerializer(employeeleave, many=True)
        return empLeavedataserializer.data

def get_empSep(EmpId):
        employeeseparation = EmpSep.objects.filter(empId=EmpId)
        empSepdataserializer = EmpSeparation(employeeseparation, many=True)
        return empSepdataserializer.data










