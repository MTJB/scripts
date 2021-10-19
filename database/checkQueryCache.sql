/*
-- Use this to clear the plan cache if you want to see top queries for a specific use case
DBCC FREEPROCCACHE;
GO
*/

SELECT TOP 1000
db.name,
qs.total_elapsed_time,
(qs.total_elapsed_time / 1000000) as total_elapsed_time_seconds,
((qs.total_elapsed_time/qs.execution_count) / 1000000) as av_elapsed_time_seconds,
qs.execution_count,
qs.last_worker_time,
qs.last_elapsed_time,
qs.last_logical_reads,
st.text,
qp.query_plan,
qs.*
FROM sys.dm_exec_query_stats qs
CROSS APPLY sys.dm_exec_sql_text(qs.plan_handle) st
CROSS APPLY sys.dm_exec_query_plan(qs.plan_handle) qp
INNER JOIN sys.databases db on db.database_id = st.dbid
WHERE db.name = DB_NAME()
AND st.text NOT LIKE '%sys.dm_exec_query_stats%' -- ignore this query!
-- AND st.text LIKE '%{WUERY_TEXT}%'
-- AND qs.last_execution_time > '2019-02-18 15:53:00'
ORDER BY qs.total_elapsed_time desc
