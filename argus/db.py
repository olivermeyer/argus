import os

from sqlalchemy import create_engine


db_location = os.environ.get("DB_LOCATION") or os.path.join(os.path.dirname(__file__), "..", "data", "argus.db")


engine = create_engine(f"sqlite:///{db_location}")
