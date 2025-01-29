class ModelConstants:
    class StringLength:
        MIN_NAME = 2
        MAX_NAME = 255

        MIN_FIRST_NAME = 2
        MAX_FIRST_NAME = 20

        MIN_LAST_NAME = 2
        MAX_LAST_NAME = 20

        EQUAL_PHONE = 10

        MAX_EMAIL = 80
        MAX_PASSWORD = 80
        MAX_FEEDBACK = 255
        MAX_STATUS = 20
        MAX_TOKEN = 128
        TOKEN_ENTROPY_BYTES = 8
        MAX_IP_ADDRESS = 45
        MAX_USER_AGENT = 255


    class DefaultValues:
        DEFAULT_IS_MANDATORY = True
        DEFAULT_STATUS = "pending"

    class TokenStatus:
        ACTIVE = "active"
        USED = "used"
        INVALIDATED = "invalidated"
        CHOICES = [ACTIVE, USED, INVALIDATED]