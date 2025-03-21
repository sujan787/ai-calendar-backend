import MySQLdb
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_mysql_db_url():
    return DATABASE_URL

def db_transaction(callback: callable):
    db = SessionLocal()
    try:
        return callback(db)
    except Exception as err:
        db.rollback()  
        raise Exception(str(err))
    finally:
        db.close()
        
def db_query(callback: callable):
    db = SessionLocal()
    try:
        response = callback(db)
        db.commit() 
        return response
    except Exception as err:
        raise Exception(str(err))
    finally:
        pass
        db.close()        