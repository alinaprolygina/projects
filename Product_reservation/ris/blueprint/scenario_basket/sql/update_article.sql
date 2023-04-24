UPDATE new_schema.article
SET res_number = res_number + $count,
    res_date = CURRENT_DATE()
WHERE art_id = $art_id;