import datetime
import json
from django.db import connection
from approval_engine.models import ApprovalEngMasterData,ApprovalFlow,ApprovalFlowHirarchies
from rest_framework.response import Response
from approval_engine.common_function import *
from rest_framework.decorators import api_view



class Approver:
# # #not need to change 
    def get(request):
        try:
            request = request if isinstance(request,dict) else json.loads(request.body)
            return_obj = {}
            if 'empId' in request and request['empId'] and 'flowName' in request and request['flowName']:
                with connection.cursor() as cursor:
                    cursor.execute("BEGIN;")
                    # Call the stored procedure
                    cursor.execute(' CALL get_approvalstatus(%s,%s); ',["%"+str(request['empId'])+"%",request['flowName']])
                    # Fetch all from the result cursor
                    cursor.execute('FETCH ALL FROM "rs_approvaldata";')
                    approvaldata = cursor.fetchall()
                    # Commit the transaction
                    cursor.execute("COMMIT;")
                    formatedApprovalData = formating_response(approvaldata)
                    return_obj = {
                        "status":200,
                        "message":"Data retrieved successfully",
                        "result":formatedApprovalData
                    }
                
            else:
                return_obj = {
                        "status":400,
                        "message":"Invalid Request Body"
                    }
        except (Exception) as error:
            print("Issue is beacause of "+str(error))
            return_obj = {
                        "status":500,
                        "message":"Failed to retrieved data"
                    }
        return Response(return_obj)
   
    
    def put(request):
        try:
            return_object={}
            request = request if isinstance(request,dict) else json.loads(request.body)
            approvaldata = list(ApprovalEngMasterData.objects.filter(approvalEngUniqueID=request['approvalEngUniqueID_id']).values())
            if 'status' in request and request['status']:#request['status'] in ('Approved','Rejected'): 
                status,approvalReason,rejectionReason,description,justification,remarks,comments=[],[],[],[],[],[],[]
                for key,records in approvaldata[0].items():
                    if key in ['status','approvalReason','rejectionReason','description','justification','remarks','comments']:
                        for data in records:
                            append_obj=data
                            if data['actionby']==request['actionby']:
                                for updt_key,update_value in data.items():
                                        append_obj[updt_key]=request[updt_key] if updt_key in request else update_value
                            if key == 'status':
                                status.append(append_obj)
                            if key == 'approvalReason':
                                approvalReason.append(append_obj)
                            if key == 'rejectionReason':
                                rejectionReason.append(append_obj)
                            if key == 'description':
                                description.append(append_obj)
                            if key == 'justification':
                                justification.append(append_obj)
                            if key == 'remarks':
                                remarks.append(append_obj)
                            if key == 'comments':
                                comments.append(append_obj)
                
                ApprovalEngMasterData.objects.filter(approvalEngUniqueID=request['approvalEngUniqueID_id']).update(status=status,approvalReason=approvalReason,rejectionReason=rejectionReason,description=description,justification=justification,remarks=remarks,comments=comments,latestUpdateDate=datetime.datetime.now().isoformat())
                
                return_object={
                    "status":200,
                    "message":"Data Updated Successfully"
                               }
            else:
                return_object={
                    "status":400,
                    'message': "Invalid request body",   
                }
        except (Exception) as error:
            print("Failed to approve data",error)
            return_object={
                "status":500,
                'message': "Failed to approve data",
                
            }
        return Response(return_object)
    
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
    