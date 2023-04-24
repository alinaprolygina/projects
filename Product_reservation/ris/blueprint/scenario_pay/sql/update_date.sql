UPDATE new_schema.article
SET fix_date = CURDATE()
WHERE art_id = $art_id;