SELECT * from 02_gold.customer_summary;

ALTER TABLE 02_gold.customer_summary DROP ROW FILTER;

CREATE OR REPLACE FUNCTION 02_gold.filter_simple_usa(Country STRING)
RETURN Country = 'USA' AND IS_ACCOUNT_GROUP_MEMBER('USERS_USA');


ALTER TABLE 02_gold.customer_summary SET ROW FILTER ws_testing_databricks.02_gold.filter_simple_usa ON (Country);