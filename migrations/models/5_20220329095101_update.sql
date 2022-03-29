-- upgrade --
ALTER TABLE "user" ADD "company_id" INT;
ALTER TABLE "project" ADD "company_id" INT;
ALTER TABLE "user" ADD CONSTRAINT "fk_user_company_164e84ed" FOREIGN KEY ("company_id") REFERENCES "company" ("id") ON DELETE CASCADE;
ALTER TABLE "project" ADD CONSTRAINT "fk_project_company_c8fb5855" FOREIGN KEY ("company_id") REFERENCES "company" ("id") ON DELETE CASCADE;
-- downgrade --
ALTER TABLE "project" DROP CONSTRAINT "fk_project_company_c8fb5855";
ALTER TABLE "user" DROP CONSTRAINT "fk_user_company_164e84ed";
ALTER TABLE "user" DROP COLUMN "company_id";
ALTER TABLE "project" DROP COLUMN "company_id";
