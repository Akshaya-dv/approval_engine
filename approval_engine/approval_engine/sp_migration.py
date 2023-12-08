from django.db import connection

def spCreation():

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

		get_hirarchy="""CREATE OR REPLACE PROCEDURE public.get_hirarchy(
	empid integer,
	flowname character varying,
	INOUT _result_cursor refcursor DEFAULT 'hirarchy'::refcursor)
LANGUAGE 'plpgsql'
AS $BODY$
		declare
		approvalflowid int;
		empHirarchy int;
		hirachy int;

		BEGIN
		EXECUTE 'SELECT "approvalFlowId" FROM public."ApprovalFlow" WHERE "approvalFlowName" = $1' 
		INTO approvalflowid USING flowname;
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
				'SELECT "approvalFlowId","approvalFlowName" FROM public."ApprovalFlow" WHERE "approvalFlowName" = $1' 
				using flowname;    
			ELSE
			open _result_cursor for execute
				'SELECT "approvalFlowId","approvalFlowName" FROM public."ApprovalFlow"';
			END IF;
		END;
		$BODY$;
		"""

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

			INSERT INTO public."ApprovalFlow"("approvalFlowName")
				VALUES (flowname);
				result:='inserted';

			END IF;

		END;
		$BODY$;
		"""

		insert_flow_hirarchy="""CREATE OR REPLACE PROCEDURE public.insert_flow_hirarchy(
			flowname character varying,
			empid integer,
			hirarchy integer,
			INOUT result text)
		LANGUAGE 'plpgsql'
		AS $BODY$
		declare
		approvalflowid int;
		empHirarchy int;

		BEGIN
		EXECUTE 'SELECT "approvalFlowId" FROM public."ApprovalFlow" WHERE "approvalFlowName" = $1' 
		INTO approvalflowid USING flowname;

			IF approvalflowid IS NOT NULL  THEN
			EXECUTE  'SELECT "hirarchy" FROM public."ApprovalFlowHirarchy"
				WHERE "approvalFlowId_id" =$1 AND "empId" = $2'
				into empHirarchy using approvalflowid,empId;

			IF empHirarchy IS NOT NULL  THEN
			result:='empIdAlreadyExistsInThisHirarchy';
			ELSE
			INSERT INTO public."ApprovalFlowHirarchy"(
				"empId", hirarchy, "approvalFlowId_id")
				VALUES ( empId, hirarchy, approvalflowid);
			result:='inserted';
			END IF;
			
			ELSE
				result:='flowNameDoesnotExists';
			END IF;

		END;
		$BODY$;"""

		update_flow_hirarchy="""CREATE OR REPLACE PROCEDURE public.update_flow_hirarchy(
			flowname character varying,
			new_empid integer,
			hirarchy integer,
			INOUT result text)
		LANGUAGE 'plpgsql'
		AS $BODY$
		declare
		approvalflowid int;
		empHirarchy int;

		BEGIN
		EXECUTE 'SELECT "approvalFlowId" FROM public."ApprovalFlow" WHERE "approvalFlowName" = $1' 
		INTO approvalflowid USING flowname;

			IF approvalflowid IS NOT NULL  THEN
			EXECUTE  'SELECT "empId" FROM public."ApprovalFlowHirarchy"
				WHERE "approvalFlowId_id" =$1 AND "hirarchy" = $2'
				into empHirarchy using approvalflowid,hirarchy;

			IF empHirarchy IS NOT NULL  THEN
			EXECUTE  'UPDATE public."ApprovalFlowHirarchy"
			SET  "empId"=$1
			WHERE "hirarchy"=$2 and "approvalFlowId_id"= $3;'
				using new_empid ,hirarchy,approvalflowid;
			result:='updated';
			ELSE
			result:='recordNotPresent';
			END IF;
			
			ELSE
				result:='flowNameDoesnotExists';
			END IF;

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

		spList=[get_approvaldata,
				get_delete_approvalstatus,
				get_hirarchy,
				insert_approval,
				get_approvalstatus,
				get_ApprovalMaster_AppEngUniqId1,
				update_approval_status,
				get_flow,
				get_flow_hirarchy,
				insert_flow,
				insert_flow_hirarchy,
				update_flow_hirarchy,
				get_approval_flow_status]


		cursor=connection.cursor()
		for sp in spList:
			cursor.execute(sp)


		cursor.close()
		return {"status":200,
			"message":{
				"DB":"DataBase connected successfully ",
				"SP":"Stored Procedures are created successfully"
			}}

# print("......dfy")
# # spCreation()


# post_approvaldata="""CREATE OR REPLACE PROCEDURE public.post_approvaldata(
# 	latestupdatedate timestamp with time zone,
# 	flowname character varying,
# 	empid integer,
# 	requestraiseddatetime timestamp with time zone,
# 	actiondatetime timestamp with time zone,
# 	status character varying,
# 	approvalreason character varying,
# 	rejectionreason character varying,
# 	description character varying,
# 	justification character varying,
# 	comment character varying,
# 	remark character varying,
# 	INOUT approvalid bigint)
# LANGUAGE 'plpgsql'
# AS $BODY$
# DECLARE
#      StatusArr text ;
# 	 ApprovalReasonArr text;
# 	 RejectionReasonArr text ;
# 	 DescriptionArr text;
# 	JustificationArr text ;
# 	RemarksArr text ;
# 	CommentsArr text ;
# 	Level integer;
# 	empIdExistsInAppHirarchy BOOLEAN;
# 	empHirarchy integer;
# 	rec_appHirarchy   record;
#     cur_appHirarchy  refcursor;
#     approvalflowid integer;
#     approval_id INTEGER;
#     varStatusArr jsonb;
# 	varApprovalReasonArr jsonb;
# 	varRejectionReasonArr jsonb;
# 	varDescriptionArr jsonb;
# 	varJustificationArr jsonb;
# 	varRemarksArr jsonb;
# 	varCommentsArr jsonb;
# BEGIN
# EXECUTE 'SELECT "approvalFlowId" FROM public."ApprovalFlow" WHERE "approvalFlowName" = $1' 
# INTO approvalflowid USING flowname;
# EXECUTE  'SELECT "hirarchy" FROM public."ApprovalFlowHirarchy"
#         WHERE "approvalFlowId_id" =$1 AND "empId" = $2'
# 		into empHirarchy using approvalflowid,empId;
		
# SELECT EXISTS (select empHirarchy) INTO empIdExistsInAppHirarchy;

#     IF empHirarchy IS NOT NULL  THEN
# 	   open cur_appHirarchy for execute
# 		'select "empId","hirarchy"
# 		from public."ApprovalFlowHirarchy"
# 		where "approvalFlowId_id"=$1 and "hirarchy">$2
# 		order by "hirarchy";' using approvalflowid,empHirarchy;
        
#     ELSE
# 	  open cur_appHirarchy for execute
# 		'select "empId","hirarchy"
# 		from public."ApprovalFlowHirarchy"
# 		where "approvalFlowId_id"=$1
# 		order by "hirarchy";' using approvalflowid;
     
#     END IF;

#      StatusArr:='[{"actionby":' || empId||',"status":"'||status||'","date":"'||current_timestamp||'","level":'||0||',"positioncode":"na"}';
# 	 ApprovalReasonArr :='[{"actionby":' || empId||',"approvalReason":"'||approvalReason||'","date":"'||current_timestamp||'","level":'||0||'}';
# 	 RejectionReasonArr  :='[{"actionby":' || empId||',"rejectionReason":"'||rejectionReason||'","date":"'||current_timestamp||'","level":'||0||'}';
# 	 DescriptionArr  :='[{"actionby":' || empId||',"description":"'||description||'","date":"'||current_timestamp||'","level":'||0||'}';
# 	 JustificationArr  :='[{"actionby":' || empId||',"justification":"'||justification||'","date":"'||current_timestamp||'","level":'||0||'}';
# 	 RemarksArr  :='[{"actionby":' || empId||',"remark":"'||remark||'","date":"'||current_timestamp||'","level":'||0||'}';
# 	 CommentsArr  :='[{"actionby":' || empId||',"comment":"'||comment||'","date":"'||current_timestamp||'","level":'||0||'}';
#      Level:=0;
#    loop
#     -- fetch row into the film
#       fetch cur_appHirarchy into rec_appHirarchy;
#     -- exit when no more row to fetch
#       exit when not found;
#        Level:=Level+1;
#     -- build the output
     
#          StatusArr := StatusArr || ',{"actionby":' || rec_appHirarchy."empId"||',"status":"ApprovalPending","date":"na","level":'||Level||',"positioncode":"na"}';
#          ApprovalReasonArr:=ApprovalReasonArr || ',{"actionby":' || rec_appHirarchy."empId"||',"approvalReason":"na","date":"na","level":'||Level||'}';
#          RejectionReasonArr:=RejectionReasonArr || ',{"actionby":' || rec_appHirarchy."empId"||',"rejectionReason":"na","date":"na","level":'||Level||'}';
#          DescriptionArr:=DescriptionArr || ',{"actionby":' || rec_appHirarchy."empId"||',"description":"na","date":"na","level":'||Level||'}';
#          JustificationArr:=JustificationArr || ',{"actionby":' || rec_appHirarchy."empId"||',"justification":"na","date":"na","level":'||Level||'}';
#          RemarksArr:=RemarksArr || ',{"actionby":' || rec_appHirarchy."empId"||',"remark":"na","date":"na","level":'||Level||'}';
#          CommentsArr:=CommentsArr || ',{"actionby":' || rec_appHirarchy."empId"||',"comment":"na","date":"na","level":'||Level||'}';
                  
#    end loop;
#    StatusArr := StatusArr || ']' ;
#          ApprovalReasonArr:=ApprovalReasonArr || ']' ;
#          RejectionReasonArr:=RejectionReasonArr || ']' ;
#          DescriptionArr:=DescriptionArr || ']' ;
#          JustificationArr:=JustificationArr || ']' ;
#          RemarksArr:=RemarksArr || ']' ;
#          CommentsArr:=CommentsArr ||']';
#    -- close the cursor
#    close cur_appHirarchy;
   
#    select StatusArr::jsonb into varStatusArr ;
#    select ApprovalReasonArr::jsonb into varApprovalReasonArr;
#    select RejectionReasonArr::jsonb into varRejectionReasonArr ;
#    select DescriptionArr::jsonb into varDescriptionArr ;
#    select JustificationArr::jsonb into varJustificationArr;
#    select RemarksArr::jsonb into varRemarksArr;
#    select CommentsArr::jsonb  into varCommentsArr ;
   
# 	-- Insert into ApprovalEngMasterData and get the approvalEngUniqueID
#     INSERT INTO public."ApprovalEngMasterData"(
#         "status", "approvalReason", "rejectionReason", "description", "justification", "remarks", "comments", "latestUpdateDate", "flow_id","isDeleted"
#     )
#     VALUES (
#         varstatusarr, varapprovalReasonarr, varrejectionReasonarr, vardescriptionarr, varjustificationarr, varremarksarr, varcommentsarr, latestUpdateDate, approvalflowid,False
#     )
#     RETURNING "approvalEngUniqueID" INTO approvalid;

# --     -- Insert int
# --     INSERT INTO public."EmpLeave"(
# --         "empId", "pendingActionFrom", "requestRaisedDatetime", "actionDatetime", "approvalEngUniqueID_id"
# --     )
# --     VALUES (
# --         empid,'[{}]', requestRaisedDatetime, actionDatetime, approvalid
# --     );
   
# END;
# $BODY$;"""
