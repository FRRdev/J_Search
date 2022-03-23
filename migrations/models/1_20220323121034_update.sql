-- upgrade --
CREATE TABLE IF NOT EXISTS "category" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(150) NOT NULL,
    "parent_id" INT NOT NULL REFERENCES "category" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "toolkit" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(150) NOT NULL,
    "parent_id" INT NOT NULL REFERENCES "toolkit" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "toolkit" IS 'Category for project';;
CREATE TABLE IF NOT EXISTS "project" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(150) NOT NULL,
    "description" TEXT NOT NULL,
    "create_date" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "category_id" INT NOT NULL REFERENCES "category" ("id") ON DELETE CASCADE,
    "toolkit_id" INT NOT NULL REFERENCES "toolkit" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "project" IS 'Category for project';;
COMMENT ON TABLE "category" IS 'Category for project';;
CREATE TABLE IF NOT EXISTS "task" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "description" TEXT NOT NULL,
    "create_date" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "start_date" TIMESTAMPTZ,
    "end_date" TIMESTAMPTZ,
    "project_id" INT NOT NULL REFERENCES "project" ("id") ON DELETE CASCADE,
    "worker_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "task" IS 'Model task by project';;
CREATE TABLE IF NOT EXISTS "commenttask" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "message" VARCHAR(1000) NOT NULL,
    "create_date" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "task_id" INT NOT NULL REFERENCES "task" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "commenttask" IS 'Model task by task';;
CREATE TABLE "project_user" ("user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,"project_id" INT NOT NULL REFERENCES "project" ("id") ON DELETE CASCADE);
-- downgrade --
DROP TABLE IF EXISTS "project_user";
DROP TABLE IF EXISTS "category";
DROP TABLE IF EXISTS "commenttask";
DROP TABLE IF EXISTS "project";
DROP TABLE IF EXISTS "task";
DROP TABLE IF EXISTS "toolkit";
