import unicodedata

from core import texsts
from core.enums import Limits
from core.validators import MinLenValidator, OneOfTwoValidator
from django.contrib.auth.models import AbstractUser
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    CheckConstraint,
    DateTimeField,
    EmailField,
    F,
    ForeignKey,
    Model,
    Q,
    UniqueConstraint,
)
from django.db.models.functions import Length
from django.utils.translation import gettext_lazy as _

CharField.register_lookup(Length)


class MyUser(AbstractUser):
    """
    Пользователь
    """

    email = EmailField(
        verbose_name="Адрес электронной почты",
        max_length=Limits.MAX_LEN_EMAIL_FIELD.value,
        unique=True,
        help_text=texsts.USERS_HELP_EMAIL,
    )
    username = CharField(
        verbose_name="Уникальный юзернейм",
        max_length=Limits.MAX_LEN_USERS_CHARFIELD.value,
        unique=True,
        help_text=texsts.USERS_HELP_UNAME,
        validators=(
            MinLenValidator(
                min_len=Limits.MIN_LEN_USERNAME,
                field="username",
            ),
            OneOfTwoValidator(field="username"),
        ),
    )
    first_name = CharField(
        verbose_name="Имя",
        max_length=Limits.MAX_LEN_USERS_CHARFIELD.value,
        help_text=texsts.USERS_HELP_FNAME,
        validators=(
            OneOfTwoValidator(
                first_regex="[^а-яёА-ЯЁ -]+",
                second_regex="[^a-zA-Z -]+",
                field="Имя",
            ),
        ),
    )
    last_name = CharField(
        verbose_name="Фамилия",
        max_length=Limits.MAX_LEN_USERS_CHARFIELD.value,
        help_text=texsts.USERS_HELP_FNAME,
        validators=(
            OneOfTwoValidator(
                first_regex="[^а-яёА-ЯЁ -]+",
                second_regex="[^a-zA-Z -]+",
                field="Фамилия",
            ),
        ),
    )
    password = CharField(
        verbose_name=_("Пароль"),
        max_length=128,
        help_text=texsts.USERS_HELP_FNAME,
    )
    is_active = BooleanField(
        verbose_name="Активирован",
        default=True,
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("username",)
        constraints = (
            CheckConstraint(
                check=Q(username__length__gte=Limits.MIN_LEN_USERNAME.value),
                name="\nusername is too short\n",
            ),
        )

    def __str__(self) -> str:
        return f"{self.username}: {self.email}"

    @classmethod
    def normalize_email(cls, email: str) -> str:
        """
        Нормализация email-адреса путем приведения
        к нижнему регистру части с доменом.
        """
        email = email or ""
        try:
            email_name, domain_part = email.strip().rsplit("@", 1)
            email = email_name.lower() + "@" + domain_part.lower()
        except (ValueError, AttributeError):
            # Обработка случаев, когда email не
            # может быть разделен на имя и домен.
            # Например, если email равен None или не содержит символа "@".
            pass
        return email

    @classmethod
    def normalize_username(cls, username: str) -> str:
        """
        Нормализует имя пользователя, применяя Unicode-нормализацию
        формы NFKC и делая первую букву заглавной.
        """
        return unicodedata.normalize("NFKC", username).capitalize()

    def __normalize_human_names(self, name: str) -> str:
        """
        Нормализует имена пользователей,
        делая первую букву каждого слова заглавной.
        Вместо этой реализации,
        можно использовать встроенную функцию str.title().
        """
        return name.title()

    def clean(self) -> None:
        self.first_name = self.__normalize_human_names(self.first_name)
        self.last_name = self.__normalize_human_names(self.last_name)
        return super().clean()


class Subscriptions(Model):
    """
    Модель подписок пользователей на авторов рецептов.

    Attributes:
        author (MyUser): Автор рецепта, на которого оформлена подписка.
        user (MyUser): Пользователь, оформивший подписку на автора рецепта.
        date_added (DateTimeField): Дата создания подписки.
    """

    author = ForeignKey(
        verbose_name="Автор рецепта",
        related_name="subscribers",
        to=MyUser,
        on_delete=CASCADE,
    )
    user = ForeignKey(
        verbose_name="Подписчики",
        related_name="subscriptions",
        to=MyUser,
        on_delete=CASCADE,
    )
    date_added = DateTimeField(
        verbose_name="Дата создания подписки",
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = (
            UniqueConstraint(
                fields=("author", "user"),
                name="\nRepeat subscription\n",
            ),
            CheckConstraint(
                check=~Q(author=F("user")), name="\nNo self sibscription\n"
            ),
        )

    def __str__(self) -> str:
        return f"{self.user.username} -> {self.author.username}"
