SELECT t.trip_id, ROUND((total_seats - seats_left) * 1.0 / total_seats, 1) * 100 as seats_occupiced_percentage, datetime(departure_date, 'unixepoch')
FROM trips t
INNER JOIN (
	SELECT trip_id, max(modify_date) as latest
		FROM trips
	GROUP BY trip_id
	HAVING departure_date < strftime('%s', 'now')
		AND search_city_from = Berlin AND search_city_to = Leipzig
) t2
ON t.modify_date = t2.latest AND t.trip_id = t2.trip_id
ORDER BY departure_date DESC
