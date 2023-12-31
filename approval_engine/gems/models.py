from django.db import models

from approval_engine.models import ApprovalEngMasterData

# Create your models here.
class GemsProjectGeneration(models.Model):
    pgId = models.AutoField(primary_key=True)
    pgTitle = models.CharField(max_length=255,null=False)
    pgDescription = models.TextField()
    skils = models.JSONField()
    created_by = models.IntegerField(null=False)
    approvalEngUniqueID =models.ForeignKey(ApprovalEngMasterData,null=False,on_delete=models.CASCADE)
    class Meta:
        db_table="ProjectGeneration"


class GemsApplication(models.Model):
    applicantion_request_ID = models.AutoField(primary_key=True)
    applicantId = models.IntegerField(null=False)
    projectId =models.ForeignKey(GemsProjectGeneration,null=False,on_delete=models.CASCADE)
    request_raised_datetime =models.DateField()
    attachment =models.CharField(max_length=255)
    status=models.CharField(max_length=255)
    approvalEngUniqueID =models.ForeignKey(ApprovalEngMasterData,null=False,on_delete=models.CASCADE)
    isDeleted =models.BooleanField()
    class Meta:
        db_table="GemsApplication"


        