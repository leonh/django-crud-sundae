from sundae.views import CRUDSundaeView, bulk_action
from .models import Article

class ArticleView(CRUDSundaeView):
    model = Article
    lookup_field = 'pk'
    fields = ['title', 'content', 'status']
    list_fields = ['title', 'status', 'created_at']
    search_fields = ['title', 'content']
    filterset_fields = ['status']
    paginate_by = 10

    @bulk_action(display_name="Mark as Published", confirmation_required=True)
    def publish_selected(self, request, queryset):
        queryset.update(status='published')
        return len(queryset), "published"

    bulk_edit_actions = ['publish_selected']
