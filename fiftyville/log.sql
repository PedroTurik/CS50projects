-- Keep a log of any SQL queries you execute as you solve the mystery.

-- all crime reports
SELECT * FROM crime_scene_reports;

-- all crime reports at humphrey street
SELECT * FROM crime_scene_reports WHERE street = "Humphrey Street";
-- theft took place at 10:15am at Bakery and 3 witness

-- check bakery at the time the crime took place
SELECT * FROM bakery_security_logs WHERE day = 28 AND month = 7 AND hour = 10;

-- check interviews
SELECT * FROM interviews WHERE day = 28 AND month = 7;
-- he got the earliest flight of 29 of July and the helper purchased the tickets.
-- thief left the bakery wothin 10 minutes after the theft.
-- Thief was at ATM at Leggett Street withdrawing money during morning

-- Thief's possible license plates.
SELECT license_plate FROM bakery_security_logs
WHERE hour = 10
AND minute > 15
AND minute < 25
AND day = 28
AND month = 7;

-- check people with possible licence plates
SELECT *
   FROM people
   WHERE license_plate IN
   (SELECT license_plate FROM bakery_security_logs
   WHERE hour = 10
   AND minute > 15
   AND minute < 25
   AND day = 28
   AND month = 7);

-- check phone calls in timeframe from possible callers based on license plate
SELECT * FROM phone_calls
WHERE caller IN
(SELECT phone_number
   FROM people
   WHERE license_plate IN
   (SELECT license_plate FROM bakery_security_logs
   WHERE hour = 10
   AND minute > 15
   AND minute < 25
   AND day = 28
   AND month = 7))
   AND day = 28
   AND duration < 60;


-- possible helpers based on phone calls
SELECT * FROM people WHERE phone_number IN
(SELECT receiver FROM phone_calls
WHERE caller IN
(SELECT phone_number
   FROM people
   WHERE license_plate IN
   (SELECT license_plate FROM bakery_security_logs
   WHERE hour = 10
   AND minute > 15
   AND minute < 25
   AND day = 28
   AND month = 7))
   AND day = 28
   AND duration < 60);

-- Withdrawls from ATM at that day
SELECT * FROM atm_transactions
WHERE day = 28
AND month = 7
AND atm_location = "Leggett Street"
AND transaction_type = "withdraw";

-- Bank accounts with possible ID from license plate and possible account number from atm
SELECT * FROM bank_accounts WHERE person_id IN
(SELECT id
   FROM people
   WHERE license_plate IN
   (SELECT license_plate FROM bakery_security_logs
   WHERE hour = 10
   AND minute > 15
   AND minute < 25
   AND day = 28
   AND month = 7))
AND account_number IN
(SELECT account_number FROM atm_transactions
WHERE day = 28
AND month = 7
AND atm_location = "Leggett Street"
AND transaction_type = "withdraw");

-- Finding possible Airports
SELECT * FROM airports WHERE city = "Fiftyville";

-- finding flight
SELECT * FROM flights WHERE day = 29 AND month = 7 AND origin_airport_id = 8 ORDER BY hour;

--finding passenger
SELECT * FROM passengers WHERE flight_id = 36;

-- finding culprit
SELECT * FROM people WHERE
passport_number IN
(SELECT passport_number FROM passengers WHERE flight_id = 36)
AND license_plate IN
(SELECT license_plate FROM bakery_security_logs
WHERE hour = 10
AND minute > 15
AND minute < 25
AND day = 28
AND month = 7)
AND phone_number IN
(SELECT caller FROM phone_calls
WHERE caller IN
(SELECT phone_number
   FROM people
   WHERE license_plate IN
   (SELECT license_plate FROM bakery_security_logs
   WHERE hour = 10
   AND minute > 15
   AND minute < 25
   AND day = 28
   AND month = 7))
   AND day = 28
   AND duration < 60)
AND id IN
(SELECT person_id FROM bank_accounts WHERE person_id IN
(SELECT id
   FROM people
   WHERE license_plate IN
   (SELECT license_plate FROM bakery_security_logs
   WHERE hour = 10
   AND minute > 15
   AND minute < 25
   AND day = 28
   AND month = 7))
AND account_number IN
(SELECT account_number FROM atm_transactions
WHERE day = 28
AND month = 7
AND atm_location = "Leggett Street"
AND transaction_type = "withdraw"));

+--------+-------+----------------+-----------------+---------------+
|   id   | name  |  phone_number  | passport_number | license_plate |
+--------+-------+----------------+-----------------+---------------+
| 686048 | Bruce | (367) 555-5533 | 5773159633      | 94KL13X       |
+--------+-------+----------------+-----------------+---------------+

-- finding helper
SELECT * FROM people WHERE phone_number = "(375) 555-8161";

+--------+-------+----------------+-----------------+---------------+
|   id   | name  |  phone_number  | passport_number | license_plate |
+--------+-------+----------------+-----------------+---------------+
| 864400 | Robin | (375) 555-8161 |                 | 4V16VO0       |
+--------+-------+----------------+-----------------+---------------+

-- finding destination
SELECT * FROM airports WHERE id = 4;

+----+--------------+-------------------+---------------+
| id | abbreviation |     full_name     |     city      |
+----+--------------+-------------------+---------------+
| 4  | LGA          | LaGuardia Airport | New York City |
+----+--------------+-------------------+---------------+