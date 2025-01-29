from typing import Optional, List

from flask_mail import Message

from app import mail
from app.constants import GeneralConstants
from config import Config


class EmailService:
    """Service for handling all email communications."""

    def send_email(
            self,
            subject: str,
            body: str,
            to: str,
            cc: Optional[List[str]] = None,
            bcc: Optional[List[str]] = None,
            sender: Optional[str] = None,
            reply_to: Optional[str] = None
    ) -> None:
        """
        Send an email using Flask-Mail.

        Args:
            subject: Email subject line
            body: Email content
            to: Primary recipient email address
            cc: List of carbon copy recipient addresses
            bcc: List of blind carbon copy recipient addresses
            sender: Override default sender address
            reply_to: Reply-to email address
        """

        msg = Message(
            subject=subject,
            recipients=[to],
            body=body,
            sender=sender or Config.MAIL_DEFAULT_SENDER,
            cc=cc,
            bcc=bcc,
            reply_to=reply_to
        )
        mail.send(msg)

    def send_password_reset_token(self, email: str, token: str) -> None:
        """
        Send password reset email with token.

        Args:
            email: Recipient's email address
            token: Password reset token
        """

        subject = "Password Reset Request"

        body = f"""
        We received a request to reset your password.

        Your password reset code is:    "{token}"

        To reset your password, send a POST request, to /auth/password/reset, with the following JSON structure:
        {{
            "email": "{email}",
            "token": "{token}",
            "new_password": "Your new password"
        }}
        
        This code will expire in {GeneralConstants.Time.DEFAULT_TOKEN_EXPIRATION_HOURS} hour.

        If you did not request this password reset, please ignore this email, and ensure your account is secure.
        """

        self.send_email(
            subject=subject,
            body=body,
            to=email
        )

    def send_password_reset_confirmation(self, email: str) -> None:
        """
        Send password reset confirmation email.

        Args:
            email: Recipient's email address
        """
        subject = "Password Reset Confirmation"

        body = f"""
        Your password has been successfully reset.

        If you did not request this password reset, please contact the support manager as soon as possible.
        """

        self.send_email(
            subject=subject,
            body=body,
            to=email
        )