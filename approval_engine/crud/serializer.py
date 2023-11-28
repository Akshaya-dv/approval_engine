from rest_framework import serializers
from .models import ApprovalEngMasterData,ApprovalFlow,ApprovalFlowHirarchies
from .leaveModel_to_be_deleted import EmpLeave
from .e_sepModel_to_be_deleted import EmpSep

class EmpLeaveSerializer(serializers.ModelSerializer):
  class Meta:
    model=EmpLeave
    fields=['empId','leaveRequestId','pendingActionFrom','requestRaisedDatetime','actionDatetime','approvalEngUniqueID']


class ApprovalEngMasterDataSerializer(serializers.ModelSerializer):
  class Meta:
    model=ApprovalEngMasterData
    fields=['approvalEngUniqueID','status','approvalReason','rejectionReason','description','justification','remarks','comments','latestUpdateDate','flow_id']

class ApprovalFlowSerializer(serializers.ModelSerializer):
    class Meta:
      model=ApprovalFlow
      fields=[ 'approvalFlowId','approvalFlowName']

    

class ApprovalFlowHirarchiesSerializer(serializers.ModelSerializer):
    class Meta:
        model=ApprovalFlowHirarchies
        fields=['empId','hirarchy','approvalFlowId']