from sqlalchemy import Table, Column, Integer, String, MetaData

meta1 = MetaData()


user_t1 = Table(
    "user", meta1,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False, unique=False),
    Column("email", String, nullable=True, unique=True),
    Column("data", String))

post_t = Table(
    "post", meta1,
    Column("id", Integer, primary_key=True, autoincrement=True))

question_t = Table(
    "question", meta1,
    Column("id", Integer, primary_key=True, autoincrement=True))


meta2 = MetaData()

user_t2 = Table(
    "user", meta2,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=True, unique=True, default="123"),
    Column("email", String, nullable=False, unique=False),
    Column("password", String(32), nullable=True, default="123"))

post_t = Table(
    "post", meta2,
    Column("id", Integer, primary_key=True, autoincrement=True))

answer_t = Table(
    "answer", meta2,
    Column("id", Integer, primary_key=True, autoincrement=True))
