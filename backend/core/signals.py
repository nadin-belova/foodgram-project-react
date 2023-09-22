from pathlib import Path

from django.db.models.signals import post_delete
from django.dispatch import receiver
from recipes.models import Recipe


@receiver(post_delete, sender=Recipe)
def delete_image(sender: Recipe, instance: Recipe, *a, **kw) -> None:
    """
    Удаляет изображение, связанное с рецептом, после удаления рецепта.

    :param sender: Класс модели, отправляющий сигнал (Recipe в данном случае).
    :param instance: Экземпляр модели, который был удален (рецепт).
    :param a: Позиционные аргументы.
    :param kw: Аргументы ключевых слов.
    :return: None
    """
    image = Path(instance.image.path)
    if image.exists():
        image.unlink()
