from django.urls import include, path
from rest_framework.routers import DefaultRouter

from rockart.api import views

router = DefaultRouter()
router.register("sites", views.SiteViewSet)
router.register("rock-art-types", views.RockArtTypeViewSet)
router.register("rock-art-categories", views.RockArtCategoryViewSet)
router.register("rock-art-info", views.RockArtInfoViewSet)
router.register("panels", views.PanelViewSet)
router.register("rock-art-conditions", views.RockArtConditionViewSet)
router.register("rock-art-attributes", views.RockArtAttributesViewSet)
router.register("anthropomorph-inventories", views.AnthropomorphInventoryViewSet)
router.register("enigmatic-inventories", views.EnigmaticInventoryViewSet)
router.register("zoomorph-inventories", views.ZoomorphInventoryViewSet)
router.register(
    "general-iconographic-attributes", views.GeneralIconographicAttributesViewSet
)
router.register("photogrammetry-logs", views.PhotogrammetryLogEntryViewSet)
router.register("rock-art-notes", views.RockArtNoteViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("graphql/", views.GraphQLAPIView.as_view(), name="graphql-api"),
]
