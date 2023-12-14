import datetime
import json
from django.db import connection
from approval_engine.models import ApprovalEngMasterData,ApprovalFlow,ApprovalFlowHirarchies
from rest_framework.response import Response
from approval_engine.common_function import *
from rest_framework.decorators import APIView
from approval_engine.constants import columns



class Approver:
# # #not need to change 
    def get(request):
        try:
            request = request if isinstance(request,dict) else json.loads(request.body)
            return_object = {}
            if 'empId' in request and request['empId'] and 'flowName' in request and request['flowName']:
                with connection.cursor() as cursor:
                    
                    cursor.execute("BEGIN;")
                    # Call the stored procedure
                    cursor.execute(' CALL get_approvalstatus(%s,%s,%s); ',[request['empId'],request['flowName'],request.get('status')])
                    # Fetch all from the result cursor
                    cursor.execute('FETCH ALL FROM "rs_approvaldata";')
                    approvaldata = cursor.fetchall()
                    # Commit the transaction
                    cursor.execute("COMMIT;")
                    
                    formatedApprovalData = formating_response(approvaldata)
                 
                    return_object = {
                        "status":200,
                        "message":"Data retrieved successfully",
                        "result":formatedApprovalData
                    }
                
            else:
                return_object = {
                        "status":400,
                        "message":"Invalid Request Body"
                    }
        except (Exception) as error:
            print("Issue is beacause of "+str(error))
            return_object = {
                        "status":500,
                        "message":"Failed to retrieved data"
                    }
        return Response(return_object)
   
    
    def put(request):
        try:
            return_object={}
            request = request if isinstance(request,dict) else json.loads(request.body)
            cursor=connection.cursor()
            cursor.execute("BEGIN;")
            # Call the stored procedure
            cursor.execute(' CALL get_ApprovalMaster_AppEngUniqId(%s); ',[request.get('approvalEngUniqueID_id')])
            # Fetch all from the result cursor
            cursor.execute('FETCH ALL FROM "rs_approvaldata";')
            approvaldata_status = cursor.fetchall()
            # Commit the transaction
           
            cursor.execute("COMMIT;")
            
            approvaldata = [{columns[index]:json.loads(value) if isinstance(value,str) else value for index,value in enumerate(approvaldata_status[0])}]      

            # approvaldata = list(ApprovalEngMasterData.objects.filter(approvalEngUniqueID=request['approvalEngUniqueID_id']).values())
            if 'status' in request and request['status']:#request['status'] in ('Approved','Rejected'): 
                status,approvalReason,rejectionReason,description,justification,remarks,comments=[],[],[],[],[],[],[]
                for key,records in approvaldata[0].items():
                    if key in ['status','approvalReason','rejectionReason','description','justification','remarks','comments']:
                        for data in records:
                            append_obj=data
                            if data['actionby']==request['actionby']:
                                for updt_key,update_value in data.items():
                                        append_obj[updt_key]=request[updt_key] if updt_key in request and updt_key != 'date' else update_value
                                        if updt_key=='date':
                                            append_obj[updt_key]=str(datetime.datetime.now())
                                         
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
                cursor.execute("call update_approval_status(%s, %s,%s,%s,%s,%s,%s,%s)",(int(request['approvalEngUniqueID_id']),json.dumps(status),json.dumps(approvalReason),json.dumps(rejectionReason),json.dumps(description),json.dumps(justification),json.dumps(remarks),json.dumps(comments)))
                cursor.close()
                
                # ApprovalEngMasterData.objects.filter(approvalEngUniqueID=request['approvalEngUniqueID_id']).update(status=status,approvalReason=approvalReason,rejectionReason=rejectionReason,description=description,justification=justification,remarks=remarks,comments=comments,latestUpdateDate=datetime.datetime.now().isoformat())
                
                return_object={
                    "status":200,
                    "message":"Data Updated Successfully",
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
    
 
    
# class Approver(APIView):
# # # #not need to change 
#     def get(self,request):
#         try:
#             request = request if isinstance(request,dict) else json.loads(request.body)
#             return_object = {}
#             if 'empId' in request and request['empId'] and 'flowName' in request and request['flowName']:
#                 with connection.cursor() as cursor:
                    
#                     cursor.execute("BEGIN;")
#                     # Call the stored procedure
#                     cursor.execute(' CALL get_approvalstatus(%s,%s,%s); ',[request['empId'],request['flowName'],request.get('status')])
#                     # Fetch all from the result cursor
#                     cursor.execute('FETCH ALL FROM "rs_approvaldata";')
#                     approvaldata = cursor.fetchall()
#                     # Commit the transaction
#                     cursor.execute("COMMIT;")
                    
#                     formatedApprovalData = formating_response(approvaldata)
#                
#                     return_object = {
#                         "status":200,
#                         "message":"Data retrieved successfully",
#                         "result":formatedApprovalData
#                     }
                
#             else:
#                 return_object = {
#                         "status":400,
#                         "message":"Invalid Request Body"
#                     }
#         except (Exception) as error:
#             print("Issue is beacause of "+str(error))
#             return_object = {
#                         "status":500,
#                         "message":"Failed to retrieved data"
#                     }
#         return Response(return_object)
   
    
#     def put(self,request):
#         try:
#             return_object={}
#             request = request if isinstance(request,dict) else json.loads(request.body)
#             cursor=connection.cursor()
#             cursor.execute("BEGIN;")
#             # Call the stored procedure
#             cursor.execute(' CALL get_ApprovalMaster_AppEngUniqId(%s); ',[request.get('approvalEngUniqueID_id')])
#             # Fetch all from the result cursor
#             cursor.execute('FETCH ALL FROM "rs_approvaldata";')
#             approvaldata_status = cursor.fetchall()
#             # Commit the transaction
#             cursor.execute("COMMIT;")
            
#             approvaldata = [{columns[index]:json.loads(value) if isinstance(value,str) else value for index,value in enumerate(approvaldata_status[0])}]      
#             # approvaldata = list(ApprovalEngMasterData.objects.filter(approvalEngUniqueID=request['approvalEngUniqueID_id']).values())
#             if 'status' in request and request['status']:#request['status'] in ('Approved','Rejected'): 
#                 status,approvalReason,rejectionReason,description,justification,remarks,comments=[],[],[],[],[],[],[]
#                 for key,records in approvaldata[0].items():
#                     if key in ['status','approvalReason','rejectionReason','description','justification','remarks','comments']:
#                         for data in records:
#                             append_obj=data
#                             if data['actionby']==request['actionby']:
#                                 for updt_key,update_value in data.items():
#                                         append_obj[updt_key]=request[updt_key] if updt_key in request and updt_key != 'date' else update_value
#                                         if updt_key=='date':
#                                             append_obj[updt_key]=str(datetime.datetime.now())
                                         
#                             if key == 'status':
#                                 status.append(append_obj)
#                             if key == 'approvalReason':
#                                 approvalReason.append(append_obj)
#                             if key == 'rejectionReason':
#                                 rejectionReason.append(append_obj)
#                             if key == 'description':
#                                 description.append(append_obj)
#                             if key == 'justification':
#                                 justification.append(append_obj)
#                             if key == 'remarks':
#                                 remarks.append(append_obj)
#                             if key == 'comments':
#                                 comments.append(append_obj)
#                 cursor.execute("call update_approval_status(%s, %s,%s,%s,%s,%s,%s,%s)",(int(request['approvalEngUniqueID_id']),json.dumps(status),json.dumps(approvalReason),json.dumps(rejectionReason),json.dumps(description),json.dumps(justification),json.dumps(remarks),json.dumps(comments)))
#                 cursor.close()
                
#                 # ApprovalEngMasterData.objects.filter(approvalEngUniqueID=request['approvalEngUniqueID_id']).update(status=status,approvalReason=approvalReason,rejectionReason=rejectionReason,description=description,justification=justification,remarks=remarks,comments=comments,latestUpdateDate=datetime.datetime.now().isoformat())
                
#                 return_object={
#                     "status":200,
#                     "message":"Data Updated Successfully",
#                                }
#             else:
#                 return_object={
#                     "status":400,
#                     'message': "Invalid request body",   
#                 }
#         except (Exception) as error:
#             print("Failed to approve data",error)
#             return_object={
#                 "status":500,
#                 'message': "Failed to approve data",
                
#             }
#         return Response(return_object)
    
#     # def put(self,request):
#     #     try:
#     #         return_object={}
#     #         request = request if isinstance(request,dict) else json.loads(request.body)
#     #         approvaldata = list(ApprovalEngMasterData.objects.filter(approvalEngUniqueID=request['approvalEngUniqueID_id']).values())
#     #         if 'status' in request and request['status']:#request['status'] in ('Approved','Rejected'): 
#     #             status,approvalReason,rejectionReason,description,justification,remarks,comments=[],[],[],[],[],[],[]
#     #             for key,records in approvaldata[0].items():
#     #                 if key in ['status','approvalReason','rejectionReason','description','justification','remarks','comments']:
#     #                     for data in records:
#     #                         append_obj=data
#     #                         if data['actionby']==request['actionby']:
#     #                             for updt_key,update_value in data.items():
#     #                                     append_obj[updt_key]=request[updt_key] if updt_key in request and updt_key != 'date' else update_value
#     #                                     if updt_key=='date':
#     #                                         append_obj[updt_key]=str(datetime.datetime.now())
                                         
#     #                         if key == 'status':
#     #                             status.append(append_obj)
#     #                         if key == 'approvalReason':
#     #                             approvalReason.append(append_obj)
#     #                         if key == 'rejectionReason':
#     #                             rejectionReason.append(append_obj)
#     #                         if key == 'description':
#     #                             description.append(append_obj)
#     #                         if key == 'justification':
#     #                             justification.append(append_obj)
#     #                         if key == 'remarks':
#     #                             remarks.append(append_obj)
#     #                         if key == 'comments':
#     #                             comments.append(append_obj)
                
#     #             ApprovalEngMasterData.objects.filter(approvalEngUniqueID=request['approvalEngUniqueID_id']).update(status=status,approvalReason=approvalReason,rejectionReason=rejectionReason,description=description,justification=justification,remarks=remarks,comments=comments,latestUpdateDate=datetime.datetime.now().isoformat())
                
#     #             return_object={
#     #                 "status":200,
#     #                 "message":"Data Updated Successfully"
#     #                            }
#     #         else:
#     #             return_object={
#     #                 "status":400,
#     #                 'message': "Invalid request body",   
#     #             }
#     #     except (Exception) as error:
#     #         print("Failed to approve data",error)
#     #         return_object={
#     #             "status":500,
#     #             'message': "Failed to approve data",
                
#     #         }
#     #     return Response(return_object)
    