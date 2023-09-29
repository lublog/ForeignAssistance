# @Time    : 2023/09/29 09:55
# @Author  : lu yao
# @FileName: database.py

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID
import uuid

engine = create_engine('postgresql://postgres:123456@localhost/postgres')

Base = declarative_base()


class Complete(Base):
    __tablename__ = 'us_foreign_aid_complete'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    country_code = Column("Country Code", String)
    country_name = Column("Country Name", String)
    assistance_type = Column("Foreign Assistance Objective Name", String)
    year = Column("Fiscal Year", Integer)
    amount = Column("Current Dollar Amount", Integer)


session = Session(bind=engine)

# 查询
complete = session.query(Complete).filter_by(country_code='AFG').all()

for i in complete:
    print(i.country_code, i.country_name, i.assistance_type, i.year, i.amount)



