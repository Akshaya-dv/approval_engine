from django.db import models
# Create your models here.
from django.db.models import JSONField

class ApprovalEngMasterData(models.Model):
    approvalEngUniqueID =models.AutoField(primary_key=True)
    status=JSONField() 
    approvalReason = JSONField()
    rejectionReason=JSONField()
    description =JSONField()
    justification =JSONField()
    remarks =JSONField()
    comments =JSONField()
    latestUpdateDate =models.DateTimeField(max_length=255) 
    flowName=models.CharField(null=False,blank=False,default='unassigned')
    class Meta:
        db_table="ApprovalEngMasterData"

class EmpLeave(models.Model):
    empId = models.CharField(max_length=255)
    leaveRequestId = models.AutoField(primary_key=True)
    pendingActionFrom = models.CharField(max_length=255)
    requestRaisedDatetime =models.DateTimeField(auto_now=True)
    actionDatetime =models.DateTimeField(null=True)
    approvalEngUniqueID =models.ForeignKey(ApprovalEngMasterData,null=False,on_delete=models.CASCADE)
    class Meta:
        db_table="EmpLeave"

class ApprovalFlow(models.Model):
    approvalFlowId= models.IntegerField(primary_key=True,null=False)
    approvalFlowName= models.CharField(255)
    class Meta:
        db_table="ApprovalFlow"
    

class ApprovalFlowHirarchies(models.Model):
    empId = models.CharField(max_length=255)
    hirarchy=models.IntegerField()
    approvalFlowId=models.ForeignKey(ApprovalFlow,null=False,on_delete=models.CASCADE)
    class Meta:
        db_table="ApprovalFlowHirarchy"


