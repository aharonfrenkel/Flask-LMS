class GeneralConstants:
    class Score:
        MIN = 0
        MAX = 100

    class Time:
        DEFAULT_EXERCISE_TARGET_DAYS = 7
        DEFAULT_TOKEN_EXPIRATION_HOURS = 1
        DEFAULT_SESSION_LIFETIME_WEEKS = 3

    class Status:
        PENDING = "pending"
        SUBMITTED = "submitted"
        GRADED = "graded"
        CHOICES = [PENDING, SUBMITTED, GRADED]