from django.core.management.base import BaseCommand
from journal.crossref import check_deposit_status, deposit_to_crossref
from journal.models import Article


class Command(BaseCommand):
    help = (
        "Retry Crossref deposits for articles that are pending/failed, "
        "and mark DOIs as registered once they resolve live. "
        "Safe to run on a schedule (e.g. cPanel cron every 30 minutes)."
    )

    def handle(self, *args, **options):
        pending = Article.objects.filter(doi_status__in=('pending', 'failed')).exclude(doi__isnull=True)
        self.stdout.write(f"Found {pending.count()} article(s) with pending/failed DOIs.")
        updated = 0
        for article in pending:
            try:
                if check_deposit_status(article):
                    # DOI already live (e.g. deposited via the Crossref admin UI).
                    article.doi_status = 'registered'
                    article.save(update_fields=['doi_status'])
                    self.stdout.write(self.style.SUCCESS(f"[{article.id}] {article.doi} is now live."))
                    updated += 1
                    continue
                if article.doi_status == 'failed' or not article.crossref_batch_id:
                    article.crossref_batch_id = deposit_to_crossref(article)
                    article.save(update_fields=['crossref_batch_id'])
                if check_deposit_status(article):
                    article.doi_status = 'registered'
                    article.save(update_fields=['doi_status'])
                    self.stdout.write(self.style.SUCCESS(f"[{article.id}] {article.doi} registered."))
                    updated += 1
                else:
                    self.stdout.write(f"[{article.id}] {article.doi} still pending — will retry next run.")
            except Exception as e:  # noqa: BLE001 — log and continue with the rest
                article.doi_status = 'failed'
                article.save(update_fields=['doi_status'])
                self.stdout.write(self.style.ERROR(f"[{article.id}] deposit failed: {e}"))
        self.stdout.write(self.style.SUCCESS(f"Done. {updated} DOI(s) newly registered."))
