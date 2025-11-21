from rest_framework import serializers

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


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = "__all__"


class RockArtTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RockArtType
        fields = "__all__"


class RockArtCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RockArtCategory
        fields = "__all__"


class RockArtInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RockArtInfo
        fields = "__all__"


class PanelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Panel
        fields = "__all__"


class RockArtConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RockArtCondition
        fields = "__all__"


class RockArtAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RockArtAttributes
        fields = "__all__"


class AnthropomorphInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AnthropomorphInventory
        fields = "__all__"


class EnigmaticInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EnigmaticInventory
        fields = "__all__"


class ZoomorphInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ZoomorphInventory
        fields = "__all__"


class GeneralIconographicAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralIconographicAttributes
        fields = "__all__"


class PhotogrammetryLogEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotogrammetryLogEntry
        fields = "__all__"


class RockArtNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RockArtNote
        fields = "__all__"
