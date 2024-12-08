CREATE TABLE user_metrics (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    username TEXT,
    event TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

ALTER TABLE user_metrics ADD CONSTRAINT unique_user_event UNIQUE (user_id, event);
