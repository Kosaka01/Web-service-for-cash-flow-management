from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Status(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey(Type, on_delete=models.PROTECT, related_name="categories")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["type__name", "name"]
        constraints = [
            models.UniqueConstraint(fields=["type", "name"], name="unique_category_per_type"),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.type.name})"


class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="subcategories"
    )

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        ordering = ["category__name", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["category", "name"], name="unique_subcategory_per_category"
            ),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.category.name})"


class CashflowRecord(models.Model):
    date = models.DateField(default=timezone.localdate)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, related_name="records")
    type = models.ForeignKey(Type, on_delete=models.PROTECT, related_name="records")
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="records"
    )
    subcategory = models.ForeignKey(
        Subcategory, on_delete=models.PROTECT, related_name="records"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Запись ДДС"
        verbose_name_plural = "Записи ДДС"
        ordering = ["-date", "-id"]

    def __str__(self) -> str:
        return f"{self.date} · {self.amount}"

    def clean(self) -> None:
        errors = {}

        if self.category and self.type:
            if self.category.type_id != self.type_id:
                errors["category"] = "Категория не относится к выбранному типу."

        if self.subcategory and self.category:
            if self.subcategory.category_id != self.category_id:
                errors["subcategory"] = "Подкатегория не относится к выбранной категории."

        if self.subcategory and not self.category:
            errors["subcategory"] = "Сначала выберите категорию."

        if errors:
            raise ValidationError(errors)
