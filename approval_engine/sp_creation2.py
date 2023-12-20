import psycopg2
from leave_services.settings import DB_NAME,DB_USER,DB_PASSWORD,DB_HOST,DB_PORT
connection = psycopg2.connect(
    database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port= DB_PORT
)
cursor = connection.cursor()
tablename='edp_employee_details'
empcolumnname='Perno'
reportingcolumnname='Reporting'

def create_sp():
    
    creating_view="""CREATE OR REPLACE PROCEDURE public.creating_view(
	IN tablename character varying,
	IN empcolumnname character varying,
	IN reportingcolumnname character varying,
	INOUT result text)
LANGUAGE 'plpgsql'
AS $BODY$
		BEGIN
		result:= 'create view  dynamicHirarchyView as 
select "'||empcolumnname||'" as empid,"'||reportingcolumnname||'" as reporting 
FROM "'||Tablename||'";';
execute result;
		END;
		
$BODY$;
	"""

    get_approvaldata="""CREATE OR REPLACE PROCEDURE public.get_approvaldata(
	_empid integer,
	_flowname text,
	INOUT _result_one refcursor DEFAULT 'rs_approvaldata'::refcursor)
LANGUAGE 'plpgsql'
AS $BODY$
		declare
		approvalflowid int;
		BEGIN
		EXECUTE 'SELECT "approvalFlowId" FROM public."ApprovalFlow" WHERE "approvalFlowName" = $1' 
		INTO approvalflowid USING _flowname;
		open _result_one for 
		SELECT "approvalEngUniqueID", status, "approvalReason", "rejectionReason", description, justification, remarks, comments, "latestUpdateDate", flow_id,"isDeleted"
		FROM public."ApprovalEngMasterData" WHERE exists( SELECT 1
														   FROM jsonb_array_elements(status) AS s
														   WHERE s->>'actionby' =_empid ::text 
														   and s->>'level' = '0' 
														  ) and "flow_id"=approvalflowid ;

		END;
		
$BODY$;
		"""
	
    get_delete_approvalstatus="""CREATE OR REPLACE PROCEDURE public.get_delete_approvalstatus(
			_approvalenguniqeid integer,
			_selectdelete integer,
			INOUT _result_one refcursor DEFAULT 'selctedrow'::refcursor)
		LANGUAGE 'plpgsql'
		AS $BODY$

		BEGIN
		if _selectDelete=1 then
		open _result_one for 
		SELECT * from public."ApprovalEngMasterData"
		where "approvalEngUniqueID"=_approvalEngUniqeId;
		end if;
		if _selectDelete=0 then
		UPDATE public."ApprovalEngMasterData"
			SET "isDeleted"=True
			where "approvalEngUniqueID"=_approvalEngUniqeId;
		open _result_one for 
		SELECT 'Record is soft Deleted';
		end if;

		END;
		$BODY$;"""
	
    get_static_hirarchy="""CREATE OR REPLACE PROCEDURE public.get_static_hirarchy(
	IN empid integer,
	IN approvalflowid integer,
	INOUT _result_cursor refcursor DEFAULT 'hirarchy'::refcursor)
LANGUAGE 'plpgsql'
AS $BODY$
		declare
	
		empHirarchy int;
		hirachy int;

		BEGIN
		
		EXECUTE  'SELECT "hirarchy" FROM public."ApprovalFlowHirarchy"
				WHERE "approvalFlowId_id" =$1 AND "empId" = $2'
				into empHirarchy using approvalflowid,empId;

			IF empHirarchy IS NOT NULL  THEN
						EXECUTE	'select "hirarchy"
				from public."ApprovalFlowHirarchy"
				where "approvalFlowId_id"=$1 and "hirarchy">$2
				order by "hirarchy";' into hirachy using approvalflowid,empHirarchy;
			if hirachy IS NOT NULL  THEN
			open _result_cursor for execute
				'select "empId","hirarchy"
				from public."ApprovalFlowHirarchy"
				where "approvalFlowId_id"=$1 and "hirarchy">$2
				order by "hirarchy";' using approvalflowid,empHirarchy;
			else
			open _result_cursor for execute
				'select "empId","hirarchy"
				from public."ApprovalFlowHirarchy"
				where "approvalFlowId_id"=$1 and "hirarchy"=$2
				order by "hirarchy";' using approvalflowid,empHirarchy;
			END IF;
				
			ELSE
			open _result_cursor for execute
				'select "empId","hirarchy"
				from public."ApprovalFlowHirarchy"
				where "approvalFlowId_id"=$1
				order by "hirarchy";' using approvalflowid;
			END IF;
		END;
		
$BODY$;"""
	
    insert_approval="""CREATE OR REPLACE PROCEDURE public.insert_approval(
			statusarr jsonb,
			approvalreasonarr jsonb,
			rejectionreasonarr jsonb,
			descriptionarr jsonb,
			justificationarr jsonb,
			remarksarr jsonb,
			commentsarr jsonb,
			latestupdatedate timestamp with time zone,
			flowname character varying,
			INOUT approvalid bigint)
		LANGUAGE 'plpgsql'
		AS $BODY$
		declare
		approvalflowid int;

		BEGIN
		EXECUTE 'SELECT "approvalFlowId" FROM public."ApprovalFlow" WHERE "approvalFlowName" = $1' 
		INTO approvalflowid USING flowname;
			-- Insert into ApprovalEngMasterData and get the approvalEngUniqueID
			INSERT INTO public."ApprovalEngMasterData"(
				"status", "approvalReason", "rejectionReason", "description", "justification", "remarks", "comments", "latestUpdateDate", "flow_id","isDeleted"
			)
			VALUES (
				statusarr, approvalReasonarr, rejectionReasonarr, descriptionarr, justificationarr, remarksarr, commentsarr, latestUpdateDate, approvalflowid,False
			)
			RETURNING "approvalEngUniqueID" INTO approvalid;

		END;
		$BODY$;"""
	
    get_approvalstatus="""CREATE OR REPLACE PROCEDURE public.get_approvalstatus(
	_actionby int,
	_flowname text,
	_status text,
	INOUT _result_one refcursor DEFAULT 'rs_approvaldata'::refcursor)
LANGUAGE 'plpgsql'
AS $BODY$
declare
		approvalflowid int;
		BEGIN
		EXECUTE 'SELECT "approvalFlowId" FROM public."ApprovalFlow" WHERE "approvalFlowName" = $1' 
		INTO approvalflowid USING _flowname;
			 IF _status is not null then
			 open _result_one for 
		        SELECT "approvalEngUniqueID", status, "approvalReason", "rejectionReason", description, justification, remarks, comments, "latestUpdateDate", flow_id, "isDeleted"
				FROM public."ApprovalEngMasterData" 
				WHERE "flow_id" =approvalflowid AND exists( SELECT 1
														   FROM jsonb_array_elements(status) AS s
														   WHERE s->>'actionby' =_actionby ::text 
														   and s->>'level' <> '0' 
														   and s->>'status'=_status );
			
			 ELSE
			 open _result_one for 
		        SELECT "approvalEngUniqueID", status, "approvalReason", "rejectionReason", description, justification, remarks, comments, "latestUpdateDate", flow_id, "isDeleted"
				FROM public."ApprovalEngMasterData" 
				WHERE "flow_id" =approvalflowid AND exists( SELECT 1 
														   FROM jsonb_array_elements(status) AS s 
														   WHERE s->>'actionby' =_actionby ::text 
														   and s->>'level' <> '0');
			 END IF;

		END;
		
$BODY$;
		"""
	
    get_ApprovalMaster_AppEngUniqId1="""CREATE OR REPLACE PROCEDURE public.get_ApprovalMaster_AppEngUniqId(
		_approvalenguniqeid integer,
		inout _cursor refcursor 
		DEFAULT 'rs_approvaldata'::refcursor
		)  
		LANGUAGE 'plpgsql'
		AS $BODY$
		begin
			open _cursor for
		SELECT "approvalEngUniqueID", "status", 
		"approvalReason", "rejectionReason", "description", 
		"justification", "remarks", "comments", "latestUpdateDate", 
		"flow_id","isDeleted" from public."ApprovalEngMasterData"
		where "approvalEngUniqueID"=_approvalenguniqeid;
		END;
		$BODY$;"""
	
    update_approval_status="""CREATE OR REPLACE PROCEDURE public.update_approval_status(IN _approvalenguniqueid integer, IN _status jsonb, IN _approvalreason jsonb, IN _rejectionreason jsonb, IN _description jsonb, IN _justification jsonb, IN _remarks jsonb, IN _comments jsonb)
		LANGUAGE plpgsql
		AS $procedure$
			BEGIN
			update "ApprovalEngMasterData" set "status" = _status::jsonb,
			"approvalReason" = _approvalReason::jsonb,
			"rejectionReason" = _rejectionReason::jsonb,
			"description" = _description::jsonb,
			"justification" = _justification::jsonb,
			"remarks" = _remarks::jsonb,
			"comments" = _comments::jsonb 

		where "approvalEngUniqueID" = _approvalEngUniqueID;
			END;
		$procedure$
		;
		"""
	
    get_flow="""CREATE OR REPLACE PROCEDURE public.get_flow(
			flowname character varying,
			INOUT _result_cursor refcursor DEFAULT 'flow'::refcursor)
		LANGUAGE 'plpgsql'
		AS $BODY$
		BEGIN
			IF flowname IS NOT NULL  THEN
			open _result_cursor for execute
				'SELECT "approvalFlowId","approvalFlowName", "noOfApproval","approvalFlowType" FROM public."ApprovalFlow" WHERE "approvalFlowName" = $1' 
				using flowname;    
			ELSE
			open _result_cursor for execute
				'SELECT "approvalFlowId","approvalFlowName", "noOfApproval","approvalFlowType" FROM public."ApprovalFlow"';
			END IF;
		END;
		$BODY$;
		"""
	
    get_dynamic_hirarchy="""CREATE OR REPLACE PROCEDURE public.get_dynamic_hirarchy(
	IN _perno text,
	INOUT _result_one refcursor DEFAULT 'hirarchy'::refcursor)
LANGUAGE 'plpgsql'
AS $BODY$
    begin
            open _result_one for
                WITH RECURSIVE cte_query        
                AS                      
                (
                select x."empid",x."reporting" from "dynamichirarchyview" x where x."empid"=_Perno              
                UNION ALL  
                select x1."empid",x1."reporting" from "dynamichirarchyview" x1   
                INNER JOIN cte_query c ON c."reporting" = x1."empid"
                )
            Select * from cte_query;
 
    END;
$BODY$;"""

    get_flow_hirarchy="""CREATE OR REPLACE PROCEDURE public.get_flow_hirarchy(
			flowname character varying,
			INOUT _result_cursor refcursor DEFAULT 'flow_hirarchy'::refcursor)
		LANGUAGE 'plpgsql'
		AS $BODY$

		declare
		approvalflowid int;

		BEGIN
		EXECUTE 'SELECT "approvalFlowId" FROM public."ApprovalFlow" WHERE "approvalFlowName" = $1' 
		INTO approvalflowid USING flowname;

			IF approvalflowid IS NOT NULL  THEN
			open _result_cursor for execute
				'select "empId","hirarchy","approvalFlowId_id"
				from public."ApprovalFlowHirarchy"
				where "approvalFlowId_id"=$1
				order by "hirarchy";' using approvalflowid;  
			ELSE
			open _result_cursor for
				SELECT 'flownameNotPresent';
			END IF;
		END;
		$BODY$;"""
	
    insert_flow="""CREATE OR REPLACE PROCEDURE public.insert_flow(
			flowname character varying,
	noOfApproval int,
	approvalFlowType character varying,
			INOUT result text)
		LANGUAGE 'plpgsql'
		AS $BODY$
		declare
		approvalflowid int;

		BEGIN
		EXECUTE 'SELECT "approvalFlowId" FROM public."ApprovalFlow" WHERE "approvalFlowName" = $1' 
		INTO approvalflowid USING flowname;

			IF approvalflowid IS NOT NULL  THEN
			result:='exist';	
			ELSE
			INSERT INTO public."ApprovalFlow"("approvalFlowName","noOfApproval","approvalFlowType")
				VALUES (flowname,noOfApproval,approvalFlowType);
				result:='inserted';

			END IF;
		END;
		$BODY$;"""
    insert_flow_hirarchy="""CREATE OR REPLACE PROCEDURE public.insert_flow_hirarchy(
		IN flowid integer,
		IN empid integer,
		IN hirarchy integer,
		INOUT result text)
		LANGUAGE 'plpgsql'
		AS $BODY$
				declare
				empHirarchy int;
				BEGIN
			
					EXECUTE  'SELECT "hirarchy" FROM public."ApprovalFlowHirarchy"
						WHERE "approvalFlowId_id" =$1 AND "empId" = $2'
						into empHirarchy using flowid,empId;
		
					IF empHirarchy IS NOT NULL  THEN
					result:='empIdAlreadyExistsInThisHirarchy';
					ELSE
					INSERT INTO public."ApprovalFlowHirarchy"(
						"empId", hirarchy, "approvalFlowId_id")
						VALUES ( empId, hirarchy, flowid);
					result:='inserted';
					END IF;

				END;	
	    $BODY$;"""

    update_flow="""CREATE OR REPLACE PROCEDURE public.update_flow(
	IN flowname character varying,
	IN noofapproval integer,
	IN approvalflowtype character varying,
	INOUT result text)
LANGUAGE 'plpgsql'
AS $BODY$
		declare
		approvalflowid int;

		BEGIN
		EXECUTE 'SELECT "approvalFlowId" FROM public."ApprovalFlow" WHERE "approvalFlowName" = $1' 
		INTO approvalflowid USING flowname;

			IF approvalflowid IS NOT NULL  THEN
			UPDATE public."ApprovalFlow"
	SET  "noOfApproval"=noofapproval, "approvalFlowType"=approvalflowtype
	WHERE  "approvalFlowName"=flowname;
				result:='updated';
    				
    			ELSE
    		result:='doesNotExist';
    
    			END IF;
    
    		END;
    		
        $BODY$;"""

    update_flow_hirarchy="""CREATE OR REPLACE PROCEDURE public.update_flow_hirarchy(
	IN flowname character varying,
	IN new_empid integer,
	IN hirarchy integer,
	INOUT result text)
LANGUAGE 'plpgsql'
AS $BODY$
		declare
		approvalflowid int;
		empHirarchy int;
		empAlreadyExist int;
		BEGIN
		EXECUTE 'SELECT "approvalFlowId" FROM public."ApprovalFlow" WHERE "approvalFlowName" = $1' 
		INTO approvalflowid USING flowname;

			IF approvalflowid IS NOT NULL  THEN
			EXECUTE  'SELECT "empId" FROM public."ApprovalFlowHirarchy"
				WHERE "approvalFlowId_id" =$1 AND "hirarchy" = $2'
				into empHirarchy using approvalflowid,hirarchy;

			IF empHirarchy IS NOT NULL  THEN
			EXECUTE  'SELECT "empId" FROM public."ApprovalFlowHirarchy"
				WHERE "approvalFlowId_id" =$1 AND "empId" = $2'
				into empAlreadyExist using approvalflowid,new_empid;
			
			if empAlreadyExist is not null then 
			result:='thisEmpIdAlreadyPresent';
            
			ELSE
			EXECUTE  'UPDATE public."ApprovalFlowHirarchy"
			SET  "empId"=$1
			WHERE "hirarchy"=$2 and "approvalFlowId_id"= $3;'
			using new_empid ,hirarchy,approvalflowid;
			result:='updated';
			END IF;
			
			ELSE
			result:='recordNotPresent';
			END IF;
			
			ELSE
				result:='flowNameDoesnotExists';
			END IF;

		END;
		
$BODY$;"""
	
    delete_flow_hirarchy="""CREATE OR REPLACE PROCEDURE public.delete_flow_hirarchy(
	IN flowid int,
	INOUT result text)
LANGUAGE 'plpgsql'
AS $BODY$
		BEGIN
	DELETE FROM public."ApprovalFlowHirarchy"
	WHERE "approvalFlowId_id"=flowid;
    result:='deletesuccessfully';
		END;
$BODY$;"""

    get_approval_flow_status="""CREATE OR REPLACE PROCEDURE public.get_approval_flow_status(
	_flowname text,
	_status text,
	INOUT _result_one refcursor DEFAULT 'rs_approvaldata'::refcursor)
LANGUAGE 'plpgsql'
AS $BODY$
declare
		approvalflowid int;
		maxhirarchy int;
		BEGIN
		EXECUTE 'SELECT "approvalFlowId" FROM public."ApprovalFlow" WHERE "approvalFlowName" = $1  group by "approvalFlowId";' 
		INTO  approvalflowid USING _flowname;
		EXECUTE 'select max("hirarchy")
				from public."ApprovalFlowHirarchy"
				where "approvalFlowId_id"=$1;'
				INTO maxhirarchy using approvalflowid;
				
			 IF _status is not null then
			 open _result_one for 
		        SELECT "approvalEngUniqueID", status, "approvalReason", "rejectionReason", description, justification, remarks, comments, "latestUpdateDate", flow_id, "isDeleted"
				FROM public."ApprovalEngMasterData" 
				WHERE "flow_id" =approvalflowid AND exists( SELECT 1
														   FROM jsonb_array_elements(status) AS s
														   WHERE
														    s->>'level' = maxhirarchy::text 
														   and s->>'status'=_status );
			
			 ELSE
			 open _result_one for 
		        SELECT "approvalEngUniqueID", status, "approvalReason", "rejectionReason", description, justification, remarks, comments, "latestUpdateDate", flow_id, "isDeleted"
				FROM public."ApprovalEngMasterData" 
				WHERE "flow_id" =approvalflowid ;
			 END IF;

		END;
		
$BODY$;"""
	
    spList=[creating_view,
            get_approvaldata,
				get_delete_approvalstatus,
                get_static_hirarchy,
                get_dynamic_hirarchy,
				insert_approval,
				get_approvalstatus,
				get_ApprovalMaster_AppEngUniqId1,
				update_approval_status,
				get_flow,
				get_flow_hirarchy,
				insert_flow,
				insert_flow_hirarchy,
                update_flow,
				update_flow_hirarchy,
                delete_flow_hirarchy,
				get_approval_flow_status]

    for sp in spList:
        cursor.execute(sp)
        cursor.execute('commit;')
    cursor.execute('call creating_view(%s,%s,%s,%s)',[tablename,empcolumnname,reportingcolumnname,''])
    cursor.close()

    return {"status":200,
        "message":{
            "DB":"DataBase connected successfully ",
            "SP":"Stored Procedures are created successfully"
        }}

status = create_sp()
print(status)