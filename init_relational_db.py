from relational.schema import Engine
from relational.tables.base import Base

if __name__ == "__main__":
    Base.metadata.create_all(bind=Engine)