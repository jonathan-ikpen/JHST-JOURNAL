from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Article

class LatestArticlesFeed(Feed):
    title = "JHST Latest Articles"
    link = "/rss/"
    description = "Updates on new published articles from the Journal of Hydrocarbon Science and Technology."

    def items(self):
        return Article.objects.order_by('-issue__publication_date')[:10]

    def item_title(self, item):
        return item.manuscript.title

    def item_description(self, item):
        return item.manuscript.abstract

    def item_link(self, item):
        return reverse('article_detail', args=[item.pk])
