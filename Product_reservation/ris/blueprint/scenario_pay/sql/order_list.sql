SELECT ord_id, order_date, ordered_number, costs, statuss, art_id, c_id
FROM new_schema.orders
WHERE c_id = $c_id and statuss = 1;
