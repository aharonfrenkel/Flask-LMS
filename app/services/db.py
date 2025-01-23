from app import db


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