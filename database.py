from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#engine = create_engine("postgresql://postgres:Lijopleurodon12#4@localhost/database", echo=True)
engine = create_engine("postgresql://wppnfwageosvfn:10f68c34e79be33239046277597ae2fe9ad9abbb3512617cfe3fdd457ddc94a1@ec2-52-72-99-110.compute-1.amazonaws.com:5432/d8md2fjpejrtsr")

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)