-- Keep a log of any SQL queries you execute as you solve the mystery.

-- checking out the tables

.schema

-- looking at how crime_scene_reports table is laid out

SELECT * FROM crime_scene_reports LIMIT 10;

-- reading crime scene report for theft

SELECT * FROM crime_scene_reports WHERE year = 2021 AND month = 7 AND day = 28
AND street = "Humphrey Street";

-- looking at how interviews table is laid out

SELECT * FROM interviews LIMIT 1;

-- trying to read interview transcripts

SELECT * FROM interviews WHERE transcript = "%bakery%";

-- reading interview transcripts

SELECT * FROM interviews WHERE transcript LIKE "%bakery%";

-- looking at how bakery_security_logs table is laid out

SELECT * FROM bakery_security_logs LIMIT 2;

-- checking the security logs for a car exiting the parking lot between 10:15 & 10:25 AM

SELECT * FROM bakery_security_logs
WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10
AND activity = "exit";

-- looking at how atm_transactions table is laid out

SELECT * FROM atm_transactions LIMIT 5;

-- checking ATM transactions

SELECT * FROM atm_transactions WHERE atm_location = "Leggett Street"
AND year = 2021 AND month = 7 AND day = 28
AND transaction_type = "withdraw";

-- looking at all IDs of people who withdrew money at Legget Street on morning of July 28

SELECT * FROM bank_accounts WHERE account_number IN
(SELECT account_number FROM atm_transactions WHERE atm_location = "Leggett Street"
AND year = 2021 AND month = 7 AND day = 28
AND transaction_type = "withdraw");

-- looking at all names of people who withdrew money at Legget Street on morning of July 28

SELECT name FROM people WHERE id IN
(SELECT person_id FROM bank_accounts WHERE account_number IN
(SELECT account_number FROM atm_transactions WHERE atm_location = "Leggett Street"
AND year = 2021 AND month = 7 AND day = 28 AND transaction_type = "withdraw"));

-- looking at the people's license plates who also withdrew money that morning

SELECT name, license_plate FROM people WHERE name IN
(SELECT name FROM people WHERE id IN
(SELECT person_id FROM bank_accounts WHERE account_number IN
(SELECT account_number FROM atm_transactions WHERE atm_location = "Leggett Street"
AND year = 2021 AND month = 7 AND day = 28 AND transaction_type = "withdraw")));

-- figuring out earliest flight the next day

SELECT * FROM flights WHERE year = 2021 AND month = 7 AND day = 29;

-- checking to make sure flight departs Fiftyville

SELECT * FROM airports WHERE id = 8;

-- checking where thief escaped to

SELECT * FROM airports WHERE id = 4;

-- getting passports, filtered by everyone who left the bakery between 10:15 - 10:25 on July 28th

SELECT name, passport_number FROM people WHERE name = "Iman" OR name = "Luca" OR name = "Diana" OR name = "Bruce";

-- getting passport numbers of everyone who left on the first flight

SELECT passport_number FROM passengers WHERE flight_id = 36;

-- getting name of people who left on the first flight July 29 and also left the bakery between 10:15 - 10:25 on July 28th

SELECT name FROM people WHERE passport_number IN (SELECT passport_number FROM people WHERE name = "Iman" OR name = "Luca" OR name = "Diana" OR name = "Bruce")
AND passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = 36);

-- looking at all calls less than 60s on July 28

SELECT caller, duration FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60;

-- getting names of everyone who made phone calls less than 60s on July 28

SELECT name FROM people WHERE phone_number IN (SELECT caller FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60);

-- checking my work

SELECT name FROM people WHERE
passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = 36)
AND phone_number IN (SELECT caller FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60)
AND license_plate IN (SELECT license_plate FROM people WHERE name IN
(SELECT name FROM people WHERE id IN
(SELECT person_id FROM bank_accounts WHERE account_number IN
(SELECT account_number FROM atm_transactions WHERE atm_location = "Leggett Street"
AND year = 2021 AND month = 7 AND day = 28 AND transaction_type = "withdraw"))))
AND license_plate IN (SELECT license_plate FROM bakery_security_logs
WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute < 26
AND activity = "exit");

-- finding accomplice

SELECT name FROM people WHERE phone_number = (SELECT receiver FROM phone_calls WHERE caller = (SELECT phone_number FROM people WHERE
(passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = 36)
AND phone_number IN (SELECT caller FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60)
AND license_plate IN (SELECT license_plate FROM people WHERE name IN
(SELECT name FROM people WHERE id IN
(SELECT person_id FROM bank_accounts WHERE account_number IN
(SELECT account_number FROM atm_transactions WHERE atm_location = "Leggett Street"
AND year = 2021 AND month = 7 AND day = 28 AND transaction_type = "withdraw"))))
AND license_plate IN (SELECT license_plate FROM bakery_security_logs
WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute < 26
AND activity = "exit")))
AND year = 2021 AND month = 7 AND day = 28 AND duration < 60);