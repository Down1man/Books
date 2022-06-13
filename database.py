from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#engine = create_engine("postgresql://postgres:Lijopleurodon12#4@localhost/database", echo=True)
engine = create_engine("postgresql://erjdqsphgnfdfv:34efc68fe9d48c3925e73abc1e90851e7b7bae6a1073f2a6c5adb71ab928c929@ec2-52-72-99-110.compute-1.amazonaws.com:5432/d394s9u0corcpe")

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)