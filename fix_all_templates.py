import os
import re

def fix_templates():
    template_dir = 'templates/journal'
    slugs = {
        'about': 'about.html',
        'aim-scope': 'aim_scope.html',
        'editorial-team': 'editorial_team.html',
        'publication-schedule': 'publication_schedule.html',
        'publication-fees': 'publication_fees.html',
        'contact': 'contact.html',
        'publications': 'publications.html',
        'indexing': 'indexing.html',
        'metrics': 'metrics.html',
        'guidelines': 'guidelines.html',
        'author-guidelines': 'author_guidelines.html',
        'reviewer-guidelines': 'reviewer_guidelines.html',
        'ethics-malpractice': 'ethics_malpractice.html',
        'open-access-policy': 'open_access_policy.html',
        'editorial-policy': 'editorial_policy.html',
        'peer-review-policy': 'peer_review_policy.html',
        'archiving-policy': 'archiving_policy.html',
        'subscription-advertising': 'subscription_advertising.html',
        'plagiarism-policy': 'plagiarism_policy.html',
        'policies': 'policies.html',
        'jhst-journals': 'jhst_journals.html',
    }

    template_template = """{{% extends 'base.html' %}} 
{{% load static %}}
{{% block content %}}
<section class="max-w-5xl mx-auto space-y-8">
    <div class="bg-card-light dark:bg-card-dark p-8 rounded">
        <h1 class="text-3xl font-display font-bold text-primary mb-6 border-b border-border-light dark:border-border-dark pb-2">
            {title}
        </h1>
        <div class="prose dark:prose-invert max-w-none text-gray-800 dark:text-gray-200">
            {{{{ page.sections_dict.main_content.text_content|safe }}}}
        </div>
    </div>
</section>
{{% endblock %}}
"""

    for slug, filename in slugs.items():
        filepath = os.path.join(template_dir, filename)
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract title from existing H1
        title_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL | re.IGNORECASE)
        if title_match:
            title = title_match.group(1).strip()
        else:
            title = slug.replace('-', ' ').title()
            
        new_content = template_template.format(title=title)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print(f"Fixed {filename}")

if __name__ == "__main__":
    fix_templates()
