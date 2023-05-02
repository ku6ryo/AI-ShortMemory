import os
from sqlalchemy import create_engine as ce

def create_engine():

    print(os.environ.get("DATABASE"))
    return ce(
        os.environ.get("DATABASE"),
        echo=True
    )