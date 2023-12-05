from rest_framework import serializers
from .models import ApprovalEngMasterData,ApprovalFlow,ApprovalFlowHirarchies
from .leaveModel_to_be_deleted import EmpLeave
from .e_sepModel_to_be_deleted import EmpSep

class EmpLeaveSerializer(serializers.ModelSerializer):
  class Meta:
    model=EmpLeave
    fields=['empId','leaveRequestId','pendingActionFrom','requestRaisedDatetime','actionDatetime','approvalEngUniqueID']
class EmpSeparation(serializers.ModelSerializer):
   class Meta:
    model=EmpSep
    fields=[ 'empId','empSep_request_ID' ,'position_code','request_raised_by','request_raised_datetime','actual_request_datetime','lwd_per_policy','lwd_requested','np_days','np_shortfall_days','pending_action_from','isDeleted','recovery_amount','shortfall_days','tataGrp_joining_date','tmlGrp_joining_date','isPosted','attachment','approvalEngUniqueID']

    
class ApprovalEngMasterDataSerializer(serializers.ModelSerializer):
  class Meta:
    model=ApprovalEngMasterData
    fields=['approvalEngUniqueID','status','approvalReason','rejectionReason','description','justification','remarks','comments','latestUpdateDate','flow_id','isDeleted']

class ApprovalFlowSerializer(serializers.ModelSerializer):
    class Meta:
      model=ApprovalFlow
      fields=[ 'approvalFlowId','approvalFlowName']

    

class ApprovalFlowHirarchiesSerializer(serializers.ModelSerializer):
    class Meta:
        model=ApprovalFlowHirarchies
        fields=['empId','hirarchy','approvalFlowId']