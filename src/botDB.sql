PRAGMA foreign_keys = OFF;
CREATE TABLE "server_info" (
"initialized"  TEXT
);
CREATE TABLE "users" (
"id" INTEGER NOT NULL,
"address" TEXT,
PRIMARY KEY ("id" ASC)
);
