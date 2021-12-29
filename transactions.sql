--------------------------------------------------------------------------------------------------------------------------------
DROP TABLE IF EXISTS "transactions";
CREATE TABLE "transactions"(
	"id" bigserial PRIMARY KEY,
	"numeric" bigint,
	"text" text
);

INSERT INTO "transactions"("numeric", "text") VALUES (111, 'string1'), (222, 'string2'), (333, 'string3');

SELECT * FROM "transactions";
--------------------------------------------------------------------------------------------------------------------------------
-- READ COMMITTED
-- T1
START TRANSACTION;
SET TRANSACTION ISOLATION LEVEL READ COMMITTED READ WRITE;
	
UPDATE "transactions" SET "numeric" = "numeric" + 1;
INSERT INTO "transactions"("numeric", "text") VALUES (444, 'string4');
DELETE FROM "transactions" WHERE "id"=1;

COMMIT;
-- /T1

-- T2
START TRANSACTION;
SET TRANSACTION ISOLATION LEVEL READ COMMITTED READ WRITE;

SELECT * FROM "transactions";

UPDATE "transactions" SET "text" = "text" || '_';
INSERT INTO "transactions"("numeric", "text") VALUES (555, 'string5');
DELETE FROM "transactions" WHERE "id"=3;

COMMIT;
-- /T2
SELECT * FROM "transactions";

--------------------------------------------------------------------------------------------------------------------------------
-- REPEATABLE READ
-- T1
START TRANSACTION;
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ WRITE;
	
UPDATE "transactions" SET "numeric" = "numeric" + 1;
INSERT INTO "transactions"("numeric", "text") VALUES (444, 'string4');
DELETE FROM "transactions" WHERE "id"=1;

COMMIT;
-- /T1

-- T2
START TRANSACTION;
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ WRITE;
SELECT * FROM "transactions";

UPDATE "transactions" SET "numeric" = "numeric" + 1;
INSERT INTO "transactions"("numeric", "text") VALUES (444, 'string4');
DELETE FROM "transactions" WHERE "id"=1;

COMMIT;
-- /T2
SELECT * FROM "transactions";

--------------------------------------------------------------------------------------------------------------------------------
-- SERIALIZABLE
-- T1
START TRANSACTION;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE READ WRITE;
	
UPDATE "transactions" SET "numeric" = "numeric" + 1;
INSERT INTO "transactions"("numeric", "text") VALUES (444, 'string4');
DELETE FROM "transactions" WHERE "id"=1;

COMMIT;
-- /T1

-- T2
START TRANSACTION;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE READ WRITE;

SELECT * FROM "transactions";

UPDATE "transactions" SET "text" = "text" || '_';
INSERT INTO "transactions"("numeric", "text") VALUES (555, 'string5');
DELETE FROM "transactions" WHERE "id"=3;

COMMIT;
-- /T2
SELECT * FROM "transactions";