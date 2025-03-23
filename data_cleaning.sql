CREATE VIEW transaction_details_cleaned AS
SELECT 
    user_id,
    transaction_id,
    item_code,
    item_description,
    CAST(number_of_items_purchased AS NUMERIC) AS number_of_items_purchased,
    CAST(cost_per_item AS NUMERIC) AS cost_per_item,
    country,
  to_char(
    to_timestamp(
      trim(replace(substring(transaction_time, 5), 'IST', '')),
      'Mon DD HH24:MI:SS YYYY'
    ),
    'YYYY-MM-DD HH24:MI:SS'
  ) AS transaction_timestamp,
    _dlt_load_id,
    _dlt_id
FROM "zoomcamp"."transaction_details_data"."transaction_details";