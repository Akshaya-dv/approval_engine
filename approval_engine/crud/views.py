
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.views import APIView
from django.db import connection
import json
import datetime

from crud.e_sepModel_to_be_deleted import EmpSep
from .models import  ApprovalEngMasterData,ApprovalFlow,ApprovalFlowHirarchies
from .leaveModel_to_be_deleted import EmpLeave
from .serializer import EmpLeaveSerializer,ApprovalEngMasterDataSerializer,ApprovalFlow,ApprovalFlowHirarchies, EmpSeparation
from rest_framework import status
import psycopg2
from psycopg2.extras import Json
from django.db import connection



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
            d=[2]
        return Response(employee_leave)
    
    # #not need to change without sp
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
    
    
    # #Don'uncomment it
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
    #     return Response(employee_leave)
    
    
    
    
    # #not need to change with sp
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
    











