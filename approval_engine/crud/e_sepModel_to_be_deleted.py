from django.db import models
# Create your models here.
from django.db.models import JSONField
from .models import ApprovalEngMasterData

class EmpSep(models.Model):
    empId = models.IntegerField(null=False)
    empSep_request_ID = models.AutoField(primary_key=True)
    position_code = models.CharField(max_length=255)
    request_raised_by =models.IntegerField()
    request_raised_datetime =models.DateField()
    actual_request_datetime =models.DateField()
    lwd_per_policy =models.CharField(max_length=255)
    lwd_requested =models.CharField(max_length=255)
    np_days =models.IntegerField()
    np_shortfall_days =models.IntegerField()
    pending_action_from =JSONField() 
    isDeleted =models.BooleanField()
    recovery_amount =models.IntegerField()
    shortfall_days =models.IntegerField()
    tataGrp_joining_date =models.DateField()
    tmlGrp_joining_date =models.DateField()
    isPosted =models.BooleanField()
    attachment =models.CharField(max_length=255)
    approvalEngUniqueID =models.ForeignKey(ApprovalEngMasterData,null=False,on_delete=models.CASCADE)
    class Meta:
        db_table="EmpSep"