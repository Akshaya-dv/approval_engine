
from crud.e_sepModel_to_be_deleted import EmpSep
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

defaultkey=['description','status','approvalReason','rejectionReason','justification','comment','remark','actionby','date','level']
               

# Create your views here.
class empLeave(APIView):
    def post(self,request):
        if 'application/json' in request.content_type:
            try:
                data = json.loads(request.body.decode('utf-8'))
                empId = data.get('empId')

                requestRaisedDatetime = data.get('requestRaisedDatetime', None)
                flowName = data.get('flowName',None)
                description =data.get('description',None)
                actionDatetime =data.get('actionDatetime',None)
                # status =data.get('status',None)
                approvalReason=data.get('approvalReason',None)
                rejectionReason=data.get('rejectionReason',None)
                justification =data.get('justification',None)
                comment =data.get('comment',None)
                remark=data.get('remark',None)
                extraKeys=data.get('extrakeys')
                LatestUpdateDate =datetime.datetime.now()
                approvalId=0
                
                Statusobj={"actionby":empId,"status":"na","date":LatestUpdateDate.isoformat(),"level":0}
                ApprovalReasonobj ={"actionby":empId,"approvalReason":approvalReason,"date":LatestUpdateDate.isoformat(),"level":0}
                RejectionReasonobj={"actionby":empId,"rejectionReason":rejectionReason,"date":LatestUpdateDate.isoformat(),"level":0}
                Descriptionobj={"actionby":empId,"description":description,"date":LatestUpdateDate.isoformat(),"level":0}
                Justificationobj ={"actionby":empId,"justification":justification,"date":LatestUpdateDate.isoformat(),"level":0}
                Remarksobj ={"actionby":empId,"remark":remark,"date":LatestUpdateDate.isoformat(),"level":0}
                Commentsobj ={"actionby":empId,"comment":comment,"date":LatestUpdateDate.isoformat(),"level":0}
                
                columnObjMapping={'description':Descriptionobj,
                                  'status':Statusobj,
                                  'approvalReason':ApprovalReasonobj,
                                  'rejectionReason':RejectionReasonobj,
                                  'justification':Justificationobj,
                                  'comment':Commentsobj,
                                  'remark':Remarksobj}
                if extraKeys:
                    for columnkey in extraKeys.keys():
                        if (columnkey in columnObjMapping.keys()) and type(extraKeys[columnkey])==dict:
                            for extraKey in extraKeys[columnkey].keys():
                                if not(extraKey in defaultkey) and extraKeys[columnkey][extraKey]:
                                    (columnObjMapping[columnkey])[extraKey]=extraKeys[columnkey][extraKey]
                                else:
                                    return_object={
                                      "status":400,
                                      "message":f"The keys in extrakeys request body sholud not be equal to {defaultkey}"
                                      }  
                        else:
                            return_object={
                                      "status":400,
                                      "message":f"The keys in extrakeys request body sholud json object key format"
                                      }  
                statusStrObj=str(columnObjMapping['status'])
                StatusArr=[json.loads(statusStrObj.replace("'", "\""))]
                approvalReasonStrObj=str(columnObjMapping['approvalReason'])
                ApprovalReasonArr=[json.loads(approvalReasonStrObj.replace("'", "\""))]
                rejectionReasonStrObj=str(columnObjMapping['rejectionReason'])
                RejectionReasonArr=[json.loads(rejectionReasonStrObj.replace("'", "\""))]
                descriptionStrObj=str(columnObjMapping['description'])
                DescriptionArr=[json.loads(descriptionStrObj.replace("'", "\""))]
                justificationStrObj=str(columnObjMapping['justification'])
                JustificationArr=[json.loads(justificationStrObj.replace("'", "\""))]
                remarkStrObj=str(columnObjMapping['remark'])
                RemarksArr=[json.loads(remarkStrObj.replace("'", "\""))]
                commentStrObj=str(columnObjMapping['comment'])
                CommentsArr=[json.loads(commentStrObj.replace("'", "\""))]
#             #  getting approval flow id from approval flow
                with connection.cursor() as cursor:
                    try:
                        cursor.execute("BEGIN;")
                        # Call the stored procedure
                        cursor.execute(' CALL public.get_hirarchy(%s,%s); ',[empId,flowName])
                        # Fetch all from the result cursor
                        cursor.execute('FETCH ALL FROM "hirarchy";')
                        hirarchyData = cursor.fetchall()
                        # Commit the transaction
                        cursor.execute("COMMIT;")
                        print (hirarchyData)

#             #  getting the approval hirarchy form hirarchy table
                        for i in hirarchyData:
                            for columnkey in columnObjMapping.keys():
                                (columnObjMapping[columnkey])['actionby']=i[0]
                                (columnObjMapping[columnkey])['level']=i[1]
                                (columnObjMapping[columnkey])['date']='na'
                            (columnObjMapping['status'])['status']='ApprovalPending'
                            (columnObjMapping['approvalReason'])['approvalReason']=''
                            (columnObjMapping['rejectionReason'])['rejectionReason']=''
                            (columnObjMapping['description'])['description']=''
                            (columnObjMapping['justification'])['justification']=''
                            (columnObjMapping['remark'])['remark']=''
                            (columnObjMapping['comment'])['comment']=''
                            statusStrObj=str(columnObjMapping['status'])
                            approvalReasonStrObj=str(columnObjMapping['approvalReason'])
                            rejectionReasonStrObj=str(columnObjMapping['rejectionReason'])
                            descriptionStrObj=str(columnObjMapping['description'])
                            justificationStrObj=str(columnObjMapping['justification'])
                            remarkStrObj=str(columnObjMapping['remark'])
                            commentStrObj=str(columnObjMapping['comment'])

                            StatusArr.append(json.loads(statusStrObj.replace("'", "\"")))
                            ApprovalReasonArr.append(json.loads(approvalReasonStrObj.replace("'", "\"")))
                            RejectionReasonArr.append(json.loads(rejectionReasonStrObj.replace("'", "\"")))
                            DescriptionArr.append(json.loads(descriptionStrObj.replace("'", "\"")))
                            JustificationArr.append(json.loads(justificationStrObj.replace("'", "\"")))
                            RemarksArr.append(json.loads(remarkStrObj.replace("'", "\"")))
                            CommentsArr.append(json.loads(commentStrObj.replace("'", "\"")))
                        
                        
                        # print(StatusArr,ApprovalReasonArr,RejectionReasonArr,DescriptionArr,JustificationArr,RemarksArr,CommentsArr,LatestUpdateDate, flowName,approvalId)
                        cursor.execute('CALL public.insert_approval(%s, %s, %s, %s, %s, %s,%s, %s, %s, %s)', [json.dumps(StatusArr),json.dumps(ApprovalReasonArr),json.dumps(RejectionReasonArr),json.dumps(DescriptionArr),json.dumps(JustificationArr),json.dumps(RemarksArr),json.dumps(CommentsArr),LatestUpdateDate, flowName,approvalId])
                        results = cursor.fetchall()
                    finally:
                          cursor.close()
                          for item in results:
                              approvalId = item[0]
                          return_object={
                    "status":200,
                    "result":approvalId,
                    "message":"success"
                }
            except json.JSONDecodeError as e:
                return_object={
                    "status":400,
                    "message":"invalid request body"
                    }  
    
        return JsonResponse(return_object)

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
                           
                            objFormatedApprovalData[status[i]['actionby']]={
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
                                "commentsUpdatedDate":remarks[i]['date'],
                            }
                            for key in status[i].keys():
                                if not(key in defaultkey):
                                   (objFormatedApprovalData[status[i]['actionby']])[key]=status[i][key]
                            for key in approvalReason[i].keys():
                                if not(key in defaultkey):
                                   (objFormatedApprovalData[status[i]['actionby']])[key]=approvalReason[i][key]
                            for key in rejectionReason[i].keys():
                                if not(key in defaultkey):
                                   (objFormatedApprovalData[status[i]['actionby']])[key]=rejectionReason[i][key]
                            for key in description[i].keys():
                                if not(key in defaultkey):
                                   (objFormatedApprovalData[status[i]['actionby']])[key]=description[i][key]
                            for key in justification[i].keys():
                                if not(key in defaultkey):
                                   (objFormatedApprovalData[status[i]['actionby']])[key]=justification[i][key]
                            for key in remarks[i].keys():
                                if not(key in defaultkey):
                                   (objFormatedApprovalData[status[i]['actionby']])[key]=remarks[i][key]
                            for key in comments[i].keys():
                                if not(key in defaultkey):
                                   (objFormatedApprovalData[status[i]['actionby']])[key]=comments[i][key]
                            
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

    def delete(self,request):
        try:
            return_object={}
            request = request if isinstance(request,dict) else json.loads(request.body)
            approvalEngUniqueID = request['approvalEngUniqueID_id']
            with connection.cursor() as cursor:
                    cursor.execute("BEGIN;")
                    # Call the stored procedure
                    cursor.execute(' CALL get_delete_approvalstatus(%s,%s); ',[approvalEngUniqueID,0])
                    # Fetch all from the result cursor
                    cursor.execute('FETCH ALL FROM "selctedrow";')
                    deletedmessage = cursor.fetchall()
                    # Commit the transaction
                    cursor.execute("COMMIT;")
                    return_object={
                        "status":200,
                        "message":deletedmessage
                    }
        except:
            return_object={
                        "status":400,
                        "message":"Invalid Request Body"
                    }
        return JsonResponse(return_object)
    


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
    
    # # #not need to change 
    def get(self,request):
        try:
            request = request if isinstance(request,dict) else json.loads(request.body)
            pending={'approvalEngUniqueID_id':[],'empId':[]}
            if 'empId' in request and request['empId']:
                approvaldata = list(ApprovalEngMasterData.objects.all().values())
                print("---->1",approvaldata)
            if 'empId' in request and request['empId'] and 'status' in request and request['status']:

                if approvaldata:
                    for data in approvaldata:
                        for status in data['status']:
                            if request['empId'] == status['actionby'] and request['status']== status['status']:
                                pending['approvalEngUniqueID_id'].append(data['approvalEngUniqueID'])
            else:
                if approvaldata:
                    for data in approvaldata:
                        for status in data['status']:
                            if request['empId'] == status['actionby']:
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
            print('error------>ApprovalStatus_get',error)
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
                    if records['actionby'] == request['actionby']:
                        records['status'] = request['status']   
                        records['date'] = str(datetime.datetime.now())
                approvaldata.status=status
                
                approvalReason = approvaldata.approvalReason
                for records in approvalReason:
                    if records['actionby'] == request['actionby']:
                        records['approvalReason'] = request['approvalReason']   
                        records['date'] = str(datetime.datetime.now())
                approvaldata.approvalReason=approvalReason
                
                rejectionReason = approvaldata.rejectionReason
                for records in rejectionReason:
                    if records['actionby'] == request['actionby']:
                        records['rejectionReason'] = request['rejectionReason']   
                        records['date'] = str(datetime.datetime.now())
                approvaldata.rejectionReason=rejectionReason
                
                description = approvaldata.description
                for records in description:
                    if records['actionby'] == request['actionby']:
                        records['description'] = request['description']   
                        records['date'] = str(datetime.datetime.now())
                approvaldata.description=description
                
                justification = approvaldata.justification
                for records in justification:
                    if records['actionby'] == request['actionby']:
                        records['justification'] = request['justification']   
                        records['date'] = str(datetime.datetime.now())
                approvaldata.justification=justification
                
                remarks = approvaldata.remarks
                for records in remarks:
                    if records['actionby'] == request['actionby']:
                        records['remarks'] = request['remarks']   
                        records['date'] = str(datetime.datetime.now())
                approvaldata.remarks=remarks
                
                comments = approvaldata.comments
                for records in comments:
                    if records['actionby'] == request['actionby']:
                        records['comments'] = request['comments']   
                        records['date'] = str(datetime.datetime.now())
                approvaldata.comments=comments
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
    
    #not need to change with sp
    def put(self,request):
        try:
            return_object={}
            request = request if isinstance(request,dict) else json.loads(request.body)
            sql_query = 'SELECT "status", "approvalReason", "rejectionReason", "description", "justification", "remarks", "comments" FROM "ApprovalEngMasterData" where "approvalEngUniqueID" = '+ str(request['approvalEngUniqueID_id']) +';'
            cursor= connection.cursor()
            cursor.execute(sql_query)
            columns = cursor.description 
            approvaldata = [{columns[index][0]:column for index, column in enumerate(value)} for value in cursor.fetchall()]
            # if 'status' in request and request['status']:
            status = json.loads(approvaldata[0]['status'])
            for records in status:
                if records['actionby'] == request['actionby']:
                    records['status'] = request['status']  
            # if 'approvalReason' in request and request['approvalReason']:
            approvalReason= json.loads(approvaldata[0]['approvalReason'])  
            for records in approvalReason:
                if records['actionby'] == request['actionby']:
                    records['approvalReason'] = request['approvalReason'] 
            # if 'rejectionReason' in request and request['rejectionReason']:
            rejectionReason= json.loads(approvaldata[0]['rejectionReason'])  
            for records in rejectionReason:
                if records['actionby'] == request['actionby']:
                    records['rejectionReason'] = request['description'] 
            # if 'description' in request and request['description']:
            description= json.loads(approvaldata[0]['description'])  
            for records in description:
                if records['actionby'] == request['actionby']:
                    records['description'] = request['description'] 
            # if 'justification' in request and request['justification']:
            justification= json.loads(approvaldata[0]['justification'])  
            for records in justification:
                if records['actionby'] == request['actionby']:
                    records['justification'] = request['justification']
            # if 'remarks' in request and request['remarks']:
            remarks= json.loads(approvaldata[0]['remarks'])  
            for records in remarks:
                if records['actionby'] == request['actionby']:
                    records['remarks'] = request['remarks']
            # if 'remarks' in request and request['remarks']:
            comments= json.loads(approvaldata[0]['comments'])  
            for records in comments:
                if records['actionby'] == request['actionby']:
                    records['comments'] = request['comments']  
            status=json.dumps(status)
            approvalReason=json.dumps(approvalReason)
            rejectionReason=json.dumps(rejectionReason)
            description=json.dumps(description)
            justification=json.dumps(justification)
            remarks=json.dumps(remarks)
            comments=json.dumps(comments)
            cursor.execute("call update_approval_status(%s, %s,%s,%s,%s,%s,%s,%s)",(int(request['approvalEngUniqueID_id']),status,approvalReason,rejectionReason,description,justification,remarks,comments))
            cursor.close()
            return_object={"message":"Success"}
           
        except (Exception) as error:
            print("Failed to approve data",error)
            return_object={
                'message': "Failed to approve data",
                
            }
        return Response(return_object)
    










