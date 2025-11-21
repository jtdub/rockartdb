import graphene
from graphene_django import DjangoObjectType

from rockart import models


class SiteType(DjangoObjectType):
    class Meta:
        model = models.Site
        fields = "__all__"


class RockArtInfoType(DjangoObjectType):
    class Meta:
        model = models.RockArtInfo
        fields = "__all__"


class PanelType(DjangoObjectType):
    class Meta:
        model = models.Panel
        fields = "__all__"


class RockArtConditionType(DjangoObjectType):
    class Meta:
        model = models.RockArtCondition
        fields = "__all__"


class RockArtAttributesType(DjangoObjectType):
    class Meta:
        model = models.RockArtAttributes
        fields = "__all__"


class RockArtNoteType(DjangoObjectType):
    class Meta:
        model = models.RockArtNote
        fields = "__all__"


class PhotogrammetryLogEntryType(DjangoObjectType):
    class Meta:
        model = models.PhotogrammetryLogEntry
        fields = "__all__"


class RockArtTypeType(DjangoObjectType):
    class Meta:
        model = models.RockArtType
        fields = "__all__"


class RockArtCategoryType(DjangoObjectType):
    class Meta:
        model = models.RockArtCategory
        fields = "__all__"


class AnthropomorphInventoryType(DjangoObjectType):
    class Meta:
        model = models.AnthropomorphInventory
        fields = "__all__"


class EnigmaticInventoryType(DjangoObjectType):
    class Meta:
        model = models.EnigmaticInventory
        fields = "__all__"


class ZoomorphInventoryType(DjangoObjectType):
    class Meta:
        model = models.ZoomorphInventory
        fields = "__all__"


class GeneralIconographicAttributesType(DjangoObjectType):
    class Meta:
        model = models.GeneralIconographicAttributes
        fields = "__all__"


class Query(graphene.ObjectType):
    sites = graphene.List(SiteType)
    site = graphene.Field(SiteType, id=graphene.Int(required=True))

    rock_art_info = graphene.List(RockArtInfoType)
    panels = graphene.List(PanelType)
    notes = graphene.List(RockArtNoteType)
    photogrammetry_entries = graphene.List(PhotogrammetryLogEntryType)
    rock_art_types = graphene.List(RockArtTypeType)
    rock_art_categories = graphene.List(RockArtCategoryType)
    conditions = graphene.List(RockArtConditionType)
    attributes = graphene.List(RockArtAttributesType)
    anthropomorph_inventories = graphene.List(AnthropomorphInventoryType)
    enigmatic_inventories = graphene.List(EnigmaticInventoryType)
    zoomorph_inventories = graphene.List(ZoomorphInventoryType)
    general_iconographic_attributes = graphene.List(GeneralIconographicAttributesType)

    def resolve_sites(root, info):
        return models.Site.objects.all()

    def resolve_site(root, info, id):
        return models.Site.objects.filter(pk=id).first()

    def resolve_rock_art_info(root, info):
        return models.RockArtInfo.objects.select_related("site").all()

    def resolve_panels(root, info):
        return models.Panel.objects.select_related("site").all()

    def resolve_notes(root, info):
        return models.RockArtNote.objects.select_related("site").all()

    def resolve_photogrammetry_entries(root, info):
        return models.PhotogrammetryLogEntry.objects.select_related("site").all()

    def resolve_rock_art_types(root, info):
        return models.RockArtType.objects.all()

    def resolve_rock_art_categories(root, info):
        return models.RockArtCategory.objects.all()

    def resolve_conditions(root, info):
        return models.RockArtCondition.objects.select_related("site").all()

    def resolve_attributes(root, info):
        return models.RockArtAttributes.objects.select_related(
            "site", "rock_art_category"
        ).all()

    def resolve_anthropomorph_inventories(root, info):
        return models.AnthropomorphInventory.objects.select_related("site").all()

    def resolve_enigmatic_inventories(root, info):
        return models.EnigmaticInventory.objects.select_related("site").all()

    def resolve_zoomorph_inventories(root, info):
        return models.ZoomorphInventory.objects.select_related("site").all()

    def resolve_general_iconographic_attributes(root, info):
        return models.GeneralIconographicAttributes.objects.select_related("site").all()


schema = graphene.Schema(query=Query)
