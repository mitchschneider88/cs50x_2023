SELECT AVG(rating) as avg_2012_rating
FROM ratings
WHERE movie_id
IN (SELECT id FROM movies WHERE year = 2012);