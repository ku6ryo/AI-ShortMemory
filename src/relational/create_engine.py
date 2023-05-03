import os
from sqlalchemy import create_engine as ce

def create_engine():
    return ce(
        os.environ.get("DATABASE"),
        echo=False
    )