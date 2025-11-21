from django.urls import path

from . import views

urlpatterns = [
    path("", views.site_select, name="rockart-home"),
    path("sites/<int:site_id>/project/", views.project_info, name="rockart-project"),
    path("sites/<int:site_id>/rock-art/", views.rock_art, name="rockart-rock-art"),
    path("sites/<int:site_id>/panel/", views.panel_view, name="rockart-panel"),
    path(
        "sites/<int:site_id>/conditions/",
        views.conditions_view,
        name="rockart-conditions",
    ),
    path(
        "sites/<int:site_id>/attributes/",
        views.attributes_view,
        name="rockart-attributes",
    ),
    path(
        "sites/<int:site_id>/inventory/anthropomorphs/",
        views.inventory_anthro_view,
        name="rockart-inventory-anthro",
    ),
    path(
        "sites/<int:site_id>/inventory/continued/",
        views.inventory_continued_view,
        name="rockart-inventory-continued",
    ),
    path(
        "sites/<int:site_id>/photogrammetry/",
        views.photogrammetry_view,
        name="rockart-photogrammetry",
    ),
    path("sites/<int:site_id>/notes/", views.notes_view, name="rockart-notes"),
]
