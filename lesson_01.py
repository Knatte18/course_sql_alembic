from sqlalchemy import create_engine, URL, text
from sqlalchemy.orm import sessionmaker

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


# with session_pool() as session:
#     session.execute(
#         text("""
# CREATE TABLE IF NOT EXISTS users (
#     telegram_id BIGINT PRIMARY KEY,
#     full_name VARCHAR(255) NOT NULL,
#     username VARCHAR(255),
#     language_code VARCHAR(255) NOT NULL,
#     created_at TIMESTAMP DEFAULT NOW(),
#     referrer_id BIGINT,
#     FOREIGN KEY (referrer_id) REFERENCES users (telegram_id) ON DELETE SET NULL
# );

# INSERT INTO users
#     (telegram_id, full_name, username, language_code, created_at)
# VALUES (1, 'John Doe', 'johnny', 'en', '2020-01-01');

# INSERT INTO users
#     (telegram_id, full_name, username, language_code, created_at, referrer_id)
# VALUES (2, 'Jane Doe', 'jane', 'en', '2020-01-01', 1);
#     """)
#     )
#     session.commit()


with session_pool() as session:
    result = session.execute(
        text("""
SELECT * FROM users;
        """)
    )

    # List the names of the fields returned
    field_names = result.keys()
    print('Field names:', field_names)

    rows = result.first()
    print(rows)

    # # Print each row's keys and corresponding values
    # for row in result:
    #     print("Row:")
    #     for key in field_names:
    #         print(f"    {key}: {row[key]}")
