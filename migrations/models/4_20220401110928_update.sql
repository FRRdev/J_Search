-- upgrade --
ALTER TABLE "user" ADD "company_id" INT;
CREATE TABLE IF NOT EXISTS "classification" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(150) NOT NULL,
    "parent_id" INT REFERENCES "classification" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "classification" IS 'Category for company';;
CREATE TABLE IF NOT EXISTS "company" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(150) NOT NULL,
    "create_date" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "classification_id" INT NOT NULL REFERENCES "classification" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "company" IS 'Model of Company';;
CREATE TABLE IF NOT EXISTS "address" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "country" VARCHAR(150) NOT NULL,
    "city" VARCHAR(150) NOT NULL,
    "street" VARCHAR(150),
    "house" VARCHAR(150),
    "company_id" INT NOT NULL REFERENCES "company" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "address" IS 'Category for company';;
CREATE TABLE IF NOT EXISTS "vacancy" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(150) NOT NULL,
    "description" TEXT NOT NULL,
    "salary" INT NOT NULL,
    "create_date" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "company_id" INT NOT NULL REFERENCES "company" ("id") ON DELETE CASCADE
);;
CREATE TABLE IF NOT EXISTS "offer" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "vacancy_id" INT NOT NULL REFERENCES "vacancy" ("id") ON DELETE CASCADE
);;
CREATE TABLE IF NOT EXISTS "skill" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "text" VARCHAR(150) NOT NULL
);;
CREATE TABLE "vacancy_skill" ("vacancy_id" INT NOT NULL REFERENCES "vacancy" ("id") ON DELETE CASCADE,"skill_id" INT NOT NULL REFERENCES "skill" ("id") ON DELETE CASCADE);
ALTER TABLE "project" ADD "company_id" INT;
ALTER TABLE "user" ADD CONSTRAINT "fk_user_company_164e84ed" FOREIGN KEY ("company_id") REFERENCES "company" ("id") ON DELETE CASCADE;
ALTER TABLE "project" ADD CONSTRAINT "fk_project_company_c8fb5855" FOREIGN KEY ("company_id") REFERENCES "company" ("id") ON DELETE CASCADE;
-- downgrade --
ALTER TABLE "project" DROP CONSTRAINT "fk_project_company_c8fb5855";
ALTER TABLE "user" DROP CONSTRAINT "fk_user_company_164e84ed";
ALTER TABLE "user" DROP COLUMN "company_id";
ALTER TABLE "project" DROP COLUMN "company_id";
DROP TABLE IF EXISTS "address";
DROP TABLE IF EXISTS "classification";
DROP TABLE IF EXISTS "company";
DROP TABLE IF EXISTS "offer";
DROP TABLE IF EXISTS "skill";
DROP TABLE IF EXISTS "vacancy";
