from django.db import models
# Create your models here.
from django.db.models import JSONField
from approval_engine.models import ApprovalEngMasterData

class EmpLeave(models.Model):
    empId = models.IntegerField(null=False)
    leaveRequestId = models.AutoField(primary_key=True)
    pendingActionFrom = models.CharField(max_length=255)
    requestRaisedDatetime =models.DateTimeField(auto_now=True)
    actionDatetime =models.DateTimeField(null=True)
    approvalEngUniqueID =models.ForeignKey(ApprovalEngMasterData,null=False,on_delete=models.CASCADE)
    class Meta:
        db_table="EmpLeave"
        