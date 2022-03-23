-- upgrade --
ALTER TABLE "category" ALTER COLUMN "parent_id" DROP NOT NULL;
ALTER TABLE "toolkit" ALTER COLUMN "parent_id" DROP NOT NULL;
-- downgrade --
ALTER TABLE "toolkit" ALTER COLUMN "parent_id" SET NOT NULL;
ALTER TABLE "category" ALTER COLUMN "parent_id" SET NOT NULL;
