
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.views import APIView
from django.db import connection
import json
import datetime
from .models import  ApprovalEngMasterData,ApprovalFlow,ApprovalFlowHirarchies
from .leaveModel_to_be_deleted import EmpLeave
from .serializer import EmpLeaveSerializer,ApprovalEngMasterDataSerializer,ApprovalFlow,ApprovalFlowHirarchies
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
                approvalId=0

                LatestUpdateDate =datetime.datetime.now()
                with connection.cursor() as cursor:
                    try:
                        cursor.execute('CALL public.insert_leave_approval(%s, %s, %s, %s, %s, %s)', [ LatestUpdateDate, FlowName, EmpId, RequestRaisedDatetime, ActionDatetime,approvalId])
                        results = cursor.fetchall()
                    finally:
                        cursor.close()
                        for item in results:
                            approvalId = item[0]
                           
                
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
                insert_empLeave(EmpId,'[{}]',RequestRaisedDatetime,ActionDatetime,approvalId)
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
            emp_leave_entry['status']=approval_data['status']
            emp_leave_entry['approvalReason']=approval_data['approvalReason']
            emp_leave_entry['rejectionReason']=approval_data['rejectionReason']
            emp_leave_entry['description']=approval_data['description']
            emp_leave_entry['justification']=approval_data['justification']
            emp_leave_entry['remarks']=approval_data['remarks']
            emp_leave_entry['comments']=approval_data['comments']
        
            combined_data.append(emp_leave_entry)
        
        EmpId=1111
        with connection.cursor() as cursor:
            result = cursor.var(psycopg2.extensions.PG_CURSOR)
            cursor.execute('call public.procedure_name(%s,%s)', [EmpId, result])
            result = cursor.fetchone()
            # Fetch the results from the result_cursor
            cursor.execute('FETCH ALL FROM result')
            result =cursor.fetchall()
            print(result)

        return Response(combined_data)


def insert_empLeave(EmpId,PendingActionFrom,RequestRaisedDatetime,ActionDatetime,ApprovalEngUniqueID):
    data = EmpLeave(empId=EmpId, pendingActionFrom=PendingActionFrom, requestRaisedDatetime=RequestRaisedDatetime,actionDatetime= ActionDatetime,approvalEngUniqueID_id = ApprovalEngUniqueID)
    data.save()
 
def insert_ApprovalEngMasterData():
    pass












