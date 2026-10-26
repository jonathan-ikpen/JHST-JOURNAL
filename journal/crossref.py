"""Crossref DOI integration for JHST.

Member: Petroleum Training Institute | Prefix: 10.68763 (fixed) | Role: bcmg

Public API (as requested):
    generate_doi(article)      -> full DOI string, saved to nothing (pure)
    build_crossref_xml(article) -> Crossref deposit XML (schema 5.3.1)
    deposit_to_crossref(article) -> POSTs the deposit, returns submission/batch id
    check_deposit_status(article) -> True once the DOI resolves live

Design notes (deviations from the pasted prompt, for good reasons):
- Deposits run synchronously with a timeout but NEVER crash publishing;
  failures leave the article 'pending' for retry via the
  `deposit_pending_dois` management command. cPanel shared hosting has no
  Celery/Redis, so a cron-able command is the reliable "background job".
- There is no Crossref REST endpoint that reports deposit status by
  submission ID, so liveness is checked with https://api.crossref.org/works/.
- Credentials come from environment variables only, never templates or git.
"""

import logging
import re
from datetime import datetime

import requests
from django.conf import settings
from django.core.exceptions import ValidationError
from xml.sax.saxutils import escape

logger = logging.getLogger(__name__)

# Fixed by Crossref at membership approval. NEVER generate or change this.
CROSSREF_PREFIX = "10.68763"

DEPOSIT_URL_LIVE = "https://doi.crossref.org/servlet/deposit"
DEPOSIT_URL_TEST = "https://test.crossref.org/servlet/deposit"
WORKS_API_URL = "https://api.crossref.org/works"

JOURNAL_TITLE = "Journal of Hydrocarbon Science and Technology"
REGISTRANT = "Petroleum Training Institute"


def validate_crossref_doi(value):
    """Reject placeholder or foreign DOIs (e.g. 10.1234/...) at the model level."""
    if value and not value.startswith(CROSSREF_PREFIX + "/"):
        raise ValidationError(
            f"DOI must use the journal prefix {CROSSREF_PREFIX}/. "
            "Placeholder DOIs are not allowed."
        )


def _issn_or_none(raw):
    """Extract a bare ISSN (XXXX-XXX[X]) from a messy footer value."""
    if not raw:
        return None
    normalized = raw.replace(" ", "")
    # Legacy typo: "1595 - 431 (Online)" lost the final 5; correct it before regex
    if "1595-431" in normalized and "1595-4315" not in normalized:
        return "1595-4315"
    match = re.search(r"(\d{4}-\d{3}[\dX])", normalized)
    issn = match.group(1) if match else None
    if issn and not re.fullmatch(r"\d{4}-\d{3}[\dX]", issn):
        return None
    return issn


def generate_doi(article):
    """Build the full DOI for an article: 10.68763/jhst.{year}.v{vol}i{iss}.{id}."""
    from .models import Article  # deferred to avoid circular import

    issue = article.issue
    suffix = (
        f"jhst.{issue.publication_date.year}"
        f".v{issue.volume.number}i{issue.number}.{article.id}"
    )
    doi = f"{CROSSREF_PREFIX}/{suffix}"
    # Defensive: article ids are unique, but never save a duplicate DOI.
    counter = 2
    while Article.objects.filter(doi=doi).exclude(pk=article.pk).exists():
        doi = f"{CROSSREF_PREFIX}/{suffix}.{counter}"
        counter += 1
    return doi


def _split_name(full_name):
    full_name = (full_name or "").strip()
    if not full_name:
        return "", ""
    parts = full_name.split()
    if len(parts) == 1:
        return parts[0], ""
    return " ".join(parts[:-1]), parts[-1]


def _person_xml(full_name, affiliation, orcid=None, sequence="first"):
    given, surname = _split_name(full_name)
    orcid_xml = (
        f"<ORCID authenticated=\"true\">https://orcid.org/{escape(orcid.strip())}</ORCID>"
        if orcid and orcid.strip()
        else ""
    )
    affiliation_xml = (
        f"<affiliations><institution><institution_name>{escape(affiliation.strip())}</institution_name>"
        f"</institution></affiliations>"
        if affiliation and affiliation.strip()
        else ""
    )
    return (
        f"<person_name contributor_role=\"author\" sequence=\"{sequence}\">"
        f"<given_name>{escape(given)}</given_name>"
        f"<surname>{escape(surname) or escape(given)}</surname>"
        f"{affiliation_xml}{orcid_xml}</person_name>"
    )


def build_crossref_xml(article, site_url=None):
    """Build a Crossref 5.3.1 journal deposit for a single article."""
    manuscript = article.manuscript
    issue = article.issue
    volume = issue.volume
    site_url = site_url or getattr(settings, "CROSSREF_SITE_URL", "https://www.jhst.org").rstrip("/")
    resource_url = f"{site_url}/article/{article.id}/"
    pub_date = issue.publication_date
    now = datetime.now()

    from pages.models import SiteSettings  # journal metadata lives in the CMS

    # SingletonMixin has no get_instance(); pk=1 is the singleton row.
    try:
        site_settings = SiteSettings.objects.get(pk=1)
        issn_online = _issn_or_none(getattr(site_settings, "issn_online", ""))
        issn_print = _issn_or_none(getattr(site_settings, "issn_print", ""))
    except Exception:
        issn_online, issn_print = None, None
    # Fallback: _issn_or_none normalizes "1595 - 431" -> "1595-4315" (real ISSN per https://portal.issn.org/resource/ISSN/1595-4315)
    issn_online = issn_online or "1595-4315"

    issn_xml = ""
    if issn_online:
        issn_xml += f'<issn media_type="electronic">{issn_online}</issn>'
    if issn_print:
        issn_xml += f'<issn media_type="print">{issn_print}</issn>'

    author = manuscript.author
    author_name = author.get_full_name() or author.username
    contributors = [_person_xml(author_name, author.affiliation, getattr(author, "orcid", None))]
    for co_author in [c.strip() for c in (manuscript.co_authors or "").split(",") if c.strip()]:
        contributors.append(
            _person_xml(co_author, manuscript.affiliations, sequence="additional")
        )

    pages_xml = ""
    if article.page_start:
        pages_xml = f"<pages><first_page>{article.page_start}</first_page>"
        if article.page_end:
            pages_xml += f"<last_page>{article.page_end}</last_page>"
        pages_xml += "</pages>"

    batch_id = f"jhst-{article.id}-{now.strftime('%Y%m%d%H%M%S')}"
    timestamp = now.strftime("%Y%m%d%H%M%S") + f"{now.microsecond // 1000:03d}"
    depositor_email = getattr(settings, "CROSSREF_DEPOSITOR_EMAIL", "") or "noreply@jhst.org"

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<doi_batch version="5.3.1" xmlns="http://www.crossref.org/schema/5.3.1"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.crossref.org/schema/5.3.1 http://www.crossref.org/schema/deposit/crossref5.3.1.xsd">
  <head>
    <doi_batch_id>{batch_id}</doi_batch_id>
    <timestamp>{timestamp}</timestamp>
    <depositor>
      <depositor_name>{escape(REGISTRANT)}</depositor_name>
      <email_address>{escape(depositor_email)}</email_address>
    </depositor>
    <registrant>{escape(REGISTRANT)}</registrant>
  </head>
  <body>
    <journal>
      <journal_metadata language="en">
        <full_title>{escape(JOURNAL_TITLE)}</full_title>
        {issn_xml}
      </journal_metadata>
      <journal_issue>
        <publication_date media_type="online">
          <month>{pub_date.month:02d}</month>
          <day>{pub_date.day:02d}</day>
          <year>{pub_date.year}</year>
        </publication_date>
        <journal_volume><volume>{volume.number}</volume></journal_volume>
        <issue>{issue.number}</issue>
      </journal_issue>
      <journal_article publication_type="full_text">
        <titles><title>{escape(manuscript.title)}</title></titles>
        <contributors>{''.join(contributors)}</contributors>
        <publication_date media_type="online">
          <month>{pub_date.month:02d}</month>
          <day>{pub_date.day:02d}</day>
          <year>{pub_date.year}</year>
        </publication_date>
        {pages_xml}
        <doi_data>
          <doi>{escape(article.doi)}</doi>
          <resource>{escape(resource_url)}</resource>
        </doi_data>
      </journal_article>
    </journal>
  </body>
</doi_batch>"""


def _deposit_url():
    use_test = str(getattr(settings, "CROSSREF_USE_TEST", "True")) == "True"
    return DEPOSIT_URL_TEST if use_test else DEPOSIT_URL_LIVE


def deposit_to_crossref(article, xml_string=None):
    """POST the deposit XML; returns the submission/batch id. Raises on failure."""
    login_id = getattr(settings, "CROSSREF_LOGIN_ID", "")
    login_passwd = getattr(settings, "CROSSREF_LOGIN_PASSWORD", "")
    # Crossref members belong to a role (ours is bcmg); the deposit POST must
    # carry it or the servlet 401s with 'cannot assume specified role'.
    role = getattr(settings, "CROSSREF_ROLE", "bcmg")
    if not login_id or not login_passwd:
        raise ValueError("Crossref credentials are not configured (CROSSREF_LOGIN_ID).")

    xml_string = xml_string or build_crossref_xml(article)
    response = requests.post(
        _deposit_url(),
        data={
            "operation": "doMDUpload",
            "login_id": login_id,
            "login_passwd": login_passwd,
            "role": role,
        },
        files={"fname": ("deposit.xml", xml_string, "application/xml")},
        timeout=30,
    )
    response.raise_for_status()
    body = response.text
    logger.info("Crossref deposit response for article %s: %s", article.id, body[:2000])

    lowered = body.lower()
    if "failure" in lowered or "<msg>" in lowered and "success" not in lowered:
        # Deposit servlet reports per-record failures inside a 200 response.
        match = re.search(r"<msg[^>]*>(.*?)</msg>", body, re.IGNORECASE | re.DOTALL)
        detail = match.group(1).strip()[:500] if match else body[:500]
        raise ValueError(f"Crossref rejected the deposit: {detail}")

    match = re.search(
        r"<(?:submission_id|submissionid|batch_id|doi_batch_id)[^>]*>(.*?)</",
        body,
        re.IGNORECASE | re.DOTALL,
    )
    return match.group(1).strip() if match else f"jhst-{article.id}-{datetime.now():%Y%m%d%H%M%S}"


def check_deposit_status(article):
    """True once the DOI resolves live via api.crossref.org (DOI goes live 5-30 min after deposit)."""
    if not article.doi:
        return False
    try:
        response = requests.get(
            f"{WORKS_API_URL}/{article.doi}",
            params={"mailto": getattr(settings, "CROSSREF_DEPOSITOR_EMAIL", "noreply@jhst.org")},
            timeout=15,
        )
        return response.status_code == 200
    except requests.RequestException:
        logger.warning("DOI liveness check failed for %s", article.doi)
        return False
