UPDATE new_schema.article
SET real_number = real_number - $ordered_number
WHERE art_id = $art_id;