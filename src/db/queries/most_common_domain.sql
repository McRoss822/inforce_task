SELECT domain, COUNT(*) as domain_count FROM "user"
GROUP BY domain
ORDER BY domain_count DESC
LIMIT 4;