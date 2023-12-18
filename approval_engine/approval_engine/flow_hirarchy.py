import json
from rest_framework.views import APIView
from django.http import JsonResponse
from django.db import connection
from approval_engine.models import ApprovalFlow,ApprovalFlowHirarchies

class FlowName(APIView):
    def get(self,request):
        try:
            request = request if isinstance(request,dict) else json.loads(request.body)
            return_object={}
       
            with connection.cursor() as cursor:
                cursor.execute("BEGIN;")
                # Call the stored procedure
                cursor.execute(' CALL get_flow(%s); ',[request.get('flowName')])
                # Fetch all from the result cursor
                cursor.execute('FETCH ALL FROM "flow";')
                flowdata = cursor.fetchall()
                # Commit the transaction
                cursor.execute("COMMIT;")
                cursor.close()
            if flowdata:
                formatedflowdata=[]
                for i in flowdata:
                    flow={}
                    flow['approvalFlowId']=i[0]
                    flow['approvalFlowName']=i[1]
                    flow['noOfApproval']=i[2]
                    flow['approvalFlowType']=i[3]
                    formatedflowdata.append(flow)
                return_object={
                    "status":200,
                    "message":"flowname retrieved successfully",
                    "result":formatedflowdata
                }
            else:
                 return_object={
                    "status":200,
                    "message":"Please check the flowname this flowname is not present in database"
                }
        
        except (Exception) as error:
            print("Flowname get api issue is "+str(error))
            return_object={
                "status":500,
                "message":"Internal server error "+str(error),
            }
        return JsonResponse(return_object)
             
    def post(self,request):
        try:
            request = request if isinstance(request,dict) else json.loads(request.body)
            return_object={}
                     
            if request.get('flowName') and 'noOfApproval' in request and  request['noOfApproval']>=1 and  isinstance(request['noOfApproval'],int)  and request.get('approvalFlowType') :
                if request.get('approvalFlowType','na').lower()=='static':
                    approvalFlowType='static'
                elif request.get('approvalFlowType','na').lower()=='dynamic':
                    approvalFlowType='dynamic'
                else :
                    return_object={
                    "status":400,
                    "message":'Invalid request body, "approvalFlowType" must be either "static" or "dynamic" '
                }
                    return JsonResponse(return_object)

                with connection.cursor() as cursor:
                    try:
                        results=''    
                        cursor.execute('CALL public.insert_flow(%s,%s,%s,%s)', [request.get('flowName'),request.get('noOfApproval'),approvalFlowType,results])
                        results = cursor.fetchall() 
                    except: 
                        return_object={
                            "status":500,
                            "message":"Issue is "+str(error)
                        }
                    finally:
                          cursor.close()
                if results[0][0]=='exist':
                    return_object={
                    "status":200,
                    "message":"flowname already exist"
                }    
                elif results[0][0]=='inserted':
                    return_object={
                    "status":200,
                    "message":"flowname inserted successfully"
                }         
            else:
                return_object={
                    "status":400,
                    "message":"Invalid request body"
                }    
        except (Exception) as error:
            print("Flow Name insertion issue "+str(error))
            return_object={
                "status":500,
                "message":"Issue is "+str(error)
            }
        return JsonResponse(return_object)

    def put(self,request):
        try:
            request = request if isinstance(request,dict) else json.loads(request.body)
            return_object={}
                     
            if request.get('flowName') and 'noOfApproval' in request and  request['noOfApproval']>=1 and  isinstance(request['noOfApproval'],int)  and request.get('approvalFlowType') :
                if request.get('approvalFlowType','na').lower()=='static':
                    approvalFlowType='static'
                elif request.get('approvalFlowType','na').lower()=='dynamic':
                    approvalFlowType='dynamic'
                else :
                    return_object={
                    "status":400,
                    "message":'Invalid request body, "approvalFlowType" must be either "static" or "dynamic" '
                }
                    return JsonResponse(return_object)

                with connection.cursor() as cursor:
                    try:
                        results=''    
                        cursor.execute('CALL public.update_flow(%s,%s,%s,%s)', [request.get('flowName'),request.get('noOfApproval'),approvalFlowType,results])
                        results = cursor.fetchall() 
                    except: 
                        return_object={
                            "status":500,
                            "message":"Issue is "+str(error)
                        }
                    finally:
                          cursor.close()
                if results[0][0]=='doesNotExist':
                    return_object={
                    "status":200,
                    "message":"flowname does not exist to update"
                }    
                elif results[0][0]=='updated':
                    return_object={
                    "status":200,
                    "message":"flowname updated successfully"
                }         
            else:
                return_object={
                    "status":400,
                    "message":"Invalid request body"
                }    
        except (Exception) as error:
            print("Flow Name insertion issue "+str(error))
            return_object={
                "status":500,
                "message":"Issue is "+str(error)
            }
        return JsonResponse(return_object)

class Hirarchy(APIView):
    def get(self,request):
        try:
            request = request if isinstance(request,dict) else json.loads(request.body)
            return_object={} 
            if request.get('flowName'):
                with connection.cursor() as cursor:
                    cursor.execute("BEGIN;")
                    # Call the stored procedure
                    cursor.execute(' CALL get_flow_hirarchy(%s); ',[request.get('flowName')])
                    # Fetch all from the result cursor
                    cursor.execute('FETCH ALL FROM "flow_hirarchy";')
                    flowdata = cursor.fetchall()
                  
                    # Commit the transaction
                    cursor.execute("COMMIT;")
                    cursor.close()
                if flowdata:
                    if flowdata[0][0]=='flownameNotPresent':
                        return_object={
                        "status":200,
                        "message":"Please check the flowname this flowname is not present in database"
                    }
                    else:
                       
                        formatedflowdata=[]
                        for i in flowdata:
                            flow={}
                            flow['approvalFlowId']=i[2]
                            flow['approvalFlowHirarchy']=i[1]
                            flow['empId']=i[0]
                            formatedflowdata.append(flow)
                        return_object={
                            "status":200,
                            "message":"flowname retrieved successfully",
                            "result":formatedflowdata
                        }

                else:
                    return_object={
                        "status":200,
                        "message":"The hirarchy is not present for the entered flowname"
                    }
                  
            else:
                return_object={
                    "status":400,
                    "message":"Invalid request body"
                }    
                
        except (Exception) as error:
            print("Flow Name insertion issue "+str(error))
            return_object={
                "status":500,
                "message":"Issue is "+str(error)
            }
        return JsonResponse(return_object)
    
    def put(self,request):
        try:
            request = request if isinstance(request,dict) else json.loads(request.body)
            return_object={} 
            if request.get('flowName') and request.get('empId') and request.get('hirarchy'):
                with connection.cursor() as cursor:
                    try:
                        results=''
                        cursor.execute('CALL public.update_flow_hirarchy(%s,%s,%s,%s)', [request.get('flowName'),request.get('empId'),request.get('hirarchy'),results])
                        results = cursor.fetchall()
                   
                    finally:
                          cursor.close()
                if results[0][0]=='updated':
                    return_object={
                        "status":200,
                        "message":"flow hirarchy updated successfully"
                    }
                elif results[0][0]=='recordNotPresent':
                    return_object={
                        "status":200,
                        "message":"flowname doesnot have the particular hirarchy to update  "
                    }
                elif results[0][0]=='flowNameDoesnotExists':
                    return_object={
                        "status":200,
                        "message":"Please check the flowname this flowname is not present in database "
                    }
            
        except (Exception) as error:
            print("Flow Name insertion issue "+str(error))
            return_object={
                "status":500,
                "message":"Issue is "+str(error)
            }
        return JsonResponse(return_object)
   
    def post(self,request):
        try:
            request = request if isinstance(request,dict) else json.loads(request.body)
            return_object={}
            if request.get('hirarchy') and len(request.get('hirarchy'))>0 and request.get('flowName'):
                with connection.cursor() as cursor:
                
                    cursor.execute("BEGIN;")
                    cursor.execute(' CALL get_flow(%s); ',[request.get('flowName')])
             # Fetch all from the result cursor
                    cursor.execute('FETCH ALL FROM "flow";')
                    flowdata = cursor.fetchall()
                    
                    cursor.execute("COMMIT;")
                    if flowdata and flowdata[0][3]=='static':  
                        ApprovalFlowid=flowdata[0][0]
                        NO_OF_APPROVALS=flowdata[0][2]
                        insert_list=[]
                        for hirarchy in request.get('hirarchy'):
                            if hirarchy.get('empId') and hirarchy.get('hirarchy') and NO_OF_APPROVALS>=hirarchy.get('hirarchy'):
                                    results=''
                                    cursor.execute('CALL public.insert_flow_hirarchy(%s,%s,%s,%s)', [ApprovalFlowid,hirarchy.get('empId'),hirarchy.get('hirarchy'),results])
                                    results = cursor.fetchall()
                            else:
                                return_object= {
                                    "status":400,
                                    "message":"Invalid request body or approval hirarchy must be less than or equalto no of approval specified in the flow "
                                }
                                return JsonResponse(return_object)
                            
                        if results[0][0]=='inserted':
                            return_object={
                                "status":200,
                                "message":"Hirarchy inserted successfully"
                            }
                        elif results[0][0]=='empIdAlreadyExistsInThisHirarchy':
                            return_object={
                                "status":200,
                                "message":"Employeeid is already present in the hirarchy  "
                            }
                    else :
                        return_object={
                            "status":400,
                            "message":"Please check the flowname this flowname is not present in database or flowname is dynamic "
                        }
               
            else:
                return_object={
                        "status":400,
                        "message":"Invalid request body"
                    }
        except (Exception) as error:
            print("Hirarchy post method issue is "+str(error))
            return_object={
                        "status":500,
                        "message":"Internal server error"
                    }
        return JsonResponse(return_object)

# class FlowName(APIView):
#     def get(self,request):
#         try:
#             request = request if isinstance(request,dict) else json.loads(request.body)
#             return_object={}
#             if request.get('flowName'):
#                 flow=list(ApprovalFlow.objects.filter(approvalFlowName=request.get('flowName')).values())
#                 return_object={
#                     "status":200,
#                     "message":"flowname retrieved successfully",
#                     "result":flow
#                 }
#             else:
#                 flow=list(ApprovalFlow.objects.all().values())
#                 return_object={
#                     "status":200,
#                     "message":"flowname retrieved successfully",
#                     "result":flow
#                 }
                
#         except (Exception) as error:
#             print("Flowname get api issue is "+str(error))
#             return_object={
#                 "status":500,
#                 "message":"Internal server error "+str(error),
#             }
#         return JsonResponse(return_object)
                
#     def post(self,request):
#         try:
#             request = request if isinstance(request,dict) else json.loads(request.body)
#             return_object={}
#             if request.get('flowName'):
#                 flow_exist=ApprovalFlow.objects.filter(approvalFlowName=request.get('flowName')).values()
#                 if flow_exist:
#                     return_object={
#                     "status":200,
#                     "message":"flowname already exist"
#                 }    
#                 else:
#                     ApprovalFlow(approvalFlowName=request.get('flowName')).save()
#                     return_object={
#                     "status":200,
#                     "message":"flowname inserted successfully"
#                 }    
                    
#             else:
#                 return_object={
#                     "status":400,
#                     "message":"Invalid request body"
#                 }    
#         except (Exception) as error:
#             print("Flow Name insertion issue "+str(error))
#             return_object={
#                 "status":500,
#                 "message":"Issue is "+str(error)
#             }
#         return JsonResponse(return_object)

# class Hirarchy(APIView):
#     def get(self,request):
#         try:
#             request = request if isinstance(request,dict) else json.loads(request.body)
#             return_object={} 
#             if request.get('flowName'):
#                 flow_id=ApprovalFlow.objects.filter(approvalFlowName=request.get('flowName')).values_list('approvalFlowId').first()
#                 hirarchy= list(ApprovalFlowHirarchies.objects.filter(approvalFlowId=flow_id[0]).values())
#                 return_object={
#                     "status":200,
#                     "message":"flowname inserted successfully",
#                     "result":hirarchy
#                 }    
#             else:
#                 return_object={
#                     "status":400,
#                     "message":"Invalid request body"
#                 }    
                
#         except (Exception) as error:
#             print("Flow Name insertion issue "+str(error))
#             return_object={
#                 "status":500,
#                 "message":"Issue is "+str(error)
#             }
#         return JsonResponse(return_object)
#     def post(self,request):
#         try:
#             request = request if isinstance(request,dict) else json.loads(request.body)
#             return_object={} 
#             if request.get('hirarchy') and len(request.get('hirarchy'))>0 and request.get('flowName'):
#                 flow_id=ApprovalFlow.objects.filter(approvalFlowName=request.get('flowName')).values_list('approvalFlowId').first()[0]
#                 if flow_id or flow_id==0:
#                     insert_list=[]
#                     for hirarchy in request.get('hirarchy'):
#                         if hirarchy.get('empId') and hirarchy.get('hirarchy'):
#                             insert_list.append(ApprovalFlowHirarchies(empId=request.get('empId'),hirarchy=request.get('hirarchy'),approvalFlowId=flow_id))
#                     ApprovalFlowHirarchies.objects.bulk_create(insert_list)
#                     return_object={
#                     "status":200,
#                     "message":"FLow inserted successfully"
#                     }
#                 else:
#                     return_object={
#                         "status":200,
#                         "message":"FLow doesn't exist"
#                     }
#             else:
#                 return_object={
#                         "status":400,
#                         "message":"Invalid request body"
#                     }
#         except (Exception) as error:
#             print("Hirarchy post method issue is "+str(error))
#             return_object={
#                         "status":500,
#                         "message":"Internal server error"
#                     }
#         return JsonResponse(return_object)
    
#     def put(self,request):
#         try:
#             request = request if isinstance(request,dict) else json.loads(request.body)
#             return_object={} 
#             if request.get('flowName') and request.get('empId') and request.get('hirarchy'):
#                 flow_id=ApprovalFlow.objects.filter(approvalFlowName=request.get('flowName')).values_list('approvalFlowId').first()
                
#                 ApprovalFlowHirarchies.objects.filter(approvalFlowId=flow_id[0],hirarchy=request.get('hirarchy')).update(empId=request.get('empId'))
#                 return_object={
#                     "status":200,
#                     "message":"flowname updated successfully"
#                 }
            
#         except (Exception) as error:
#             print("Flow Name insertion issue "+str(error))
#             return_object={
#                 "status":500,
#                 "message":"Issue is "+str(error)
#             }
#         return JsonResponse(return_object)
