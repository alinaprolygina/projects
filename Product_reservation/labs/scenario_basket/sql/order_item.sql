SELECT service_id, service_name, foreighn_language, service_cost
FROM language_courses.services
WHERE 1
    AND service_id = '$id'