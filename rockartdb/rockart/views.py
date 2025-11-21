from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    AnthropomorphInventoryForm,
    EnigmaticInventoryForm,
    GeneralIconographicAttributesForm,
    PanelForm,
    PhotogrammetryLogEntryForm,
    RockArtAttributesForm,
    RockArtConditionForm,
    RockArtInfoForm,
    RockArtNoteForm,
    SiteForm,
    ZoomorphInventoryForm,
)
from .models import (
    AnthropomorphInventory,
    EnigmaticInventory,
    GeneralIconographicAttributes,
    Panel,
    PhotogrammetryLogEntry,
    RockArtAttributes,
    RockArtCondition,
    RockArtInfo,
    RockArtNote,
    Site,
    ZoomorphInventory,
)


def site_select(request):
    sites = Site.objects.all().order_by("site_number")
    form = SiteForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        site = form.save()
        return redirect("rockart-project", site.id)
    return render(
        request,
        "rockart/site_select.html",
        {"sites": sites, "form": form, "site_form": form, "site": None},
    )


def project_info(request, site_id):
    site = get_object_or_404(Site, pk=site_id)
    form = SiteForm(request.POST or None, instance=site)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("rockart-rock-art", site.id)
    return render(
        request,
        "rockart/project_info.html",
        {"form": form, "site": site, "active_tab": "project", "site_form": SiteForm()},
    )


def rock_art(request, site_id):
    site = get_object_or_404(Site, pk=site_id)
    info, _ = RockArtInfo.objects.get_or_create(site=site)
    form = RockArtInfoForm(request.POST or None, instance=info)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("rockart-panel", site.id)
    return render(
        request,
        "rockart/rock_art.html",
        {"form": form, "site": site, "active_tab": "rockart", "site_form": SiteForm()},
    )


def panel_view(request, site_id):
    site = get_object_or_404(Site, pk=site_id)
    form = PanelForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        panel = form.save(commit=False)
        panel.site = site
        panel.save()
        return redirect("rockart-panel", site.id)
    panels = Panel.objects.filter(site=site).order_by("panel_number")
    return render(
        request,
        "rockart/panel.html",
        {
            "form": form,
            "panels": panels,
            "site": site,
            "active_tab": "panel",
            "site_form": SiteForm(),
        },
    )


def conditions_view(request, site_id):
    site = get_object_or_404(Site, pk=site_id)
    condition, _ = RockArtCondition.objects.get_or_create(site=site)
    form = RockArtConditionForm(request.POST or None, instance=condition)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("rockart-attributes", site.id)
    return render(
        request,
        "rockart/condition.html",
        {
            "form": form,
            "site": site,
            "active_tab": "conditions",
            "site_form": SiteForm(),
        },
    )


def attributes_view(request, site_id):
    site = get_object_or_404(Site, pk=site_id)
    attrs, _ = RockArtAttributes.objects.get_or_create(site=site)
    form = RockArtAttributesForm(request.POST or None, instance=attrs)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("rockart-inventory-anthro", site.id)
    return render(
        request,
        "rockart/attributes.html",
        {
            "form": form,
            "site": site,
            "active_tab": "attributes",
            "site_form": SiteForm(),
        },
    )


def inventory_anthro_view(request, site_id):
    site = get_object_or_404(Site, pk=site_id)
    inv, _ = AnthropomorphInventory.objects.get_or_create(site=site)
    form = AnthropomorphInventoryForm(request.POST or None, instance=inv)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("rockart-inventory-continued", site.id)
    return render(
        request,
        "rockart/inventory_anthro.html",
        {
            "form": form,
            "site": site,
            "active_tab": "inv-anthro",
            "site_form": SiteForm(),
        },
    )


def inventory_continued_view(request, site_id):
    site = get_object_or_404(Site, pk=site_id)
    enigmatic, _ = EnigmaticInventory.objects.get_or_create(site=site)
    zoomorph, _ = ZoomorphInventory.objects.get_or_create(site=site)
    general, _ = GeneralIconographicAttributes.objects.get_or_create(site=site)

    if request.method == "POST":
        enigmatic_form = EnigmaticInventoryForm(request.POST, instance=enigmatic)
        zoomorph_form = ZoomorphInventoryForm(request.POST, instance=zoomorph)
        general_form = GeneralIconographicAttributesForm(request.POST, instance=general)
        if (
            enigmatic_form.is_valid()
            and zoomorph_form.is_valid()
            and general_form.is_valid()
        ):
            enigmatic_form.save()
            zoomorph_form.save()
            general_form.save()
            return redirect("rockart-photogrammetry", site.id)
    else:
        enigmatic_form = EnigmaticInventoryForm(instance=enigmatic)
        zoomorph_form = ZoomorphInventoryForm(instance=zoomorph)
        general_form = GeneralIconographicAttributesForm(instance=general)

    return render(
        request,
        "rockart/inventory_continued.html",
        {
            "enigmatic_form": enigmatic_form,
            "zoomorph_form": zoomorph_form,
            "general_form": general_form,
            "site": site,
            "active_tab": "inv-continued",
            "site_form": SiteForm(),
        },
    )


def photogrammetry_view(request, site_id):
    site = get_object_or_404(Site, pk=site_id)
    form = PhotogrammetryLogEntryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        entry = form.save(commit=False)
        entry.site = site
        entry.save()
        return redirect("rockart-photogrammetry", site.id)
    entries = PhotogrammetryLogEntry.objects.filter(site=site).order_by("date")
    return render(
        request,
        "rockart/photogrammetry.html",
        {
            "form": form,
            "entries": entries,
            "site": site,
            "active_tab": "photo",
            "site_form": SiteForm(),
        },
    )


def notes_view(request, site_id):
    site = get_object_or_404(Site, pk=site_id)
    form = RockArtNoteForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        note = form.save(commit=False)
        note.site = site
        note.save()
        return redirect("rockart-notes", site.id)
    notes = RockArtNote.objects.filter(site=site).order_by("date", "created_at")
    return render(
        request,
        "rockart/notes.html",
        {
            "form": form,
            "notes": notes,
            "site": site,
            "active_tab": "notes",
            "site_form": SiteForm(),
        },
    )
