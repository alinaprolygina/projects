UPDATE new_schema.customer
SET summ = summ + $costs
WHERE c_id = $c_id;