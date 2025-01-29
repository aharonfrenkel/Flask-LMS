class ValidationConstants:
    class Password:
        MIN_LENGTH = 8
        PATTERN = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])"
        ERROR_MESSAGES = {
            'length': 'Password length must be at least 8 characters',
            'pattern': ('Password must contain at least one lowercase letter, '
                        'one uppercase letter, one digit, and one special character (@$!%*?&)')
        }

    class Name:
        ERROR_MESSAGES = {
            'length': {
                'pattern': 'Name must contain only English letters',
                'first_name': 'First name length must be between 2 and 20 characters',
                'last_name': 'Last name length must be between 2 and 20 characters',
                'general': 'Name length must be between 2 and 255 characters'
            }
        }

    class Phone:
        PATTERN = r"^05\d{8}$"
        ERROR_MESSAGES = {
            'pattern': 'Phone number must be in Israeli format (05X-XXXXXXX)'
        }

    class Email:
        PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        ERROR_MESSAGES = {
            'format': 'Invalid email format'
        }

    class Score:
        ERROR_MESSAGES = {
            'range': 'Score must be between 0 and 100'
        }

    class Feedback:
        ERROR_MESSAGES = {
            'length': 'Feedback length must be between 1 and 255 characters'
        }

    class ResetPassword:
        ERROR_MESSAGES = {
            'general_error': """The password reset request cannot be completed. 
            Please verify your email address and reset code, 
            or request a new password reset if needed."""
        }