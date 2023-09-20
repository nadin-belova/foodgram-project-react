from core.enums import Limits

USERS_HELP_EMAIL = (
    "Обязательно для заполнения. "
    f"Максимум {Limits.MAX_LEN_EMAIL_FIELD} букв."
)
USERS_HELP_UNAME = (
    "Обязательно для заполнения. "
    f"От {Limits.MIN_LEN_USERNAME} до {Limits.MAX_LEN_USERS_CHARFIELD} букв."
)

USERS_HELP_FNAME = (
    "Обязательно для заполнения. "
    f"Максимум {Limits.MAX_LEN_USERS_CHARFIELD} букв."
)
