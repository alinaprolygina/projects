INSERT INTO new_schema.orders ( art_id, c_id, order_date, ordered_number, costs, statuss )
VALUES ( $art_id, $client_id, CURRENT_DATE(), $count, $count*$unit_value, 1)