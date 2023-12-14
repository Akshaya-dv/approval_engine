import datetime
import json
from django.db import connection
from rest_framework.response import Response
from .common_function import formating_response
from .constants import *
from django.db import connection
from rest_framework.views import APIView


class Applier:
    def post(request):
        try:
            return_object={}
            data = json.loads(request.body.decode('utf-8'))
            data['empId']=int(data['empId'])
            if not all(key in data for key in POST_PARAMETER_CHECK) or not isinstance(data['empId'],int) :
                    return_object={
                    "status":400,
                    "message":"invalid request body"
                    }    
                    return return_object
            
            empId = data.get('empId')
            flowName = data.get('flowName',None)
            description =data.get('description',None)
            status =data.get('status',None)
            approvalReason=data.get('approvalReason',None)
            rejectionReason=data.get('rejectionReason',None)
            justification =data.get('justification',None)
            comment =data.get('comment',None)
            remark=data.get('remark',None)
            extraKeys=data.get('extrakeys')
            LatestUpdateDate =datetime.datetime.now()
            approvalId=0
    
            Statusobj={"actionby":empId,"status":status,"date":LatestUpdateDate.isoformat(),"level":0}
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
                            if not(extraKey in defaultkey) :
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
#             # getting approval flow id from approval flow

            with connection.cursor() as cursor:
                try:
                    cursor.execute("BEGIN;")
                    cursor.execute(' CALL get_flow(%s); ',[flowName])
             # Fetch all from the result cursor
                    cursor.execute('FETCH ALL FROM "flow";')
                    flowdata = cursor.fetchall()
                   
                    cursor.execute("COMMIT;")
                    # Call the stored procedure
                    # cursor.execute(' CALL public.get_hirarchy(%s,%s); ',[empId,flowName])
                    #get_flow data approval_type, no. of approval
                    NO_OF_APPROVALS=flowdata[0][2]
           
                    APPROVAL_TYPE=flowdata[0][3] 
                    # Call the stored procedure based on approval_type
                    cursor.execute("BEGIN;")
                    if APPROVAL_TYPE=="static":
                        cursor.execute(' CALL public.get_static_hirarchy(%s,%s); ',[empId,flowdata[0][0]])
                   
                    elif APPROVAL_TYPE=="dynamic":
                        cursor.execute(' CALL public.get_dynamic_hirarchy(%s); ',[str(empId)])
                    else:
                        return_object={
                            "status":200,
                            "message": "None approval type is matching"
                        }
                        return return_object
                    # Fetch all from the result cursor
                    cursor.execute('FETCH ALL FROM "hirarchy";')
                    hirarchyData = cursor.fetchall()
             
                    if NO_OF_APPROVALS:
                        hirarchyData1=[[int(reporting[1]),i+1] for i,reporting in enumerate(hirarchyData) if i<NO_OF_APPROVALS]
                    
                    # Commit the transaction
                    cursor.execute("COMMIT;")
#             # getting the approval hirarchy form hirarchy table
                    for i in hirarchyData1:
                        for columnkey in columnObjMapping.keys():
                            (columnObjMapping[columnkey])['actionby']=i[0]
                            (columnObjMapping[columnkey])['level']=i[1] 
                            (columnObjMapping[columnkey])['date']='na'
                            (columnObjMapping[columnkey])[columnkey]=''
                        (columnObjMapping['status'])['status']='ApprovalPending'
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
    
        return return_object
               
    def get(request):
            try:
                return_object={}
                data = json.loads(request.body.decode('utf-8'))
                if 'empId' in data and isinstance(data['empId'],int) and data['empId'] and 'flowName' in data and data['flowName']:
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
                        formatedApprovalData = formating_response(approvaldata)
                        cursor.close()
                        return_object = {
                        "status":200,
                        "message":"Data retrieved successfully",
                        "result":formatedApprovalData
                         }
                else:
                     return_object = {
                        "status":400,
                        "message":"Invalid request body"
                         }
            except json.JSONDecodeError as e:
                return_object = {
                        "status":500,
                        "message":"Issue is beacause of "}
            return return_object
    
    def delete(request):
        try:
            return_object={}
            request = request if isinstance(request,dict) else json.loads(request.body)
            if 'approvalEngUniqueID_id' in request and request['approvalEngUniqueID_id'] and isinstance(request['approvalEngUniqueID_id'],int):
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
                    cursor.close()

                    return_object={
                        "status":200,
                        "message":deletedmessage
                    }
            else:
                 return_object={
                        "status":400,
                        "message":"Invalid Request Body"
                    }
        except json.JSONDecodeError as e:
            return_object = {
                        "status":500,
                        "message": e}

        return Response(return_object)
    


# class Applier(APIView):
#     def post(self,request):
#         try:
#             return_object={}
#             data = json.loads(request.body.decode('utf-8'))
#             data['empId']=int(data['empId'])
#             if not all(key in data for key in POST_PARAMETER_CHECK) or not isinstance(data['empId'],int) :
#                     return_object={
#                     "status":400,
#                     "message":"invalid request body"
#                     }    
#                     return return_object

#             empId = data.get('empId')
#             flowName = data.get('flowName',None)
#             description =data.get('description',None)
#             status =data.get('status',None)
#             approvalReason=data.get('approvalReason',None)
#             rejectionReason=data.get('rejectionReason',None)
#             justification =data.get('justification',None)
#             comment =data.get('comment',None)
#             remark=data.get('remark',None)
#             extraKeys=data.get('extrakeys')
#             LatestUpdateDate =datetime.datetime.now()
#             approvalId=0
    
#             Statusobj={"actionby":empId,"status":status,"date":LatestUpdateDate.isoformat(),"level":0}
#             ApprovalReasonobj ={"actionby":empId,"approvalReason":approvalReason,"date":LatestUpdateDate.isoformat(),"level":0}
#             RejectionReasonobj={"actionby":empId,"rejectionReason":rejectionReason,"date":LatestUpdateDate.isoformat(),"level":0}
#             Descriptionobj={"actionby":empId,"description":description,"date":LatestUpdateDate.isoformat(),"level":0}
#             Justificationobj ={"actionby":empId,"justification":justification,"date":LatestUpdateDate.isoformat(),"level":0}
#             Remarksobj ={"actionby":empId,"remark":remark,"date":LatestUpdateDate.isoformat(),"level":0}
#             Commentsobj ={"actionby":empId,"comment":comment,"date":LatestUpdateDate.isoformat(),"level":0}
            
#             columnObjMapping={'description':Descriptionobj,
#                               'status':Statusobj,
#                               'approvalReason':ApprovalReasonobj,
#                               'rejectionReason':RejectionReasonobj,
#                               'justification':Justificationobj,
#                               'comment':Commentsobj,
#                               'remark':Remarksobj}
#             if extraKeys:
#                 for columnkey in extraKeys.keys():
#                     if (columnkey in columnObjMapping.keys()) and type(extraKeys[columnkey])==dict:
#                         for extraKey in extraKeys[columnkey].keys():
#                             if not(extraKey in defaultkey) :
#                                 (columnObjMapping[columnkey])[extraKey]=extraKeys[columnkey][extraKey]
#                             else:
#                                 return_object={
#                                   "status":400,
#                                   "message":f"The keys in extrakeys request body sholud not be equal to {defaultkey}"
#                                   }  
#                     else:
#                         return_object={
#                                   "status":400,
#                                   "message":f"The keys in extrakeys request body sholud json object key format"
#                                   }  
        
#             statusStrObj=str(columnObjMapping['status'])
#             StatusArr=[json.loads(statusStrObj.replace("'", "\""))]
#             approvalReasonStrObj=str(columnObjMapping['approvalReason'])
#             ApprovalReasonArr=[json.loads(approvalReasonStrObj.replace("'", "\""))]
#             rejectionReasonStrObj=str(columnObjMapping['rejectionReason'])
#             RejectionReasonArr=[json.loads(rejectionReasonStrObj.replace("'", "\""))]
#             descriptionStrObj=str(columnObjMapping['description'])
#             DescriptionArr=[json.loads(descriptionStrObj.replace("'", "\""))]
#             justificationStrObj=str(columnObjMapping['justification'])
#             JustificationArr=[json.loads(justificationStrObj.replace("'", "\""))]
#             remarkStrObj=str(columnObjMapping['remark'])
#             RemarksArr=[json.loads(remarkStrObj.replace("'", "\""))]
#             commentStrObj=str(columnObjMapping['comment'])
#             CommentsArr=[json.loads(commentStrObj.replace("'", "\""))]
# #             # getting approval flow id from approval flow
#             with connection.cursor() as cursor:
#                 try:
#                     cursor.execute("BEGIN;")
#                     cursor.execute(' CALL get_flow(%s); ',[flowName])
             # Fetch all from the result cursor
#                     cursor.execute('FETCH ALL FROM "flow";')
#                     flowdata = cursor.fetchall()
                
#                     cursor.execute("COMMIT;")
#                     # Call the stored procedure
#                     # cursor.execute(' CALL public.get_hirarchy(%s,%s); ',[empId,flowName])
#                     #get_flow data approval_type, no. of approval
#                     NO_OF_APPROVALS=flowdata[0][2]
        
#                     APPROVAL_TYPE=flowdata[0][3] 
#                     # Call the stored procedure based on approval_type
#                     cursor.execute("BEGIN;")
#                     if APPROVAL_TYPE=="static":
#                         cursor.execute(' CALL public.get_static_hirarchy(%s,%s); ',[empId,flowdata[0][0]])
                
#                     elif APPROVAL_TYPE=="dynamic":
#                         cursor.execute(' CALL public.get_dynamic_hirarchy(%s); ',[str(empId)])
#                     else:
#                         return_object={
#                             "status":200,
#                             "message": "None approval type is matching"
#                         }
#                         return return_object
#                     # Fetch all from the result cursor
#                     cursor.execute('FETCH ALL FROM "hirarchy";')
#                     hirarchyData = cursor.fetchall()
            
#                     if NO_OF_APPROVALS:
#                         hirarchyData1=[[int(reporting[1]),i+1] for i,reporting in enumerate(hirarchyData) if i<NO_OF_APPROVALS]
                    
#                     # Commit the transaction
#                     cursor.execute("COMMIT;")
# #             # getting the approval hirarchy form hirarchy table
#                     for i in hirarchyData1:
#                         for columnkey in columnObjMapping.keys():
#                             (columnObjMapping[columnkey])['actionby']=i[0]
#                             (columnObjMapping[columnkey])['level']=i[1]
#                             (columnObjMapping[columnkey])['date']='na'
#                             (columnObjMapping[columnkey])[columnkey]=''
#                         (columnObjMapping['status'])['status']='ApprovalPending'
#                         statusStrObj=str(columnObjMapping['status'])
#                         approvalReasonStrObj=str(columnObjMapping['approvalReason'])
#                         rejectionReasonStrObj=str(columnObjMapping['rejectionReason'])
#                         descriptionStrObj=str(columnObjMapping['description'])
#                         justificationStrObj=str(columnObjMapping['justification'])
#                         remarkStrObj=str(columnObjMapping['remark'])
#                         commentStrObj=str(columnObjMapping['comment'])
#                         StatusArr.append(json.loads(statusStrObj.replace("'", "\"")))
#                         ApprovalReasonArr.append(json.loads(approvalReasonStrObj.replace("'", "\"")))
#                         RejectionReasonArr.append(json.loads(rejectionReasonStrObj.replace("'", "\"")))
#                         DescriptionArr.append(json.loads(descriptionStrObj.replace("'", "\"")))
#                         JustificationArr.append(json.loads(justificationStrObj.replace("'", "\"")))
#                         RemarksArr.append(json.loads(remarkStrObj.replace("'", "\"")))
#                         CommentsArr.append(json.loads(commentStrObj.replace("'", "\"")))
                    
                    
#                     cursor.execute('CALL public.insert_approval(%s, %s, %s, %s, %s, %s,%s, %s, %s, %s)', [json.dumps(StatusArr),json.dumps(ApprovalReasonArr),json.dumps(RejectionReasonArr),json.dumps(DescriptionArr),json.dumps(JustificationArr),json.dumps(RemarksArr),json.dumps(CommentsArr),LatestUpdateDate, flowName,approvalId])
#                     results = cursor.fetchall()
#                 finally:
#                       cursor.close()
#                       for item in results:
#                           approvalId = item[0]
#                       return_object={
#                 "status":200,
#                 "result":approvalId,
#                 "message":"success"
#             }
#         except json.JSONDecodeError as e:
#             return_object={
#                     "status":400,
#                     "message":"invalid request body"
#                     }  
    
#         return Response(return_object)
               
#     def get(self,request):
#             try:
#                 return_object={}
#                 data = json.loads(request.body.decode('utf-8'))
#                 if 'empId' in data and isinstance(data['empId'],int) and data['empId'] and 'flowName' in data and data['flowName']:
#                     EmpId=data.get('empId')
#                     FlowName=data.get('flowName')
#                     with connection.cursor() as cursor:
#                         cursor.execute("BEGIN;")
#                         # Call the stored procedure
#                         cursor.execute(' CALL get_approvaldata(%s,%s); ',[EmpId,FlowName])
#                         # Fetch all from the result cursor
#                         cursor.execute('FETCH ALL FROM "rs_approvaldata";')
#                         approvaldata = cursor.fetchall()
#                         # Commit the transaction
#                         cursor.execute("COMMIT;")
#                         formatedApprovalData = formating_response(approvaldata)
#                         cursor.close()
#                         return_object = {
#                         "status":200,
#                         "message":"Data retrieved successfully",
#                         "result":formatedApprovalData
#                          }
#                 else:
#                      return_object = {
#                         "status":400,
#                         "message":"Invalid request body"
#                          }
#             except json.JSONDecodeError as e:
#                 return_object = {
#                         "status":500,
#                         "message":"Issue is beacause of "}
#             return Response(return_object)
    
#     def delete(self,request):
#         try:
#             return_object={}
#             request = request if isinstance(request,dict) else json.loads(request.body)
#             if 'approvalEngUniqueID_id' in request and request['approvalEngUniqueID_id'] and isinstance(request['approvalEngUniqueID_id'],int):
#                 approvalEngUniqueID = request['approvalEngUniqueID_id']
#                 with connection.cursor() as cursor:
#                     cursor.execute("BEGIN;")
#                     # Call the stored procedure
#                     cursor.execute(' CALL get_delete_approvalstatus(%s,%s); ',[approvalEngUniqueID,0])
#                     # Fetch all from the result cursor
#                     cursor.execute('FETCH ALL FROM "selctedrow";')
#                     deletedmessage = cursor.fetchall()
#                     # Commit the transaction
#                     cursor.execute("COMMIT;")
#                     cursor.close()

#                     return_object={
#                         "status":200,
#                         "message":deletedmessage
#                     }
#             else:
#                  return_object={
#                         "status":400,
#                         "message":"Invalid Request Body"
#                     }
#         except json.JSONDecodeError as e:
#             return_object = {
#                         "status":500,
#                         "message": e}

#         return Response(return_object)
    