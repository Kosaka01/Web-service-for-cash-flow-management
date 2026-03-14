from django.urls import path

from . import views

app_name = "records"

urlpatterns = [
    path("", views.record_list, name="list"),
    path("records/new", views.record_create, name="create"),
    path("records/<int:pk>/edit", views.record_update, name="edit"),
    path("records/<int:pk>/delete", views.record_delete, name="delete"),
    path("ajax/categories", views.ajax_categories, name="ajax_categories"),
    path("ajax/subcategories", views.ajax_subcategories, name="ajax_subcategories"),
]
