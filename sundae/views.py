"""
Django CRUD Sundae Views

A collection of class-based views for CRUD operations with Tailwind CSS and HTMX support.
"""

from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)


class CRUDView:
    """
    Base mixin for CRUD views that provides common functionality.

    Following the ice-cream metaphor: this is your base sundae!
    Add your own toppings (mixins) to customize behavior.
    """

    # Override these in your subclass
    model = None
    fields = None
    template_name_suffix = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_type'] = self.__class__.__name__.lower()
        return context


class SundaeListView(CRUDView, ListView):
    """List view with HTMX and Tailwind support."""
    template_name_suffix = "_list"


class SundaeDetailView(CRUDView, DetailView):
    """Detail view with HTMX and Tailwind support."""
    template_name_suffix = "_detail"


class SundaeCreateView(CRUDView, CreateView):
    """Create view with HTMX and Tailwind support."""
    template_name_suffix = "_form"


class SundaeUpdateView(CRUDView, UpdateView):
    """Update view with HTMX and Tailwind support."""
    template_name_suffix = "_form"


class SundaeDeleteView(CRUDView, DeleteView):
    """Delete view with HTMX and Tailwind support."""
    template_name_suffix = "_confirm_delete"
