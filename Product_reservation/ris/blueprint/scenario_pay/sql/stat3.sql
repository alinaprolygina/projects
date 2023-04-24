UPDATE new_schema.orders
SET statuss = 3
WHERE (CURDATE()-order_date) > 3 and statuss = 1;