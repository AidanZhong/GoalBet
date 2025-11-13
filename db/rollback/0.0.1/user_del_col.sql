BEGIN;

-- 1) Drop the partial index and tokens table
DROP INDEX IF EXISTS ix_user_tokens_user_kind_open;
DROP TABLE IF EXISTS user_tokens;

-- 2) Remove the username unique index
DROP INDEX IF EXISTS users_username_lower_key;

-- 3) Detach the updated_at trigger from users (keep the function by default)
DROP TRIGGER IF EXISTS trg_users_touch_updated_at ON users;

-- 4) Drop columns added to users
ALTER TABLE users
  DROP COLUMN IF EXISTS avatar_url,
  DROP COLUMN IF EXISTS username,
  DROP COLUMN IF EXISTS email_verified_at,
  DROP COLUMN IF EXISTS updated_at,
  DROP COLUMN IF EXISTS created_at;

-- Optional: if you really want to remove the helper function (only if unused elsewhere)
-- DROP FUNCTION IF EXISTS touch_updated_at();

COMMIT;
