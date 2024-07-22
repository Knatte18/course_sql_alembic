from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


"""
CREATE TABLE IF NOT EXISTS users (
    telegram_id    BIGINT       PRIMARY KEY,
    full_name      VARCHAR(255) NOT NULL,
    username       VARCHAR(255),
    language_code  VARCHAR(255) NOT NULL,
    created_at     TIMESTAMP    DEFAULT NOW(),
    referrer_id    BIGINT,
    FOREIGN KEY (referrer_id) REFERENCES users (telegram_id) ON DELETE SET NULL
);

"""
