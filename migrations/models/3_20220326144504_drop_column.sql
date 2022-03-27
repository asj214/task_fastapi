-- upgrade --
ALTER TABLE `posts` DROP COLUMN `deleted_at`;
-- downgrade --
ALTER TABLE `posts` ADD `deleted_at` DATETIME(6);
