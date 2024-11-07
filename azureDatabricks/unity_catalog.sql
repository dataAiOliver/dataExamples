-- get the current user
SELECT CURRENT_USER() AS user_name;

-- get current metastore
SELECT CURRENT_METASTORE();

-- Who can access this table?
SELECT DISTINCT(grantee) AS `ACCESSIBLE BY`
FROM system.information_schema.table_privileges
WHERE table_schema = '02_gold' AND table_name = 'customer_summary'
  UNION
    SELECT table_owner
    FROM system.information_schema.tables
    WHERE table_schema = '02_gold' AND table_name = 'customer_summary'
  UNION
    SELECT DISTINCT(grantee)
    FROM system.information_schema.schema_privileges
    WHERE schema_name = '02_gold'
    ;

-- Who accessed the table
SELECT
  user_identity.email as `User`,
  IFNULL(request_params.full_name_arg,
    request_params.name)
    AS `Table`,
    action_name AS `Type of Access`,
    event_time AS `Time of Access`
FROM system.access.audit
WHERE (request_params.full_name_arg = 'ws_testing_databricks.02_gold.customer_summary'
  OR (request_params.name = 'customer_summary'
  AND request_params.schema_name = '02_gold'))
  AND action_name
    IN ('createTable','getTable','deleteTable')
  AND event_date > now() - interval '1 day'
ORDER BY event_date DESC
;

-- Whcih table did the user accesses?
SELECT
        action_name as `EVENT`,
        event_time as `WHEN`,
        IFNULL(request_params.full_name_arg, 'Non-specific') AS `TABLE ACCESSED`,
        IFNULL(request_params.commandText,'GET table') AS `QUERY TEXT`
FROM system.access.audit
WHERE user_identity.email = 'xxx@xxx.com'
        AND action_name IN ('createTable',
'commandSubmit','getTable','deleteTable')
or
        -- AND datediff(now(), event_date) < 1
        -- ORDER BY event_date DESC