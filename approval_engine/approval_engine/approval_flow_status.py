import json
from django.db import connection

from rest_framework.response import Response

from .common_function import formating_response
from .constants import *
from django.db import connection
from rest_framework.views import APIView

class ApprovalFlowStatus(APIView):
    def get(self,request):
        try:
            request = request if isinstance(request,dict) else json.loads(request.body)
            return_obj = {}
            if  'flowName' in request and request['flowName']:


                with connection.cursor() as cursor:
                    cursor.execute("BEGIN;")
                    # Call the stored procedure
                    cursor.execute(' CALL get_approval_flow_status(%s,%s); ',[request['flowName'],request.get('status')])
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

   