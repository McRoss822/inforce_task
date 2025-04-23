SELECT * FROM "user"
WHERE email LIKE '%gmail.com'
UNION
SELECT * FROM "user"
WHERE email LIKE '%yahoo.com'
UNION
SELECT * FROM "user"
WHERE email LIKE '%hotmail.com'
ORDER BY signup_date DESC;