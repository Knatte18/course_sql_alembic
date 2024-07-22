from sqlalchemy import BIGINT, VARCHAR, ForeignKey, func
from sqlalchemy.dialects.postgresql import TIMESTAMP

from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


"""
TEMPLATE OF THE users SQL TABLE FORMAT
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


class User(Base):
    __tablename__ = 'users'
    telegram_id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    full_name: Mapped[str] = mapped_column(VARCHAR(255))
    username: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    language_code: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=func.now()
    )
    referred_id: Mapped[int] = mapped_column(
        BIGINT, ForeignKey('users.telegram_id', ondelete='SET NULL'), nullable=True
    )
