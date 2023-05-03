from dotenv import load_dotenv
load_dotenv(verbose=True)
from relational.schema import engine
from relational.tables.base import Base

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)