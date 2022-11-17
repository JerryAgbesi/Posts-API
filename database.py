from databases import Database
import sqlalchemy


DATABASE_URL = "sqlite:///./posts.db"

metadata = sqlalchemy.MetaData()

database = Database(DATABASE_URL)


posts = sqlalchemy.Table(
    "Post",
    metadata,
    sqlalchemy.Column("id",sqlalchemy.Integer,primary_key=True),
    sqlalchemy.Column("author",sqlalchemy.String(100),nullable = False),
    sqlalchemy.Column("content_tags",sqlalchemy.String(100)),
    sqlalchemy.Column("content",sqlalchemy.String(1200),nullable = False),
    sqlalchemy.Column("date_created",sqlalchemy.DateTime),
    sqlalchemy.Column("date_updated",sqlalchemy.DateTime,nullable = True)
)

engine = sqlalchemy.create_engine(DATABASE_URL)

def get_database() -> Database:
    return database
