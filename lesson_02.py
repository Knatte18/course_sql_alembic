from tkinter import TRUE
from typing import Optional
from typing_extensions import Annotated
from sqlalchemy import (
    BIGINT,
    DECIMAL,
    URL,
    VARCHAR,
    ForeignKey,
    Integer,
    create_engine,
    func,
)
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import sessionmaker


from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# Format: driver+postgresql://user:pass@host:port/dbname
url = URL.create(
    drivername='postgresql+psycopg2',
    username='testuser',
    password='testpassword',
    host='localhost',
    port=5432,
    database='testuser',
)

engine = create_engine(url, echo=True)
session_pool = sessionmaker(engine)


class Base(DeclarativeBase):
    pass


# Drop all tables
# Base.metadata.drop_all(engine)

"""
TEMPLATE OF THE users SQL TABLE FORMAT

***TEMPLATE FOR users***
CREATE TABLE IF NOT EXISTS users (
    telegram_id    BIGINT       PRIMARY KEY,
    full_name      VARCHAR(255) NOT NULL,
    username       VARCHAR(255),
    language_code  VARCHAR(255) NOT NULL,
    created_at     TIMESTAMP    DEFAULT NOW(),
    referrer_id    BIGINT,
    FOREIGN KEY (referrer_id) REFERENCES users (telegram_id) ON DELETE SET NULL
);


***TEMPLATE FOR products***
CREATE TABLE products
(
    product_id  SERIAL PRIMARY KEY,
    title       VARCHAR(255) NOT NULL,
    description TEXT,
    created_at  TIMESTAMP DEFAULT NOW()
);


***TEMPLATE FOR orders***
CREATE TABLE orders
(
    order_id    SERIAL PRIMARY KEY,
    user_id     BIGINT NOT NULL,
    created_at  TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (user_id)
        REFERENCES users (telegram_id)
        ON DELETE CASCADE
);


***TEMPLATE FOR order_products***
CREATE TABLE order_products
(
    order_id    INTEGER NOT NULL,
    product_id  INTEGER NOT NULL,
    quantity    INTEGER NOT NULL,
    FOREIGN KEY (order_id)
        REFERENCES orders (order_id)
        ON DELETE CASCADE,
    FOREIGN KEY (product_id)
        REFERENCES products (product_id)
        ON DELETE RESTRICT
);
"""


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now()
    )


class TableNameMixin:
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'


# class User(Base, TimestampMixin, TableNameMixin):
#     telegram_id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
#     full_name: Mapped[str] = mapped_column(VARCHAR(255))
#     username: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
#     language_code: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)

#     referred_id: Mapped[int] = mapped_column(
#         BIGINT, ForeignKey('users.telegram_id', ondelete='SET NULL'), nullable=True
#     )


int_pk = Annotated[int, mapped_column(Integer, primary_key=TRUE)]  # Integer primary key

user_fk = Annotated[
    int,
    mapped_column(BIGINT, ForeignKey('users.telegram_id', ondelete='SET NULL')),
]  # User Foreign Key

str_255 = Annotated[str, mapped_column(VARCHAR(255))]


class User(Base, TimestampMixin, TableNameMixin):
    telegram_id: Mapped[int] = mapped_column(
        BIGINT, primary_key=True, autoincrement=False
    )

    full_name: Mapped[str_255]
    user_name: Mapped[Optional[str_255]]
    language_code: Mapped[str] = mapped_column(VARCHAR(10))

    referred_id: Mapped[Optional[user_fk]]


class Product(Base, TimestampMixin, TableNameMixin):
    product_id: Mapped[int_pk]
    title: Mapped[str_255]
    description: Mapped[Optional[str]] = mapped_column(VARCHAR(3000))
    price: Mapped[float] = mapped_column(DECIMAL(precision=15, scale=4))


class Order(Base, TimestampMixin, TableNameMixin):
    order_id: Mapped[int_pk]
    user_id: Mapped[user_fk]


class OrderProduct(Base, TableNameMixin):
    order_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('orders.order_id', ondelete='CASCADE'), primary_key=True
    )
    product_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('products.product_id', ondelete='RESTRICT'),
        primary_key=True,
    )
    quantity: Mapped[int]
