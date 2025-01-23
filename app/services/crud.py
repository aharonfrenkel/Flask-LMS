from typing import Type, TypeVar, Optional

from marshmallow import Schema
from werkzeug.exceptions import NotFound, Conflict

from app import db
from app.factories import db_service

T = TypeVar('T')


class CRUDService:
    """
    Base service for CRUD operations.
    Provides generic functionality for reading, creating, updating and deleting records.
    """

    # Read operations
    def find_one_by_fields(self, model: Type[T], **filters) -> Optional[T]:
        return model.query.filter_by(**filters).first()

    def find_many_by_fields(self, model: Type[T], **filters) -> list[T]:
        return model.query.filter_by(**filters).all()

    def find_one_by_fields_or_raise(
            self,
            model: Type[T],
            exception: Type[Exception] = NotFound,
            error_msg: str = "Record not found",
            **filters
    ) -> T:
        item = self.find_one_by_fields(model, **filters)
        if not item:
            raise exception(error_msg)
        return item

    def validate_no_record_by_fields(
            self,
            model: Type[T],
            exception: Type[Exception] = Conflict,
            error_msg: str = "Record already exists",
            **filters
    ) -> None:
        item = self.find_one_by_fields(model, **filters)
        if item:
            raise exception(error_msg)

    # Create operations
    def create(self, data: dict, schema: Schema) -> T:
        new_item = schema.load(data)
        db.session.add(new_item)
        db_service.commit()
        return new_item