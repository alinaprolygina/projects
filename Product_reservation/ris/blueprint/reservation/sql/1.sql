Select art_id, titles, customer_name
from new_schema.orders join new_schema.customer using(c_id) join new_schema.article using(art_id)
where customer_name = '$name' and year(order_date)=$year and month(order_date)=$month;