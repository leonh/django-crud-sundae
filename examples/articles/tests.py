import datetime

from django.test import TestCase, RequestFactory, override_settings
from django.urls import reverse

from sundae.views import CRUDSundaeView

from .models import Author


@override_settings(ROOT_URLCONF="articles.test_listonly_urls")
class ListOnlyViewTests(TestCase):
    """A view that excludes ``create`` (and friends) should still render.

    Regression test: ``get_context_data`` used to reverse ``<model>-create``
    unconditionally, raising ``NoReverseMatch`` on list-only views.
    """

    def setUp(self):
        self.factory = RequestFactory()
        Author.objects.create(
            name="Ada Lovelace", bio="Mathematician", dob=datetime.date(1815, 12, 10)
        )

    def test_list_renders_when_create_excluded(self):
        response = self.client.get(reverse("author-list"))
        self.assertEqual(response.status_code, 200)
        # create page is excluded → no create URL in context, button hidden
        self.assertIsNone(response.context["create_view_url"])
        self.assertIsNotNone(response.context["list_view_url"])

    def test_create_url_not_registered(self):
        from django.urls import NoReverseMatch

        with self.assertRaises(NoReverseMatch):
            reverse("author-create")


@override_settings(ROOT_URLCONF="articles.urls")
class FullCrudViewTests(TestCase):
    """Happy path: a view with all actions still exposes create + renders."""

    def setUp(self):
        Author.objects.create(
            name="Grace Hopper", bio="Compiler", dob=datetime.date(1906, 12, 9)
        )

    def test_list_renders_with_create_url(self):
        response = self.client.get(reverse("author-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["create_view_url"], reverse("author-create")
        )

    def test_list_with_bulk_actions_renders(self):
        # ArticleView registers bulk actions → bulk_update URL must resolve
        response = self.client.get(reverse("article-list"))
        self.assertEqual(response.status_code, 200)


class SafeReverseTests(TestCase):
    """Unit tests for the ``_safe_reverse`` guard."""

    def setUp(self):
        self.view = CRUDSundaeView()

    def test_returns_none_for_missing_pattern(self):
        self.assertIsNone(self.view._safe_reverse("definitely-not-a-real-url-name"))

    @override_settings(ROOT_URLCONF="articles.urls")
    def test_returns_url_for_existing_pattern(self):
        self.assertEqual(self.view._safe_reverse("author-list"), reverse("author-list"))
