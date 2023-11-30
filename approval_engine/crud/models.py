from django.db import models
# Create your models here.
from django.db.models import JSONField



class ApprovalFlow(models.Model):
    approvalFlowId= models.IntegerField(primary_key=True,null=False)
    approvalFlowName= models.CharField(max_length=255)
    class Meta:
        db_table="ApprovalFlow"
    

class ApprovalFlowHirarchies(models.Model):
    empId = models.IntegerField(null=False)
    hirarchy=models.IntegerField()
    approvalFlowId=models.ForeignKey(ApprovalFlow,null=False,on_delete=models.CASCADE)
    class Meta:
        db_table="ApprovalFlowHirarchy"

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
    flow=models.ForeignKey(ApprovalFlow,null=False,on_delete=models.CASCADE)
    isDeleted=models.BooleanField(default=False)
    class Meta:
        db_table="ApprovalEngMasterData"



