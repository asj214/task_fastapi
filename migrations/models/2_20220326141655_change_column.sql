-- upgrade --
ALTER TABLE `posts` MODIFY COLUMN `deleted_at` DATETIME(6);
-- downgrade --
ALTER TABLE `posts` MODIFY COLUMN `deleted_at` DATETIME(6) NOT NULL;
