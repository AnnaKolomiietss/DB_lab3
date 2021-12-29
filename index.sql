\timing off
DROP TABLE IF EXISTS "gin_test";
CREATE TABLE "gin_test"("id" bigserial PRIMARY KEY, "string" text, "gin_vector" tsvector);
INSERT INTO "gin_test"("string") SELECT substr(characters, (random() * length(characters) + 1)::integer, 10) FROM (VALUES('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM')) as symbols(characters), generate_series(1, 1000000) as q;
UPDATE "gin_test" set "gin_vector" = to_tsvector("string");

\timing on
DROP INDEX IF EXISTS "gin_index";
SELECT COUNT(*) FROM "gin_test" WHERE "id" % 2 = 0;
SELECT COUNT(*) FROM "gin_test" WHERE ("gin_vector" @@ to_tsquery('bnm'));
SELECT SUM("id") FROM "gin_test" WHERE ("gin_vector" @@ to_tsquery('QWERTYUIOP')) OR ("gin_vector" @@ to_tsquery('bnm'));
SELECT MIN("id"), MAX("id") FROM "gin_test" WHERE ("gin_vector" @@ to_tsquery('bnm')) GROUP BY "id" % 2;

CREATE INDEX "gin_index" ON "gin_test" USING gin("gin_vector");
SELECT COUNT(*) FROM "gin_test" WHERE "id" % 2 = 0;
SELECT COUNT(*) FROM "gin_test" WHERE ("gin_vector" @@ to_tsquery('bnm'));
SELECT SUM("id") FROM "gin_test" WHERE ("gin_vector" @@ to_tsquery('QWERTYUIOP')) OR ("gin_vector" @@ to_tsquery('bnm'));
SELECT MIN("id"), MAX("id") FROM "gin_test" WHERE ("gin_vector" @@ to_tsquery('bnm')) GROUP BY "id" % 2;

--------------------------------------------------------------------------------------------------------------------------------
\timing off
DROP TABLE IF EXISTS "hash_test";
CREATE TABLE "hash_test"("id" bigserial PRIMARY KEY, "time" timestamp);
INSERT INTO "hash_test"("time") SELECT (timestamp '2021-01-01' + random() * (timestamp '2020-01-01' - timestamp '2022-01-01')) FROM (VALUES('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM')) as symbols(characters), generate_series(1, 1000000) as q;

\timing on
DROP INDEX IF EXISTS "time_hash_index";
SELECT COUNT(*) FROM "hash_test" WHERE "id" % 2 = 0;
SELECT COUNT(*) FROM "hash_test" WHERE "time" >= '20191001';
SELECT AVG("id") FROM "hash_test" WHERE "time" >= '20191001' AND "time" <= '20211207';
SELECT SUM("id"), MAX("id") FROM "hash_test" WHERE "time" >= '20200505' AND "time" <= '20210505' GROUP BY "id" % 2;

CREATE INDEX "time_hash_index" ON "hash_test" USING hash("id");
SELECT COUNT(*) FROM "hash_test" WHERE "id" % 2 = 0;
SELECT COUNT(*) FROM "hash_test" WHERE "time" >= '20191001';
SELECT AVG("id") FROM "hash_test" WHERE "time" >= '20191001' AND "time" <= '20211207';
SELECT SUM("id"), MAX("id") FROM "hash_test" WHERE "time" >= '20200505' AND "time" <= '20210505' GROUP BY "id" % 2;