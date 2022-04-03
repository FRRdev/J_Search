-- upgrade --
ALTER TABLE "company" ALTER COLUMN "owner_id" DROP DEFAULT;
-- downgrade --
ALTER TABLE "company" ALTER COLUMN "owner_id" SET DEFAULT 18;
