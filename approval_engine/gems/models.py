from django.db import models

from approval_engine.models import ApprovalEngMasterData


# Create your models here.

class GemProjectGeneration(models.Model):
    pgId = models.AutoField(primary_key=True)
    pgTitle = models.CharField(max_length=255,null=False)
    pgDescription = models.TextField()
    skils = models.JSONField()
    approvalEngUniqueID =models.ForeignKey(ApprovalEngMasterData,null=False,on_delete=models.CASCADE)
        
    