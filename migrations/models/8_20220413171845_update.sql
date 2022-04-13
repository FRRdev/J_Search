-- upgrade --
ALTER TABLE "user" DROP CONSTRAINT "fk_user_company_164e84ed";
ALTER TABLE "user" DROP COLUMN "company_id";
-- downgrade --
ALTER TABLE "user" ADD "company_id" INT;
ALTER TABLE "user" ADD CONSTRAINT "fk_user_company_164e84ed" FOREIGN KEY ("company_id") REFERENCES "company" ("id") ON DELETE CASCADE;
