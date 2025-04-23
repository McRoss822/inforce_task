from ..db_init import Base, session
from sqlalchemy import Column, Integer, String, Date
import pandas as pd

class User(Base):
    """
    SQLAlchemy model representing the 'user' table.
    """
    __tablename__ = 'user'
    
    user_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(255))
    signup_date = Column(Date)
    domain = Column(String(100))


def insert_data_from_csv(data_file: str):
    """
    Reads a CSV file and inserts user records into the database
    only if the user_id does not already exist.
    """
    df = pd.read_csv(data_file)

    existing_ids = {user.user_id for user in session.query(User.user_id).all()}

    new_users = []

    for _, row in df.iterrows():
        if row['user_id'] not in existing_ids:
            new_users.append(
                User(
                    user_id=row['user_id'],
                    name=row['name'],
                    email=row['email'],
                    signup_date=row['signup_date'],
                    domain=row['domain']
                )
            )

    if new_users:
        session.add_all(new_users)
        session.commit()
    session.close()
