import os
import base64
import re
try:
    import markdown
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "markdown"])
    import markdown

md_files = [
    'docs/01_introduction_and_workflow.md',
    'docs/02_guide_for_authors.md',
    'docs/03_guide_for_reviewers.md',
    'docs/04_guide_for_editors.md',
    'docs/05_guide_for_admins.md'
]

combined_md = ''
for f in md_files:
    if os.path.exists(f):
        # Adding a specific class or page break token
        combined_md += '<div class="page-break"></div>\n\n'
        combined_md += open(f, encoding='utf-8').read() + '\n\n'

html = markdown.markdown(combined_md)

# Function to encode image to base64
def get_b64_image(path):
    if os.path.exists(path):
        return base64.b64encode(open(path, 'rb').read()).decode()
    return ""

def repl(m):
    alt_text = m.group(1)
    img_path = m.group(2)
    full_path = os.path.join('docs', img_path)
    b64 = get_b64_image(full_path)
    if b64:
        return f'<img src="data:image/png;base64,{b64}" alt="{alt_text}" class="screenshot">'
    return m.group(0)

html = re.sub(r'<img alt="(.*?)" src="(.*?)" />', repl, html)

# Get logo
logo_b64 = get_b64_image('docs/images/jhst-logo.png')
logo_html = f'<img src="data:image/png;base64,{logo_b64}" alt="JHST Logo" style="max-width: 300px; margin: 0 auto 40px auto; display: block;">' if logo_b64 else ''

output_path = 'docs/Journal_Manual_Export.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <link href="https://fonts.googleapis.com/css2?family=Work+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Work Sans', sans-serif;
            max-width: 850px;
            margin: auto;
            padding: 60px 40px;
            line-height: 1.8;
            color: #333;
            font-size: 16px;
        }}
        .cover-page {{
            text-align: center;
            padding: 100px 0;
            border-bottom: 2px solid #eaeaea;
            margin-bottom: 60px;
        }}
        h1 {{
            font-size: 42px;
            font-weight: 700;
            color: #054D08;
            margin-bottom: 20px;
            line-height: 1.2;
        }}
        h2 {{
            font-size: 28px;
            font-weight: 600;
            color: #054D08;
            margin-top: 50px;
            margin-bottom: 24px;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 10px;
        }}
        h3 {{
            font-size: 22px;
            font-weight: 600;
            color: #054D08;
            margin-top: 40px;
            margin-bottom: 16px;
        }}
        p, li {{
            margin-bottom: 16px;
            color: #4a5568;
        }}
        li {{
            margin-bottom: 12px;
        }}
        .screenshot {{
            max-width: 100%;
            border: 1px solid #cbd5e0;
            margin: 30px 0;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            display: block;
        }}
        blockquote {{
            border-left: 4px solid #054D08;
            background-color: #eaf4ea;
            padding: 20px;
            margin: 30px 0;
            border-radius: 0 8px 8px 0;
            font-style: normal;
        }}
        blockquote p {{
            margin-bottom: 0;
            color: #054D08;
        }}
        .page-break {{
            page-break-before: always;
            margin-top: 80px;
        }}
        strong {{
            color: #054D08;
            font-weight: 600;
        }}
        hr {{
            border: 0;
            height: 1px;
            background: #e2e8f0;
            margin: 40px 0;
        }}
    </style>
</head>
<body>
    <div class="cover-page">
        {logo_html}
        <h1>Journal Management System</h1>
        <p style="font-size: 20px; color: #718096; max-width: 600px; margin: 0 auto;">Official User Manual & Workflow Documentation</p>
    </div>
    {html}
</body>
</html>''')

print(f"Successfully generated {output_path}")
