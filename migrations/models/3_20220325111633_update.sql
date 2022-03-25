-- upgrade --
ALTER TABLE "task" ALTER COLUMN "worker_id" DROP NOT NULL;
-- downgrade --
ALTER TABLE "task" ALTER COLUMN "worker_id" SET NOT NULL;
