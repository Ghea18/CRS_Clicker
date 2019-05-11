import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Set up database
try:
    # Check for environment variable
    if not os.getenv("DATABASE_URL"):
        raise RuntimeError("DATABASE_URL is not set") 
        #engine = create_engine("postgres://nrpdpcdgweixjb:01a255acd77e3eaa7c808e768f94fceb5c2a0044d3cb5ac5197896fc07658cec@ec2-23-21-130-182.compute-1.amazonaws.com:5432/d35hm8i3hrbss4")
    else:
        engine = create_engine(os.getenv("DATABASE_URL"))
    # Create Database Access Session
    db_session = scoped_session(sessionmaker(bind=engine))
except:
    # Create Database Access Session from Local Database
    engine = create_engine('sqlite:///database.db', convert_unicode=True) # Local sqlite
    db_session = scoped_session(sessionmaker(autocommit=False, 
                                            autoflush=False, 
                                            bind=engine))
Base = declarative_base() 
Base.query = db_session.query_property() 

def init_db():
    import models
    try:
        msg += "Creating Database: "
        Base.metadata.create_all(bind=engine)
        msg += "OK!\n"
    except Exception as e:
        msg += "FAIL!\n"+e
    finally:
        msg += f"Init database done!"
    print(msg)