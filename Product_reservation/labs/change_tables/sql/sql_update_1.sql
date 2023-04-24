UPDATE language_courses.course_order
SET customer = '$gener2',
    order_date = '$gener3',
    general_cost = $gener4
WHERE order_id = $gener1;