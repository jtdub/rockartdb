from django import forms

from .models import (
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


class BootstrapMixin:
    """
    Add Bootstrap form-control classes to inputs for quick styling.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, (forms.CheckboxInput, forms.CheckboxSelectMultiple)):
                widget.attrs.setdefault("class", "form-check-input")
            elif isinstance(widget, forms.DateInput):
                widget.attrs.setdefault("class", "form-control")
                widget.attrs.setdefault("type", "date")
            else:
                widget.attrs.setdefault("class", "form-control")


class SiteForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Site
        fields = [
            "site_number",
            "date_recorded",
            "project_name",
            "project_description",
            "recorders",
            "temporary_housing",
            "permanent_housing",
        ]
        widgets = {
            "date_recorded": forms.DateInput(attrs={"type": "date"}),
            "project_description": forms.Textarea(attrs={"rows": 3}),
        }


class RockArtInfoForm(BootstrapMixin, forms.ModelForm):
    rock_art_types = forms.ModelMultipleChoiceField(
        queryset=RockArtType.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    rock_art_categories = forms.ModelMultipleChoiceField(
        queryset=RockArtCategory.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = RockArtInfo
        exclude = ["site"]
        widgets = {
            "radiocarbon_citation": forms.Textarea(attrs={"rows": 2}),
            "unidentified_description": forms.Textarea(attrs={"rows": 2}),
        }


class PanelForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Panel
        exclude = ["site"]


class RockArtConditionForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = RockArtCondition
        exclude = ["site"]
        widgets = {
            "repainting_comments": forms.Textarea(attrs={"rows": 2}),
            "revarnishing_comments": forms.Textarea(attrs={"rows": 2}),
            "chemical_notes": forms.Textarea(attrs={"rows": 2}),
            "biochemical_notes": forms.Textarea(attrs={"rows": 2}),
            "physical_notes": forms.Textarea(attrs={"rows": 2}),
            "human_impacts_notes": forms.Textarea(attrs={"rows": 2}),
            "animal_impacts_notes": forms.Textarea(attrs={"rows": 2}),
            "known_or_perceived_future_impacts": forms.Textarea(attrs={"rows": 2}),
            "future_research_potential": forms.Textarea(attrs={"rows": 2}),
        }


class RockArtAttributesForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = RockArtAttributes
        exclude = ["site"]
        widgets = {
            "style_description": forms.Textarea(attrs={"rows": 2}),
            "post_additional_comments": forms.Textarea(attrs={"rows": 2}),
            "general_comments": forms.Textarea(attrs={"rows": 2}),
        }


class AnthropomorphInventoryForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = AnthropomorphInventory
        exclude = ["site"]


class EnigmaticInventoryForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = EnigmaticInventory
        exclude = ["site"]


class ZoomorphInventoryForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = ZoomorphInventory
        exclude = ["site"]


class GeneralIconographicAttributesForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = GeneralIconographicAttributes
        exclude = ["site"]


class PhotogrammetryLogEntryForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = PhotogrammetryLogEntry
        exclude = ["site"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 2}),
        }


class RockArtNoteForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = RockArtNote
        exclude = ["site"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "text": forms.Textarea(attrs={"rows": 3}),
        }
