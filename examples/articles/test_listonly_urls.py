"""Test URLconf: an Author view that exposes ONLY the list action.

Used by ``ListOnlyViewTests`` to reproduce the NoReverseMatch that occurred
when ``create`` was removed via ``excluded_actions`` — the list page reverses
``<model>-create`` for its "Create" button.
"""
from sundae.views import CRUDSundaeView
from .models import Author


class AuthorListOnlyView(CRUDSundaeView):
    model = Author
    lookup_field = "pk"
    fields = ["name", "bio", "dob"]
    list_fields = ["name", "dob"]
    paginate_by = 10
    list_item_actions = []
    excluded_actions = ["create", "detail", "update", "delete", "bulk_update"]


urlpatterns = AuthorListOnlyView.get_urls()
