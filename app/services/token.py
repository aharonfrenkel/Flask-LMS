from datetime import datetime
from typing import Optional

import pytz
from werkzeug.exceptions import Unauthorized

from app.constants import ModelConstants, ValidationConstants
from app.models import User, Token
from app.schemas import TokenSchema
from app.services import CRUDService
from app.utils import generate_token, hash_password, verify_password


class TokenService:
    """
    Service for managing password reset tokens.

    Handles creation and management of password reset tokens, including:
    - Creating new tokens
    - Managing token lifecycle (active/used/invalidated)
    - Ensuring only one active token exists per user
    """

    def __init__(
            self,
            crud_service: CRUDService,
            token_schema: TokenSchema
    ):
        self._crud_service = crud_service
        self._token_schema = token_schema

    def create_password_reset_token(self, user: User) -> str:
        """
        Creates a new password reset token for a user.
        If an active token exists, it will be invalidated before creating a new one.

        Args:
            user: The user requesting password reset

        Returns:
            str: The raw token to be sent to the user
        """

        self._invalidate_existing_token(user)
        raw_token = generate_token()
        token_data = self._prepare_token_data(user, raw_token)
        self._crud_service.create(token_data, self._token_schema)
        return raw_token

    def _invalidate_existing_token(self, user: User) -> None:
        existing_token = self._find_active_token(user)
        if existing_token:
            self._update_token_status(existing_token, ModelConstants.TokenStatus.INVALIDATED)

    def _prepare_token_data(self, user: User, token: str) -> dict:
        return {
            'user_id': user.id,
            'token': hash_password(token)
        }

    def mark_token_as_used(self, user: User, raw_token: str) -> None:
        """
        Marks a password reset token as used after validating it.

        Args:
            user: The user who owns the token
            raw_token: The token to be marked as used
        Raises:
            Unauthorized: If token validation fails (invalid, expired, or already used)
        """
        active_token = self._find_active_token(user)
        if not active_token or not verify_password(active_token.token, raw_token):
            raise Unauthorized(ValidationConstants.ResetPassword.ERROR_MESSAGES['general_error'])
        self._update_token_status(active_token, ModelConstants.TokenStatus.USED)

    def _find_active_token(self, user: User) -> Optional[Token]:
        return self._crud_service.find_one_by_advanced_filters(
            Token,
            Token.user_id == user.id,
            Token.status == ModelConstants.TokenStatus.ACTIVE,
            Token.expiration > datetime.now(pytz.utc)
        )

    def _update_token_status(self, token: Token, status: str) -> None:
        self._crud_service.update(token, status=status)