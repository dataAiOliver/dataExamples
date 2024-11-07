ALTER TABLE 02_gold.customer_summary DROP ROW FILTER;

CREATE OR REPLACE TABLE default.user_group_country_mapping (
    user_group STRING,
    allowed_country STRING
);

INSERT INTO default.user_group_country_mapping VALUES
('USERS_USA', 'USAa'),
('USERS_CANADA', 'CANADA'),
('USERS_EU', 'GERMANY'),
('USERS_EU', 'FRANCE');

CREATE OR REPLACE FUNCTION 02_gold.dynamic_country_filter(Country STRING)
RETURN EXISTS (
    SELECT 1
    FROM ws_testing_databricks.default.user_group_country_mapping
    WHERE IS_ACCOUNT_GROUP_MEMBER(user_group) AND allowed_country = Country
);

ALTER TABLE 02_gold.customer_summary SET ROW FILTER 02_gold.dynamic_country_filter ON (Country);




