Select c_id, customer_name, city, telephone, contract_date, summ from new_schema.customer left join ( Select ord_id, c_id from new_schema.orders
where month(order_date)=$month and year(order_date)=$year) ORD13 using(c_id)
where ord_id IS NULL;