from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods

from .forms import CashflowRecordForm, RecordFilterForm
from .models import CashflowRecord, Category, Subcategory


@require_http_methods(["GET"])
def record_list(request):
    form = RecordFilterForm(request.GET or None)
    records = CashflowRecord.objects.select_related(
        "status", "type", "category", "subcategory"
    )

    if form.is_valid():
        data = form.cleaned_data
        if data.get("date_from"):
            records = records.filter(date__gte=data["date_from"])
        if data.get("date_to"):
            records = records.filter(date__lte=data["date_to"])
        if data.get("status"):
            records = records.filter(status=data["status"])
        if data.get("type"):
            records = records.filter(type=data["type"])
        if data.get("category"):
            records = records.filter(category=data["category"])
        if data.get("subcategory"):
            records = records.filter(subcategory=data["subcategory"])

    context = {
        "form": form,
        "records": records,
    }
    return render(request, "records_list.html", context)


@require_http_methods(["GET", "POST"])
def record_create(request):
    form = CashflowRecordForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("records:list")

    context = {
        "form": form,
        "title": "Новая запись",
    }
    return render(request, "record_form.html", context)


@require_http_methods(["GET", "POST"])
def record_update(request, pk):
    record = get_object_or_404(CashflowRecord, pk=pk)
    form = CashflowRecordForm(request.POST or None, instance=record)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("records:list")

    context = {
        "form": form,
        "title": "Редактирование записи",
    }
    return render(request, "record_form.html", context)


@require_http_methods(["GET", "POST"])
def record_delete(request, pk):
    record = get_object_or_404(CashflowRecord, pk=pk)
    if request.method == "POST":
        record.delete()
        return redirect("records:list")

    context = {
        "record": record,
    }
    return render(request, "record_confirm_delete.html", context)


@require_GET
def ajax_categories(request):
    type_id = request.GET.get("type_id")
    categories = Category.objects.none()
    if type_id:
        categories = Category.objects.filter(type_id=type_id).order_by("name")

    data = [{"id": item.id, "name": item.name} for item in categories]
    return JsonResponse({"results": data})


@require_GET
def ajax_subcategories(request):
    category_id = request.GET.get("category_id")
    subcategories = Subcategory.objects.none()
    if category_id:
        subcategories = Subcategory.objects.filter(category_id=category_id).order_by(
            "name"
        )

    data = [{"id": item.id, "name": item.name} for item in subcategories]
    return JsonResponse({"results": data})
