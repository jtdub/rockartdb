from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import resolve, reverse
from rest_framework.test import APIClient

from rockart import forms, models
from rockart.api import serializers


class ModelTests(TestCase):
    def test_site_str(self):
        site = models.Site.objects.create(site_number="ABC-123")
        self.assertEqual(str(site), "ABC-123")

    def test_related_models_str(self):
        art_type = models.RockArtType.objects.create(name="Pictograph")
        art_category = models.RockArtCategory.objects.create(name="Historic")
        self.assertEqual(str(art_type), "Pictograph")
        self.assertEqual(str(art_category), "Historic")

    def test_panel_unique_together(self):
        site = models.Site.objects.create(site_number="P-1")
        models.Panel.objects.create(site=site, panel_number=1)
        with self.assertRaises(Exception):
            models.Panel.objects.create(site=site, panel_number=1)


class FormTests(TestCase):
    def test_forms_use_bootstrap_class(self):
        form = forms.SiteForm()
        self.assertIn(
            "form-control", form.fields["site_number"].widget.attrs.get("class", "")
        )

    def test_site_form_valid(self):
        form = forms.SiteForm(data={"site_number": "X-1"})
        self.assertTrue(form.is_valid())


class SerializerTests(TestCase):
    def test_site_serializer(self):
        data = {"site_number": "S-100"}
        serializer = serializers.SiteSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        instance = serializer.save()
        self.assertEqual(instance.site_number, "S-100")


class ViewTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="viewer", email="viewer@example.com", password="pass123"
        )
        self.staff = User.objects.create_user(
            username="editor",
            email="editor@example.com",
            password="pass123",
            is_staff=True,
        )
        self.client = Client()
        self.client.force_login(self.user)
        self.staff_client = Client()
        self.staff_client.force_login(self.staff)

    def test_home_lists_sites_and_allows_creation(self):
        url = reverse("rockart-home")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "rockart/site_select.html")
        create_resp = self.staff_client.post(
            reverse("rockart-create"), {"site_number": "NEW-1"}
        )
        self.assertEqual(create_resp.status_code, 302)
        self.assertTrue(models.Site.objects.filter(site_number="NEW-1").exists())

    def test_section_view_loads(self):
        site = models.Site.objects.create(site_number="SITE-1")
        resp = self.client.get(reverse("rockart-project", args=[site.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Project")


class APITests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="apiuser", email="api@example.com", password="pass123"
        )
        self.staff = User.objects.create_user(
            username="apistaff",
            email="apistaff@example.com",
            password="pass123",
            is_staff=True,
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.staff_client = APIClient()
        self.staff_client.force_authenticate(self.staff)
        self.site = models.Site.objects.create(site_number="API-1")

    def test_site_list(self):
        resp = self.client.get(reverse("site-list"))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()[0]["site_number"], "API-1")

    def test_create_note(self):
        payload = {
            "site": self.site.id,
            "text": "Test note",
            "note_type": models.NoteType.SITE_NARRATIVE,
            "category": models.NoteCategory.FIELD,
        }
        resp = self.staff_client.post(
            reverse("rockartnote-list"), payload, format="json"
        )
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(models.RockArtNote.objects.count(), 1)


class URLTests(TestCase):
    def test_urls_resolve(self):
        self.assertEqual(resolve("/").url_name, "rockart-home")
        self.assertEqual(resolve("/api/docs/").url_name, "swagger-ui")


class GraphQLTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="gqluser", email="gql@example.com", password="pass123"
        )
        self.client = Client()
        self.client.force_login(self.user)
        self.site = models.Site.objects.create(site_number="GQL-1")

    def test_sites_query(self):
        query = """
        {
            sites {
                siteNumber
            }
        }
        """
        resp = self.client.post(reverse("graphql"), data={"query": query})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()["data"]["sites"]
        self.assertEqual(data[0]["siteNumber"], "GQL-1")

    def test_rest_graphql_endpoint(self):
        query = "{ sites { siteNumber } }"
        resp = self.client.post(
            reverse("graphql-api"),
            data={"query": query},
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("data", resp.json())
