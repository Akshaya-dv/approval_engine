from django.shortcuts import render, redirect,HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.views import APIView
import json
import datetime
from .models import EmpLeave, ApprovalEngMasterData,ApprovalFlow,ApprovalFlowHirarchies
from .serializer import EmpLeaveSerializer,ApprovalEngMasterDataSerializer,ApprovalFlow,ApprovalFlowHirarchies
from rest_framework import status


# Create your views here.
class empLeave(APIView):
    def post(self,request):
        if 'application/json' in request.content_type:
            try:
                data = json.loads(request.body.decode('utf-8'))
                EmpId = data.get('empId')
                LeaveRequestId = data.get('leaveRequestId', None)
                
                RequestRaisedDatetime = data.get('requestRaisedDatetime', None)
                FlowName = data.get('flowName',None)
                Description =data.get('description',None)
                ActionDatetime =data.get('actionDatetime',None)
                status =data.get('status',None)

                LatestUpdateDate =datetime.datetime.now()
                
                StatusArr =[{'ActionBy':EmpId,'status':status,'date':LatestUpdateDate.isoformat()}]
                ApprovalReasonArr =[{'ActionBy':EmpId,'approvalReason':'na','date':LatestUpdateDate.isoformat()}]
                RejectionReasonArr=[{'ActionBy':EmpId,'rejectionReason':'na','date':LatestUpdateDate.isoformat()}]
                DescriptionArr=[{'ActionBy':EmpId,'description':Description,'date':LatestUpdateDate.isoformat()}]
                JustificationArr =[{'ActionBy':EmpId,'justification':'na','date':LatestUpdateDate.isoformat()}]
                RemarksArr =[{'ActionBy':EmpId,'remark':'na','date':LatestUpdateDate.isoformat()}]
                CommentsArr =[{'ActionBy':EmpId,'comment':'na','date':LatestUpdateDate.isoformat()}]
            #  getting approval flow id from approval flow
                approvalFlowId=ApprovalFlow.objects.filter(approvalFlowName=FlowName).values_list('approvalFlowId')
            #  getting the approval hirarchy form hirarchy table
                approvalHirarchies=list(ApprovalFlowHirarchies.objects.filter( approvalFlowId=approvalFlowId[0][0]).values( 'empId','hirarchy'))
                sortedApprovalHirarchies=sorted(approvalHirarchies, key=lambda x: x['hirarchy'])
                print(sortedApprovalHirarchies)
                for i in sortedApprovalHirarchies:
                    Statusobj={'ActionBy':i['empId'],'status':'ApprovalPending','date':'na'}
                    StatusArr.append(Statusobj)
                    ApprovalReasonobj={'ActionBy':i['empId'],'approvalReason':'na','date':'na'}
                    ApprovalReasonArr.append(ApprovalReasonobj)
                    RejectionReasonobj={'ActionBy':EmpId,'rejectionReason':'na','date':'na'}
                    RejectionReasonArr.append(RejectionReasonobj)
                    Descriptionobj={'ActionBy':i['empId'],'description':'na','date':'na'}
                    DescriptionArr.append(Descriptionobj)
                    Justificationobj ={'ActionBy':i['empId'],'justification':'na','date':'na'}
                    JustificationArr.append(Justificationobj)
                    Remarksobj ={'ActionBy':i['empId'],'remark':'na','date':'na'}
                    RemarksArr.append(Remarksobj)
                    Commentsobj ={'ActionBy':i['empId'],'comment':'na','date':'na'}
                    CommentsArr.append(Commentsobj)
                

                PendingActionFrom = sortedApprovalHirarchies[0]
                ApprovalEngMasterData_record = ApprovalEngMasterData.objects.create(status=StatusArr,approvalReason=ApprovalReasonArr,rejectionReason=RejectionReasonArr,description=DescriptionArr,justification=JustificationArr,remarks=RemarksArr,comments=CommentsArr,latestUpdateDate=LatestUpdateDate,flowName=FlowName)
               
                ApprovalEngUniqueID = ApprovalEngMasterData.objects.get(pk=ApprovalEngMasterData_record.pk)
                # flow name condition
                insert_empLeave(EmpId,LeaveRequestId,PendingActionFrom,RequestRaisedDatetime,ActionDatetime,ApprovalEngUniqueID)
                return JsonResponse({'message': 'Data processed successfully'})
            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    

    def get(self, request):
        employee = EmpLeave.objects.all()
        approvaldata = ApprovalEngMasterData.objects.all()

        approvaldataserializer = ApprovalEngMasterDataSerializer(approvaldata, many=True)
        empLeavedataserializer = EmpLeaveSerializer(employee, many=True)

        # Organize approval data into a dictionary for easy access
        approval_data_dict = {entry['approvalEngUniqueID']: entry for entry in approvaldataserializer.data}

        # Combine data based on the common field (approvalid)
        combined_data = []
        for emp_leave_entry in empLeavedataserializer.data:
            approval_id = emp_leave_entry.get('approvalEngUniqueID')
            approval_data = approval_data_dict.get(approval_id)
            # print(type(emp_leave_entry))
            combined_entry = { 
                'emp_leave_data': emp_leave_entry,
                'approval_data': approval_data,
            }
            combined_data.append(combined_entry)

        return Response(combined_data)


def insert_empLeave(EmpId,LeaveRequestId,PendingActionFrom,RequestRaisedDatetime,ActionDatetime,ApprovalEngUniqueID):
    data = EmpLeave(empId=EmpId, leaveRequestId=LeaveRequestId, pendingActionFrom=PendingActionFrom, requestRaisedDatetime=RequestRaisedDatetime,actionDatetime= ActionDatetime,approvalEngUniqueID = ApprovalEngUniqueID)
    data.save()
 
def insert_ApprovalEngMasterData():
    pass



#  def post(self,request):
#         if 'application/json' in request.content_type:
#             try:
#                 data = json.loads(request.body.decode('utf-8'))
#                 Status = data.get('status', None)
#                 ApprovalReason =data.get('approvalReason', None)
#                 RejectionReason=data.get('rejectionReason', None)
#                 Description =data.get('description', None)
#                 Justification =data.get('justification', None)
#                 Remarks =data.get('remarks', None)
#                 Comments =data.get('comments', None)
#                 LatestUpdateDate =data.get('latestUpdateDate', None)
#                 ApprovalEngMasterData_record = ApprovalEngMasterData.objects.create(status=Status,approvalReason=ApprovalReason,rejectionReason=RejectionReason,description=Description,justification=Justification,remarks=Remarks,comments=Comments,latestUpdateDate=LatestUpdateDate)
#                 EmpId = data.get('empId', None)
#                 LeaveRequestId = data.get('leaveRequestId', None)
#                 PendingActionFrom = data.get('pendingActionFrom', None)
#                 RequestRaisedDatetime = data.get('requestRaisedDatetime', None)
#                 ActionDatetime = data.get('actionDatetime', None)
#                 # ApprovalEngUniqueID = ApprovalEngMasterData_record.pk
#                 ApprovalEngUniqueID = ApprovalEngMasterData.objects.get(pk=ApprovalEngMasterData_record.pk)
#                 insert_empLeave(EmpId,LeaveRequestId,PendingActionFrom,RequestRaisedDatetime,ActionDatetime,ApprovalEngUniqueID)
#                 return JsonResponse({'message': 'Data processed successfully'})
#             except json.JSONDecodeError as e:
#                     return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    












