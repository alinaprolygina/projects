SELECT art_id, titles, materials, units, unit_value, res_number, res_date
FROM new_schema.article
WHERE 1
    AND art_id = '$id'