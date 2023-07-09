import abc
from sqlalchemy.orm import Session
from kiki_delivery.infrastructure.shared.database import engine


class AbcDatabaseRepository(abc.ABC):
    _session: Session

    def __init__(self):
        with Session(engine) as session:
            self._session = session
