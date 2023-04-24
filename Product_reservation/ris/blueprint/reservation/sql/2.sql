Select titles from new_schema.article
where unit_value = ( Select MAX(unit_value) from new_schema.article where materials = '$material') and materials = '$material';