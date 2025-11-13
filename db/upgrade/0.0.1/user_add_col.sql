BEGIN;

CREATE OR REPLACE Function touch_updated_at() returns trigger
language plpgsql
as $func$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$func$;

-- 2) users: add community + audit fields
ALTER TABLE users
  ADD COLUMN IF NOT EXISTS email_verified_at TIMESTAMPTZ,
  ADD COLUMN IF NOT EXISTS username VARCHAR(20),
  ADD COLUMN IF NOT EXISTS avatar_url TEXT,
  ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ NOT NULL DEFAULT now();

WITH seeds AS (
  SELECT
    id,
    LOWER(REGEXP_REPLACE(split_part(email,'@',1), '[^a-z0-9_]', '_', 'g')) AS base,
    LENGTH(id::text) AS idlen
  FROM users
  WHERE (username IS NULL OR username = '')
)
UPDATE users u
SET username = CASE
  WHEN s.base IS NULL OR s.base = '' THEN 'user_' || u.id::text
  WHEN LENGTH(s.base) <= 20 THEN s.base
  ELSE LEFT(s.base, 20 - s.idlen - 1) || '_' || u.id::text
END
FROM seeds s
WHERE u.id = s.id;

-- 3) unique on LOWER(username) (NULLs allowed, duplicates across NULLs are fine)
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_indexes WHERE indexname='users_username_lower_key'
  ) THEN
    CREATE UNIQUE INDEX users_username_lower_key ON users (LOWER(username));
  END IF;
END $$;

-- 4) attach updated_at trigger (safe if re-run)
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_trigger WHERE tgname='trg_users_touch_updated_at'
  ) THEN
    CREATE TRIGGER trg_users_touch_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION touch_updated_at();
  END IF;
END $$;

-- 5) user_tokens: for email verify & password reset
CREATE TABLE IF NOT EXISTS user_tokens (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  token VARCHAR(128) NOT NULL UNIQUE,
  kind VARCHAR(16)  NOT NULL CHECK (kind IN ('verify','reset')),
  expires_at TIMESTAMPTZ NOT NULL,
  consumed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 6) partial index for open tokens
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_indexes WHERE indexname='ix_user_tokens_user_kind_open'
  ) THEN
    CREATE INDEX ix_user_tokens_user_kind_open
      ON user_tokens (user_id, kind)
      WHERE consumed_at IS NULL;
  END IF;
END $$;

COMMIT;
