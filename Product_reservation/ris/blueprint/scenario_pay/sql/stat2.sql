UPDATE new_schema.orders
SET statuss = 2
WHERE ord_id = $ord_id;
