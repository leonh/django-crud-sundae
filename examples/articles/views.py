from sundae.views import CRUDSundaeView, bulk_action
from .models import Article, Author

class AuthorView(CRUDSundaeView):
    model = Author
    lookup_field = 'pk'
    fields = ['name', 'bio', 'dob' ]
    list_fields = ['name', 'dob']
    search_fields = ['name', 'bio']
    paginate_by = 10


class ArticleView(CRUDSundaeView):
    model = Article
    lookup_field = 'pk'
    fields = ['title', 'content', 'status', 'author']
    list_fields = ['title', 'status', 'created_at']
    search_fields = ['title', 'content', 'author__name']
    filterset_fields = ['status']
    paginate_by = 10

    @bulk_action(display_name="Mark as Published", confirmation_required=True)
    def publish_selected(self, request, queryset):
        queryset.update(status='published')
        return len(queryset), "published"

    @bulk_action(display_name="Mark as Draft", confirmation_required=True)
    def unpublish_selected(self, request, queryset):
        queryset.update(status='draft')
        return len(queryset), "draft"

    bulk_edit_actions = ['publish_selected','unpublish_selected']
