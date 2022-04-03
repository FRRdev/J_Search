-- upgrade --
ALTER TABLE "user" ADD "is_company" BOOL NOT NULL  DEFAULT False;
-- downgrade --
ALTER TABLE "user" DROP COLUMN "is_company";
