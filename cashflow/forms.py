from django import forms
from django.utils import timezone

from .models import CashflowRecord, Category, Subcategory, Status, Type


class CashflowRecordForm(forms.ModelForm):
    date = forms.DateField(
        label="Дата",
        required=True,
        initial=timezone.localdate,
        widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        input_formats=["%Y-%m-%d", "%d.%m.%Y"],
    )
    amount = forms.DecimalField(
        label="Сумма",
        min_value=0.01,
        max_digits=12,
        decimal_places=2,
    )

    class Meta:
        model = CashflowRecord
        fields = [
            "date",
            "status",
            "type",
            "category",
            "subcategory",
            "amount",
            "comment",
        ]
        widgets = {
            "comment": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_base_styles()
        self.fields["status"].queryset = Status.objects.all()
        self.fields["type"].queryset = Type.objects.all()
        self.fields["category"].queryset = Category.objects.none()
        self.fields["subcategory"].queryset = Subcategory.objects.none()

        if self.instance and self.instance.pk:
            self.fields["category"].queryset = Category.objects.filter(
                type=self.instance.type
            )
            self.fields["subcategory"].queryset = Subcategory.objects.filter(
                category=self.instance.category
            )

        data = self.data or None
        if data:
            type_id = data.get("type")
            if type_id:
                self.fields["category"].queryset = Category.objects.filter(
                    type_id=type_id
                )

            category_id = data.get("category")
            if category_id:
                self.fields["subcategory"].queryset = Subcategory.objects.filter(
                    category_id=category_id
                )

    def clean(self):
        cleaned_data = super().clean()
        record_type = cleaned_data.get("type")
        category = cleaned_data.get("category")
        subcategory = cleaned_data.get("subcategory")

        if category and record_type and category.type_id != record_type.id:
            self.add_error("category", "Категория не относится к выбранному типу.")

        if subcategory and category and subcategory.category_id != category.id:
            self.add_error(
                "subcategory", "Подкатегория не относится к выбранной категории."
            )

        if subcategory and not category:
            self.add_error("subcategory", "Сначала выберите категорию.")

        return cleaned_data

    def _apply_base_styles(self) -> None:
        for name, field in self.fields.items():
            if name in {"status", "type", "category", "subcategory"}:
                field.widget.attrs.setdefault("class", "form-select")
            elif name == "comment":
                field.widget.attrs.setdefault("class", "form-control")
            else:
                field.widget.attrs.setdefault("class", "form-control")
            if name == "amount":
                field.widget.attrs.setdefault("step", "0.01")


class RecordFilterForm(forms.Form):
    date_from = forms.DateField(
        label="Дата с",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        input_formats=["%Y-%m-%d", "%d.%m.%Y"],
    )
    date_to = forms.DateField(
        label="Дата по",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        input_formats=["%Y-%m-%d", "%d.%m.%Y"],
    )
    status = forms.ModelChoiceField(
        label="Статус", queryset=Status.objects.none(), required=False
    )
    type = forms.ModelChoiceField(
        label="Тип", queryset=Type.objects.none(), required=False
    )
    category = forms.ModelChoiceField(
        label="Категория", queryset=Category.objects.none(), required=False
    )
    subcategory = forms.ModelChoiceField(
        label="Подкатегория", queryset=Subcategory.objects.none(), required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_base_styles()
        self.fields["status"].queryset = Status.objects.all()
        self.fields["type"].queryset = Type.objects.all()
        self.fields["category"].queryset = Category.objects.all()
        self.fields["subcategory"].queryset = Subcategory.objects.all()

        data = self.data or None
        if data:
            type_id = data.get("type")
            if type_id:
                self.fields["category"].queryset = Category.objects.filter(
                    type_id=type_id
                )

            category_id = data.get("category")
            if category_id:
                self.fields["subcategory"].queryset = Subcategory.objects.filter(
                    category_id=category_id
                )

    def _apply_base_styles(self) -> None:
        for name, field in self.fields.items():
            if name in {"status", "type", "category", "subcategory"}:
                field.widget.attrs.setdefault("class", "form-select")
            else:
                field.widget.attrs.setdefault("class", "form-control")
