from django.db import models
# Create your models here.
from django.db.models import JSONField
from .models import ApprovalEngMasterData

class EmpSep(models.Model):
    empId = models.IntegerField(null=False)
    empSep_request_ID = models.AutoField(primary_key=True)
    position_code = models.CharField(max_length=255)
    request_raised_by =models.CharField(max_length=255)
    request_raised_datetime =models.CharField(max_length=255)
    actual_request_datetime =models.CharField(max_length=255)
    lwd_per_policy =models.CharField(max_length=255)
    lwd_requested =models.CharField(max_length=255)
    np_days =models.CharField(max_length=255)
    np_shortfall_days =models.CharField(max_length=255)
    pending_action_from =models.CharField(max_length=255)
    isDeleted =models.CharField(max_length=255)
    recovery_amount =models.CharField(max_length=255)
    shortfall_days =models.CharField(max_length=255)
    tataGrp_joining_date =models.CharField(max_length=255)
    tmlGrp_joining_date =models.CharField(max_length=255)
    isPosted =models.CharField(max_length=255)
    attachment =models.CharField(max_length=255)
    approvalEngUniqueID =models.ForeignKey(ApprovalEngMasterData,null=False,on_delete=models.CASCADE)
    class Meta:
        db_table="EmpSep"