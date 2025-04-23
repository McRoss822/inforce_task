 DROP TABLE IF EXISTS "user";

 CREATE TABLE "user" (
 user_id INT PRIMARY KEY,
 name VARCHAR(100),
 email VARCHAR(255),
 signup_date DATE,
 domain VARCHAR(100)
);

SELECT * FROM "user";