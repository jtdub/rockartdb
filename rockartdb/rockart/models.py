from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# ----------------------------------------------------------------------
# Core / Project Information tab
# ----------------------------------------------------------------------


class Site(TimeStampedModel):
    """
    Core record for a rock art site.
    """

    site_number = models.CharField(max_length=64, unique=True)
    date_recorded = models.DateField(null=True, blank=True)

    project_name = models.CharField(max_length=255, blank=True)
    project_description = models.TextField(blank=True)
    recorders = models.CharField(
        max_length=255,
        blank=True,
        help_text="Names of recorder(s) as entered on the form.",
    )

    temporary_housing = models.CharField(
        max_length=255, blank=True, help_text="Temporary data housing."
    )
    permanent_housing = models.CharField(
        max_length=255, blank=True, help_text="Permanent data housing (e.g. TARL)."
    )

    def __str__(self) -> str:
        return self.site_number


# ----------------------------------------------------------------------
# Shared vocabularies
# ----------------------------------------------------------------------


class LocationType(models.TextChoices):
    UNKNOWN = "unknown", "Unknown"
    ROCK_SHELTER = "rock_shelter", "Rock shelter"
    CAVE = "cave", "Cave"
    OPEN_AIR = "open_air", "Open air"
    OTHER = "other", "Other"


class PhotoType(models.TextChoices):
    SFM = "sfm", "SfM"
    GIGAPAN = "gigapan", "Gigapan"
    OTHER = "other", "Other"


class NoteType(models.TextChoices):
    SITE_NARRATIVE = "site_narrative", "Site Narrative"
    ICONOGRAPHIC_INVENTORY = "iconographic_inventory", "Iconographic Inventory"
    DAILY_RECORDER = "daily_recorder", "Daily Recorder"


class NoteCategory(models.TextChoices):
    FIELD = "field", "Field"
    LAB = "lab", "Lab"


class RockArtTechnique(models.TextChoices):
    NONE = "none", "None"
    PECKED = "pecked", "Pecked"
    INCISED = "incised", "Incised"
    POLISHED = "polished", "Polished"
    OTHER = "other", "Other"


class PaintingTechnique(models.TextChoices):
    NONE = "none", "None"
    WET_APPLIED = "wet_applied", "Wet-applied"
    DRY_APPLIED = "dry_applied", "Dry-applied"
    FINGER_PAINTED = "finger_painted", "Finger-painted"
    STENCILED = "stenciled", "Stenciled"
    BLOWN = "blown", "Blown"
    SPLATTER = "splatter", "Splatter"
    OTHER = "other", "Other"


# These hold values like "Pictographs", "Figurative Petroglyphs",
# "Pecos River Style", "Red Linear", etc., which you can seed via fixtures.
class RockArtType(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self) -> str:
        return self.name


class RockArtCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self) -> str:
        return self.name


# ----------------------------------------------------------------------
# Rock Art tab (general character, techniques, photography)
# ----------------------------------------------------------------------


class RockArtInfo(TimeStampedModel):
    site = models.OneToOneField(Site, on_delete=models.CASCADE, related_name="rock_art")

    reason_for_visit = models.TextField(blank=True)
    previously_recorded = models.BooleanField(default=False)
    previous_record_details = models.TextField(blank=True)

    location_type = models.CharField(
        max_length=32,
        choices=LocationType.choices,
        default=LocationType.UNKNOWN,
        blank=True,
    )

    rock_art_types = models.ManyToManyField(
        RockArtType, blank=True, related_name="sites"
    )
    rock_art_categories = models.ManyToManyField(
        RockArtCategory, blank=True, related_name="sites"
    )

    radiocarbon_assay = models.CharField(
        max_length=64, blank=True, help_text="Assay number or 'None'."
    )
    radiocarbon_citation = models.TextField(blank=True)

    unidentified_description = models.TextField(
        blank=True, help_text="Description if category is 'Unidentified'."
    )

    # Best time of day for photography
    best_winter = models.CharField(max_length=64, blank=True)
    best_spring = models.CharField(max_length=64, blank=True)
    best_summer = models.CharField(max_length=64, blank=True)
    best_fall = models.CharField(max_length=64, blank=True)

    # Prevailing techniques
    engraving_technique = models.CharField(
        max_length=32,
        choices=RockArtTechnique.choices,
        default=RockArtTechnique.NONE,
        blank=True,
    )
    engraving_other = models.CharField(max_length=128, blank=True)

    painting_technique = models.CharField(
        max_length=32,
        choices=PaintingTechnique.choices,
        default=PaintingTechnique.NONE,
        blank=True,
    )
    painting_other = models.CharField(max_length=128, blank=True)

    def __str__(self) -> str:
        return f"Rock Art Info for {self.site}"


# ----------------------------------------------------------------------
# Rock Art Panel tab
# ----------------------------------------------------------------------


class Panel(TimeStampedModel):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="panels")

    panel_number = models.PositiveIntegerField()
    overall_shelter_orientation = models.CharField(
        max_length=64, blank=True, help_text="Cardinal orientation, degrees, etc."
    )

    height_m = models.FloatField(default=0.0)
    width_m = models.FloatField(default=0.0)
    area_m2 = models.FloatField(default=0.0)
    exposure_degrees = models.FloatField(
        default=0.0, help_text="Panel exposure in degrees as recorded on form."
    )

    # Number of images within panel (initial / final counts)
    anthropomorphs_initial = models.PositiveIntegerField(default=0)
    anthropomorphs_final = models.PositiveIntegerField(default=0)

    enigmatics_initial = models.PositiveIntegerField(default=0)
    enigmatics_final = models.PositiveIntegerField(default=0)

    zoomorphs_initial = models.PositiveIntegerField(default=0)
    zoomorphs_final = models.PositiveIntegerField(default=0)

    graffiti_initial = models.PositiveIntegerField(default=0)
    graffiti_final = models.PositiveIntegerField(default=0)

    remnant_initial = models.PositiveIntegerField(default=0)
    remnant_final = models.PositiveIntegerField(default=0)

    unclassified_initial = models.PositiveIntegerField(default=0)
    unclassified_final = models.PositiveIntegerField(default=0)

    figurative_petros_initial = models.PositiveIntegerField(default=0)
    figurative_petros_final = models.PositiveIntegerField(default=0)

    grooves_initial = models.PositiveIntegerField(default=0)
    grooves_final = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("site", "panel_number")

    def __str__(self) -> str:
        return f"{self.site} - Panel {self.panel_number}"


# ----------------------------------------------------------------------
# Rock Art Conditions tab
# ----------------------------------------------------------------------


class RockArtCondition(TimeStampedModel):
    site = models.OneToOneField(
        Site, on_delete=models.CASCADE, related_name="conditions"
    )

    # Rock art assemblage characteristics
    repainting = models.CharField(max_length=128, blank=True)
    repainting_comments = models.TextField(blank=True)

    revarnishing = models.CharField(max_length=128, blank=True)
    revarnishing_comments = models.TextField(blank=True)

    clarity_overall = models.CharField(
        max_length=128, blank=True, help_text="Clarity of art (overall)."
    )

    # Agents of deterioration – each dropdown mapped to free text plus notes
    physical_agent = models.CharField(max_length=128, blank=True)
    physical_notes = models.TextField(blank=True)

    chemical_agent = models.CharField(max_length=128, blank=True)
    chemical_notes = models.TextField(blank=True)

    biochemical_agent = models.CharField(max_length=128, blank=True)
    biochemical_notes = models.TextField(blank=True)

    human_impacts = models.CharField(max_length=128, blank=True)
    human_impacts_notes = models.TextField(blank=True)

    animal_impacts = models.CharField(max_length=128, blank=True)
    animal_impacts_notes = models.TextField(blank=True)

    known_or_perceived_future_impacts = models.TextField(blank=True)
    future_research_potential = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"Conditions for {self.site}"


# ----------------------------------------------------------------------
# Rock Art Attributes tab
# ----------------------------------------------------------------------


class RockArtAttributes(TimeStampedModel):
    site = models.OneToOneField(
        Site, on_delete=models.CASCADE, related_name="attributes"
    )

    rock_art_category = models.ForeignKey(
        RockArtCategory,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="attribute_sets",
    )
    style_description = models.TextField(blank=True)

    # Post-painting modification (pecking, abrading, incising, etc.)
    post_pecking = models.CharField(max_length=128, blank=True)
    post_abrading = models.CharField(max_length=128, blank=True)
    post_incising = models.CharField(max_length=128, blank=True)
    post_additional_comments = models.TextField(blank=True)

    # General attributes
    incorporation = models.CharField(
        max_length=128, blank=True, help_text="E.g. use of natural features."
    )
    scaffolding_required = models.CharField(
        max_length=64, blank=True, help_text="Yes/No/Unknown as recorded."
    )
    potential_for_c14 = models.CharField(max_length=64, blank=True)
    general_comments = models.TextField(blank=True)

    # Colors present in style (checkboxes on the form)
    has_black = models.BooleanField(default=False)
    has_red = models.BooleanField(default=False)
    has_yellow = models.BooleanField(default=False)
    has_white = models.BooleanField(default=False)
    other_colors = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return f"Attributes for {self.site}"


# ----------------------------------------------------------------------
# Iconographic Inventory – Anthropomorphs tab
# (Each field is a count of figures with that attribute.)
# ----------------------------------------------------------------------


class AnthropomorphInventory(TimeStampedModel):
    site = models.OneToOneField(
        Site, on_delete=models.CASCADE, related_name="anthropomorph_inventory"
    )

    # General
    frontal = models.PositiveIntegerField(default=0)
    profile = models.PositiveIntegerField(default=0)
    upside_down = models.PositiveIntegerField(default=0)
    horizontal = models.PositiveIntegerField(default=0)
    impaled_anthropomorph = models.PositiveIntegerField(default=0)
    centralstyling = models.PositiveIntegerField(default=0)
    non_centralstyled = models.PositiveIntegerField(default=0)

    # Headshapes (subset – extend as needed)
    headshape_round = models.PositiveIntegerField(default=0)
    headshape_square = models.PositiveIntegerField(default=0)
    headshape_u_shape = models.PositiveIntegerField(default=0)
    headshape_other = models.PositiveIntegerField(default=0)

    # Body (subset)
    arms_extended_up = models.PositiveIntegerField(default=0)
    arms_extended_down = models.PositiveIntegerField(default=0)
    right_handed = models.PositiveIntegerField(default=0)
    left_handed = models.PositiveIntegerField(default=0)

    # Adornments / paraphernalia (subset)
    headdress = models.PositiveIntegerField(default=0)
    mask = models.PositiveIntegerField(default=0)
    staff = models.PositiveIntegerField(default=0)
    rabbit_stick = models.PositiveIntegerField(default=0)
    other_paraphernalia = models.PositiveIntegerField(default=0)

    # Old inventory fields etc. can be continued here.

    def __str__(self) -> str:
        return f"Anthropomorph Inventory for {self.site}"


# ----------------------------------------------------------------------
# Iconographic Inventory – Continued (Enigmatics, Zoomorphs, etc.)
# ----------------------------------------------------------------------


class EnigmaticInventory(TimeStampedModel):
    site = models.OneToOneField(
        Site, on_delete=models.CASCADE, related_name="enigmatic_inventory"
    )

    box_with_legs = models.PositiveIntegerField(default=0)
    arch_with_portal = models.PositiveIntegerField(default=0)
    crenelated_box = models.PositiveIntegerField(default=0)
    comb_shape = models.PositiveIntegerField(default=0)
    grid = models.PositiveIntegerField(default=0)
    zig_zag_line = models.PositiveIntegerField(default=0)
    spiral = models.PositiveIntegerField(default=0)
    serpentine_lines = models.PositiveIntegerField(default=0)
    other_enigmatics = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"Enigmatic Inventory for {self.site}"


class ZoomorphInventory(TimeStampedModel):
    site = models.OneToOneField(
        Site, on_delete=models.CASCADE, related_name="zoomorph_inventory"
    )

    feline = models.PositiveIntegerField(default=0)
    avian = models.PositiveIntegerField(default=0)
    snakes = models.PositiveIntegerField(default=0)
    antlered_deer = models.PositiveIntegerField(default=0)
    deer_without_antlers = models.PositiveIntegerField(default=0)
    other_zoomorphs = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"Zoomorph Inventory for {self.site}"


class GeneralIconographicAttributes(TimeStampedModel):
    site = models.OneToOneField(
        Site, on_delete=models.CASCADE, related_name="general_iconographic_attributes"
    )

    antlers_with_dots = models.PositiveIntegerField(default=0)
    speech_breath = models.PositiveIntegerField(default=0)
    large_cluster_single_motif = models.PositiveIntegerField(default=0)
    half_bodied_figures = models.PositiveIntegerField(default=0)
    full_bodied_figures = models.PositiveIntegerField(default=0)
    dismembered_figures = models.PositiveIntegerField(default=0)
    procession_of_anthropomorphs = models.PositiveIntegerField(default=0)
    procession_of_zoomorphs = models.PositiveIntegerField(default=0)
    peyotism_motif = models.PositiveIntegerField(default=0)
    otherworld_journey_motif = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"General Iconographic Attributes for {self.site}"


# ----------------------------------------------------------------------
# Photogrammetry tab
# ----------------------------------------------------------------------


class PhotogrammetryLogEntry(TimeStampedModel):
    site = models.ForeignKey(
        Site, on_delete=models.CASCADE, related_name="photogrammetry_logs"
    )

    date = models.DateField()
    photo_type = models.CharField(
        max_length=16, choices=PhotoType.choices, default=PhotoType.SFM
    )
    photo_range = models.CharField(
        max_length=128, blank=True, help_text="Photo number range or identifier."
    )
    scale_used = models.CharField(max_length=128, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["site", "date"]

    def __str__(self) -> str:
        return f"{self.site} photogrammetry on {self.date}"


# ----------------------------------------------------------------------
# Rock Art Notes tab
# ----------------------------------------------------------------------


class RockArtNote(TimeStampedModel):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name="notes")

    author = models.CharField(max_length=128, blank=True)
    date = models.DateField(null=True, blank=True)

    note_type = models.CharField(
        max_length=32,
        choices=NoteType.choices,
        default=NoteType.SITE_NARRATIVE,
    )
    category = models.CharField(
        max_length=16,
        choices=NoteCategory.choices,
        default=NoteCategory.FIELD,
    )

    text = models.TextField()

    class Meta:
        ordering = ["site", "date", "created_at"]

    def __str__(self) -> str:
        return f"{self.get_note_type_display()} note for {self.site}"
