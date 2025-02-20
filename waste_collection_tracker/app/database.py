from sqlmodel import Session, SQLModel, create_engine
from . import config


engine = create_engine(config.DATABASE_URL, echo=config.DEBUG)
SQLModel.metadata.create_all(engine)

# Dependency: Get the session
def get_session():
    with Session(engine) as session:
        yield session
