from sqlalchemy import create_engine

from Base import Base

engine = create_engine('postgresql://root:example@localhost:5432/pp')
Base.metadata.create_all(engine)