from django.core.management.base import BaseCommand
from journal.models import Article


class Command(BaseCommand):
    help = (
        "Remove placeholder/fake DOIs (e.g. 10.1234/...) flagged by Crossref. "
        "Real 10.68763/ DOIs are never touched."
    )

    def handle(self, *args, **options):
        bad = Article.objects.exclude(doi__startswith="10.68763/").exclude(doi__isnull=True).exclude(doi__exact="")
        count = bad.count()
        for article in bad:
            self.stdout.write(f"Clearing {article.doi} from article {article.id}")
            article.doi = None
            article.doi_status = 'none'
            article.crossref_batch_id = None
            article.save(update_fields=["doi", "doi_status", "crossref_batch_id"])
        self.stdout.write(self.style.SUCCESS(f"Cleared {count} placeholder DOI(s)."))
