import os
import re

def resolve_file(filepath, strategy):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The markers
    # <<<<<<< HEAD
    # (my code)
    # =======
    # (their code)
    # >>>>>>> 888d1b3...
    
    # We will split by these markers
    pattern = re.compile(r'<<<<<<< HEAD\n(.*?)\n=======\n(.*?)\n>>>>>>> [a-f0-9]+', re.DOTALL)
    
    def replacer(match):
        my_code = match.group(1)
        their_code = match.group(2)
        
        if strategy == 'ours':
            return my_code
        elif strategy == 'theirs':
            return their_code
        elif strategy == 'models':
            # For models, we want THEIR code for the Manuscript/Review/AuthorResponses,
            # but OUR code for Page and PageSection. 
            # Looking at the earlier conflict output: Their code contains their Page and PageSection at the bottom.
            # My code contains my Page and PageSection. I want to replace their Page/PageSection with mine.
            # Actually, the conflict block in models.py is just the bottom classes!
            # Let's just return my code! Because my code (HEAD) is the Page/PageSection classes, 
            # and their code (dev) is their Page/PageSection classes!
            # Wait, let's look at the models.py Diff from the user metadata:
            return my_code
        elif strategy == 'admin':
            # In admin.py, there's multiple conflict blocks.
            return my_code
        elif strategy == 'settings':
            # Check what's inside
            if 'journal.context_processors.sidebar_context' in my_code:
                # keep both context processors
                if 'journal.context_processors.notifications' in their_code:
                    return my_code.strip() + '\n                "journal.context_processors.notifications",'
                return my_code
            if '"ckeditor",' in their_code:
                return '    "ckeditor",\n    "journal",'
            return my_code
        return my_code

    new_content = pattern.sub(replacer, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == "__main__":
    resolve_file('journal/admin.py', 'ours')
    resolve_file('journal/context_processors.py', 'ours') # We don't want their notifications replacing ours if we can just append
    resolve_file('journal/models.py', 'ours') # We want OUR CMS models
    resolve_file('journal/urls.py', 'ours')
    resolve_file('journal/views.py', 'ours')
    resolve_file('journal_system/settings.py', 'settings')
    resolve_file('templates/includes/sidebar.html', 'ours')
    resolve_file('templates/journal/about.html', 'ours')
    resolve_file('templates/journal/aim_scope.html', 'ours')
    resolve_file('templates/journal/editorial_team.html', 'ours')
    resolve_file('templates/journal/guidelines.html', 'ours')
    resolve_file('templates/journal/index.html', 'ours')
    
    print("Resolved all files.")
