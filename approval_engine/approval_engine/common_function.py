import json
from .constants import defaultkey


def formating_response(approvaldata):
    formatedApprovalData=[]
    
    for data in approvaldata:
        objFormatedApprovalData={}
        objFormatedApprovalData['approvalEngUniqueID']=data[0]
        status=json.loads(data[1])
        
        approvalReason = json.loads(data[2])
        rejectionReason=json.loads(data[3])
        description =json.loads(data[4])
        justification =json.loads(data[5])
        remarks =json.loads(data[6])
        comments =json.loads(data[7])
        objFormatedApprovalData['latestUpdateDate'] =data[8]
        objFormatedApprovalData['flow']=data[9]
        objFormatedApprovalData['isDeleted']=data[10]
        
        for i in range(len(status)):
            
            objFormatedApprovalData[status[i]['actionby']]={
                "level":status[i]['level'],
                "status": status[i]['status'],
                "statusUpdatedDate":status[i]['date'],
                "approvalReason":approvalReason[i]['approvalReason'],
                "approvalReasonUpdatedDate":approvalReason[i]['date'],
                "rejectionReason":rejectionReason[i]['rejectionReason'],
                "rejectionReasonUpdatedDate":rejectionReason[i]['date'],
                "description":description[i]['description'],
                "descriptionUpdatedDate":description[i]['date'],
                "justification":justification[i]['justification'],
                "justificationUpdatedDate":justification[i]['date'],
                "remarks":remarks[i]['remark'],
                "remarksUpdatedDate":remarks[i]['date'],
                "comments":comments[i]['comment'],
                "commentsUpdatedDate":remarks[i]['date'],
            }
            for key in status[i].keys():
                if not(key in defaultkey):
                    (objFormatedApprovalData[status[i]['actionby']])[key]=status[i][key]
            for key in approvalReason[i].keys():
                if not(key in defaultkey):
                    (objFormatedApprovalData[status[i]['actionby']])[key]=approvalReason[i][key]
            for key in rejectionReason[i].keys():
                if not(key in defaultkey):
                    (objFormatedApprovalData[status[i]['actionby']])[key]=rejectionReason[i][key]
            for key in description[i].keys():
                if not(key in defaultkey):
                    (objFormatedApprovalData[status[i]['actionby']])[key]=description[i][key]
            for key in justification[i].keys():
                if not(key in defaultkey):
                    (objFormatedApprovalData[status[i]['actionby']])[key]=justification[i][key]
            for key in remarks[i].keys():
                if not(key in defaultkey):
                    (objFormatedApprovalData[status[i]['actionby']])[key]=remarks[i][key]
            for key in comments[i].keys():
                if not(key in defaultkey):
                    (objFormatedApprovalData[status[i]['actionby']])[key]=comments[i][key]
            
        formatedApprovalData.append(objFormatedApprovalData)
    return formatedApprovalData