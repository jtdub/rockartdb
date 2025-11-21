from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema

from rockart.graphql.schema import schema as gql_schema

from rockart.models import (
    AnthropomorphInventory,
    EnigmaticInventory,
    GeneralIconographicAttributes,
    Panel,
    PhotogrammetryLogEntry,
    RockArtAttributes,
    RockArtCategory,
    RockArtCondition,
    RockArtInfo,
    RockArtNote,
    RockArtType,
    Site,
    ZoomorphInventory,
)
from rockart.api.serializers import (
    AnthropomorphInventorySerializer,
    EnigmaticInventorySerializer,
    GeneralIconographicAttributesSerializer,
    PanelSerializer,
    PhotogrammetryLogEntrySerializer,
    RockArtAttributesSerializer,
    RockArtCategorySerializer,
    RockArtConditionSerializer,
    RockArtInfoSerializer,
    RockArtNoteSerializer,
    RockArtTypeSerializer,
    SiteSerializer,
    ZoomorphInventorySerializer,
)


class SiteViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all().order_by("site_number")
    serializer_class = SiteSerializer
    search_fields = ["site_number", "project_name"]


class RockArtTypeViewSet(viewsets.ModelViewSet):
    queryset = RockArtType.objects.all().order_by("name")
    serializer_class = RockArtTypeSerializer
    search_fields = ["name"]


class RockArtCategoryViewSet(viewsets.ModelViewSet):
    queryset = RockArtCategory.objects.all().order_by("name")
    serializer_class = RockArtCategorySerializer
    search_fields = ["name"]


class RockArtInfoViewSet(viewsets.ModelViewSet):
    queryset = RockArtInfo.objects.select_related("site").prefetch_related(
        "rock_art_types", "rock_art_categories"
    )
    serializer_class = RockArtInfoSerializer
    search_fields = ["site__site_number"]


class PanelViewSet(viewsets.ModelViewSet):
    queryset = Panel.objects.select_related("site").all()
    serializer_class = PanelSerializer
    search_fields = ["site__site_number", "panel_number"]


class RockArtConditionViewSet(viewsets.ModelViewSet):
    queryset = RockArtCondition.objects.select_related("site").all()
    serializer_class = RockArtConditionSerializer


class RockArtAttributesViewSet(viewsets.ModelViewSet):
    queryset = RockArtAttributes.objects.select_related("site", "rock_art_category")
    serializer_class = RockArtAttributesSerializer


class AnthropomorphInventoryViewSet(viewsets.ModelViewSet):
    queryset = AnthropomorphInventory.objects.select_related("site").all()
    serializer_class = AnthropomorphInventorySerializer


class EnigmaticInventoryViewSet(viewsets.ModelViewSet):
    queryset = EnigmaticInventory.objects.select_related("site").all()
    serializer_class = EnigmaticInventorySerializer


class ZoomorphInventoryViewSet(viewsets.ModelViewSet):
    queryset = ZoomorphInventory.objects.select_related("site").all()
    serializer_class = ZoomorphInventorySerializer


class GeneralIconographicAttributesViewSet(viewsets.ModelViewSet):
    queryset = GeneralIconographicAttributes.objects.select_related("site").all()
    serializer_class = GeneralIconographicAttributesSerializer


class PhotogrammetryLogEntryViewSet(viewsets.ModelViewSet):
    queryset = PhotogrammetryLogEntry.objects.select_related("site").all()
    serializer_class = PhotogrammetryLogEntrySerializer


class RockArtNoteViewSet(viewsets.ModelViewSet):
    queryset = RockArtNote.objects.select_related("site").all()
    serializer_class = RockArtNoteSerializer
    search_fields = ["site__site_number", "author", "text"]


class GraphQLRequestSerializer(serializers.Serializer):
    query = serializers.CharField(help_text="GraphQL query string")
    variables = serializers.JSONField(
        required=False, help_text="Optional variables object"
    )


class GraphQLAPIView(APIView):
    """
    REST-friendly endpoint for executing GraphQL queries.
    """

    @extend_schema(
        summary="Execute GraphQL query",
        request=GraphQLRequestSerializer,
        responses={
            200: OpenApiResponse(
                description="GraphQL response payload",
            )
        },
        examples=[
            OpenApiExample(
                "List sites",
                value={"query": "{ sites { siteNumber } }"},
            )
        ],
    )
    def post(self, request):
        serializer = GraphQLRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        query = serializer.validated_data["query"]
        variables = serializer.validated_data.get("variables")
        result = gql_schema.execute(
            query, variable_values=variables, context_value=request
        )
        resp_data = {}
        if result.errors:
            resp_data["errors"] = [str(err) for err in result.errors]
        if result.data:
            resp_data["data"] = result.data
        return Response(resp_data)
