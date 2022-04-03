-- upgrade --
ALTER TABLE "company" ADD "owner_id" INT NOT NULL  DEFAULT 18;
ALTER TABLE "company" ADD CONSTRAINT "fk_company_user_a487a00b" FOREIGN KEY ("owner_id") REFERENCES "user" ("id") ON DELETE CASCADE;
-- downgrade --
ALTER TABLE "company" DROP CONSTRAINT "fk_company_user_a487a00b";
ALTER TABLE "company" DROP COLUMN "owner_id";
