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
from django.db import connection


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
            emp_leave_entry['status']=approval_data['status']
            emp_leave_entry['approvalReason']=approval_data['approvalReason']
            emp_leave_entry['rejectionReason']=approval_data['rejectionReason']
            emp_leave_entry['description']=approval_data['description']
            emp_leave_entry['justification']=approval_data['justification']
            emp_leave_entry['remarks']=approval_data['remarks']
            emp_leave_entry['comments']=approval_data['comments']
        
            combined_data.append(emp_leave_entry)

        return Response(combined_data)


def insert_empLeave(EmpId,LeaveRequestId,PendingActionFrom,RequestRaisedDatetime,ActionDatetime,ApprovalEngUniqueID):
    data = EmpLeave(empId=EmpId, leaveRequestId=LeaveRequestId, pendingActionFrom=PendingActionFrom, requestRaisedDatetime=RequestRaisedDatetime,actionDatetime= ActionDatetime,approvalEngUniqueID = ApprovalEngUniqueID)
    data.save()
 
def insert_ApprovalEngMasterData():
    pass

class LeaveApprovalStatus(APIView):
    
    # #not need to change 
    def get(self,request):
        try:
            request = request if isinstance(request,dict) else json.loads(request.body)
            pending={'approvalEngUniqueID_id':[],'empId':[]}
            if 'empId' in request and request['empId']:
                approvaldata = list(ApprovalEngMasterData.objects.all().values())
            if 'empId' in request and request['empId'] and 'status' in request and request['status']:
                if approvaldata:
                    for data in approvaldata:
                        for status in data['status']:
                            if request['empId'] == status['ActionBy'] and request['status']== status['status']:
                                pending['approvalEngUniqueID_id'].append(data['approvalEngUniqueID'])
            else:
                if approvaldata:
                    for data in approvaldata:
                        for status in data['status']:
                            if request['empId'] == status['ActionBy']:
                                pending['approvalEngUniqueID_id'].append(data['approvalEngUniqueID'])
            employee_leave = list(EmpLeave.objects.filter(approvalEngUniqueID__in=pending['approvalEngUniqueID_id']).values())
            approvaldata = list(ApprovalEngMasterData.objects.filter(approvalEngUniqueID__in=pending['approvalEngUniqueID_id']).values())
            approval_data_dict = {}
            for approve in approvaldata:
                approval_data_dict[approve['approvalEngUniqueID']]=approve
            for leave in employee_leave:
                print("leave['approvalEngUniqueID']",leave['approvalEngUniqueID_id'])
                leave['status']=approval_data_dict[leave['approvalEngUniqueID_id']]['status']
                leave['approvalReason']=approval_data_dict[leave['approvalEngUniqueID_id']]['approvalReason']
                leave['rejectionReason']=approval_data_dict[leave['approvalEngUniqueID_id']]['rejectionReason']
                leave['description']=approval_data_dict[leave['approvalEngUniqueID_id']]['description']
                leave['justification']=approval_data_dict[leave['approvalEngUniqueID_id']]['justification']
                leave['remarks']=approval_data_dict[leave['approvalEngUniqueID_id']]['remarks']
                leave['comments']=approval_data_dict[leave['approvalEngUniqueID_id']]['comments']
            else:
                print("----->empId")
        except (Exception) as error:
            print('error------>',error)
        return Response(employee_leave)
    
    #not need to change without sp
    def put(self,request):
        try:
            return_object={}
            request = request if isinstance(request,dict) else json.loads(request.body)
            approvaldata = ApprovalEngMasterData.objects.get(approvalEngUniqueID=request['approvalEngUniqueID_id'])
            if 'status' in request and request['status']:#request['status'] in ('Approved','Rejected'):
                status = approvaldata.status
                for records in status:
                    if records['ActionBy'] == request['ActionBy']:
                        records['status'] = request['status']    
                approvaldata.status=status
                approvaldata.save()
                return_object={"message":"Success"}
            else:
                return_object={
                    'message': "Invalid request",   
                }
        except (Exception) as error:
            print("Failed to approve data",error)
            return_object={
                'message': "Failed to approve data",
                
            }
        return Response(return_object)
    
    
    #Don'uncomment it
    # def get(self,request):
    #     try:
    #         request = request if isinstance(request,dict) else json.loads(request.body)
    #         pending={'approvalEngUniqueID_id':[],'empId':[]}
    #         if 'ActionBy' in request and request['ActionBy']:
    #             flow_id=ApprovalFlow.objects.filter(approvalFlowName=request['flow_name']).values_list('flow_id')
    #             approvaldata = ApprovalEngMasterData.objects.filter(flow_id=flow_id[0][0],status__icontains=request['ActionBy']).filter(approvalEngUniqueID__icontains=request['ActionBy']).values()
    #         if 'empId' in request and request['empId'] and 'status' in request and request['status']:
    #             if approvaldata:
    #                 for data in approvaldata:
    #                     for status in data['status']:
    #                         if request['empId'] == status['ActionBy'] and request['status']== status['status']:
    #                             pending['approvalEngUniqueID_id'].append(data['approvalEngUniqueID'])
    #         else:
    #             if approvaldata:
    #                 for data in approvaldata:
    #                     for status in data['status']:
    #                         if request['empId'] == status['ActionBy']:
    #                             pending['approvalEngUniqueID_id'].append(data['approvalEngUniqueID'])
    #         employee_leave = list(EmpLeave.objects.filter(approvalEngUniqueID__in=pending['approvalEngUniqueID_id']).values())
    #         approvaldata = list(ApprovalEngMasterData.objects.filter(approvalEngUniqueID__in=pending['approvalEngUniqueID_id']).values())
    #         approval_data_dict = {}
    #         for approve in approvaldata:
    #             approval_data_dict[approve['approvalEngUniqueID']]=approve
    #         for leave in employee_leave:
    #             leave['status']=approval_data_dict[leave['approvalEngUniqueID_id']]['status']
    #             leave['approvalReason']=approval_data_dict[leave['approvalEngUniqueID_id']]['approvalReason']
    #             leave['rejectionReason']=approval_data_dict[leave['approvalEngUniqueID_id']]['rejectionReason']
    #             leave['description']=approval_data_dict[leave['approvalEngUniqueID_id']]['description']
    #             leave['justification']=approval_data_dict[leave['approvalEngUniqueID_id']]['justification']
    #             leave['remarks']=approval_data_dict[leave['approvalEngUniqueID_id']]['remarks']
    #             leave['comments']=approval_data_dict[leave['approvalEngUniqueID_id']]['comments']
    #     except (Exception) as error:
    #         print('error------>',error)
    #         d=[2]
    #     return Response(employee_leave)
    
    
    
    
    #not need to change with sp don't delete this
    # def put(self,request):
    #     try:
    #         return_object={}
    #         request = request if isinstance(request,dict) else json.loads(request.body)
    #         sql_query = 'SELECT "status", "approvalReason", "rejectionReason", "description", "justification", "remarks", "comments" FROM "ApprovalEngMasterData" where "approvalEngUniqueID" = '+ str(request['approvalEngUniqueID_id']) +';'
    #         cursor= connection.cursor()
    #         cursor.execute(sql_query)
    #         columns = cursor.description 
    #         approvaldata = [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
    #         # if 'status' in request and request['status']:
    #         status = json.loads(approvaldata[0]['status'])
    #         for records in status:
    #             if records['ActionBy'] == request['ActionBy']:
    #                 records['status'] = request['status']  
    #         # if 'approvalReason' in request and request['approvalReason']:
    #         approvalReason= json.loads(approvaldata[0]['approvalReason'])  
    #         for records in approvalReason:
    #             if records['ActionBy'] == request['ActionBy']:
    #                 records['approvalReason'] = request['approvalReason'] 
    #         # if 'rejectionReason' in request and request['rejectionReason']:
    #         rejectionReason= json.loads(approvaldata[0]['rejectionReason'])  
    #         for records in rejectionReason:
    #             if records['ActionBy'] == request['ActionBy']:
    #                 records['rejectionReason'] = request['description'] 
    #         # if 'description' in request and request['description']:
    #         description= json.loads(approvaldata[0]['description'])  
    #         for records in description:
    #             if records['ActionBy'] == request['ActionBy']:
    #                 records['description'] = request['description'] 
    #         # if 'justification' in request and request['justification']:
    #         justification= json.loads(approvaldata[0]['justification'])  
    #         for records in justification:
    #             if records['ActionBy'] == request['ActionBy']:
    #                 records['justification'] = request['justification']
    #         # if 'remarks' in request and request['remarks']:
    #         remarks= json.loads(approvaldata[0]['remarks'])  
    #         for records in remarks:
    #             if records['ActionBy'] == request['ActionBy']:
    #                 records['remarks'] = request['remarks']
    #         # if 'remarks' in request and request['remarks']:
    #         comments= json.loads(approvaldata[0]['comments'])  
    #         for records in comments:
    #             if records['ActionBy'] == request['ActionBy']:
    #                 records['comments'] = request['comments']  
    #         status=json.dumps(status)
    #         approvalReason=json.dumps(approvalReason)
    #         rejectionReason=json.dumps(rejectionReason)
    #         description=json.dumps(description)
    #         justification=json.dumps(justification)
    #         remarks=json.dumps(remarks)
    #         comments=json.dumps(comments)
    #         cursor.execute("call update_approval_status(%s, %s,%s,%s,%s,%s,%s,%s)",(int(request['approvalEngUniqueID_id']),status,approvalReason,rejectionReason,description,justification,remarks,comments))
    #         cursor.close()
    #         return_object={"message":"Success"}
    #     except (Exception) as error:
    #         print("Failed to approve data",error)
    #         return_object={
    #             'message': "Failed to approve data",
    #         }
    #     return Response(return_object)
    


