from contextlib import contextmanager

from app.extensions import db


class DatabaseService:
    """Manages database transactions."""

    def commit(self) -> None:
        try:
            db.session.commit()
        except Exception as err:
            self.rollback()
            raise err

    def rollback(self) -> None:
        db.session.rollback()

    @contextmanager
    def transaction(self):
        try:
            yield
            self.commit()
        except Exception as err:
            self.rollback()
            raise err