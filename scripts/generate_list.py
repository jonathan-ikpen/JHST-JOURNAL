import re

md_path = r"c:\jojo\school\jhst-journal\users\Reviewers_Editorial_Board_Members-v2.md"
with open(md_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Parse Editorial Team
ed_table_match = re.search(r'## List of Editorial Team Members\n\n\|.*?\|\n\|.*?\|\n(.*?)\n\n## Profile', text, re.DOTALL)
ed_rows = ed_table_match.group(1).strip().split('\n')
ed_members = []
for row in ed_rows:
    cols = [c.strip() for c in row.split('|')][1:-1]
    name, affil, spec, email = cols[1], cols[2], cols[3], cols[4]
    ed_members.append({'name': name, 'affil': affil, 'spec': spec, 'email': email})

# Parse Advisory Board
adv_table_match = re.search(r'## Journal Advisory Board Members\n\n\|.*?\|\n\|.*?\|\n(.*?)\n\n###', text, re.DOTALL)
adv_rows = adv_table_match.group(1).strip().split('\n')
adv_members = []
for row in adv_rows:
    cols = [c.strip() for c in row.split('|')][1:-1]
    name, affil, spec, email = cols[1], cols[2], cols[3], cols[4]
    adv_members.append({'name': name, 'affil': affil, 'spec': spec, 'email': email})

# Parse Bios
bios = {}
bio_matches = re.finditer(r'### (.*?)\n\n(?:!\[.*?\]\((.*?)\)\n\n)?(.*?)(?=\n\n### |\n\n## |$)', text, re.DOTALL)
for m in bio_matches:
    name = m.group(1).strip()
    bio_text = m.group(3).strip()
    bios[name] = bio_text

# Generate code
out = []
out.append("        members = [")
out.append("            {")
out.append("                'name': 'Dr. Fredrick B. Owoyemi',")
out.append("                'role_type': 'editor_in_chief',")
out.append("                'affiliation': 'Petroleum Training Institute, Effurun, Nigeria',")
out.append("                'bio': 'Dr. Fredrick B. Owoyemi serves as the Editor-in-Chief of the Journal of Hydrocarbon Science and Technology (JHST).',")
out.append("                'email': 'eic@jhst.org',")
out.append("                'order': 1,")
out.append("            },")

order = 1
for m in ed_members:
    bio = m['spec']
    # Check if there is a full bio
    for b_name in bios:
        if m['name'] in b_name or b_name in m['name'] or m['name'].replace('Prof.', '').strip() in b_name:
            bio = bios[b_name]
            break
            
    out.append("            {")
    out.append(f"                'name': {repr(m['name'])},")
    out.append("                'role_type': 'editorial_board',")
    out.append(f"                'affiliation': {repr(m['affil'])},")
    out.append(f"                'bio': {repr(bio)},")
    out.append(f"                'email': {repr(m['email'])},")
    out.append(f"                'order': {order},")
    out.append("            },")
    order += 1

order = 1
for m in adv_members:
    bio = m['spec']
    for b_name in bios:
        if m['name'] in b_name or b_name in m['name'] or m['name'].replace('Prof.', '').strip() in b_name:
            bio = bios[b_name]
            break
            
    out.append("            {")
    out.append(f"                'name': {repr(m['name'])},")
    out.append("                'role_type': 'advisory_board',")
    out.append(f"                'affiliation': {repr(m['affil'])},")
    out.append(f"                'bio': {repr(bio)},")
    out.append(f"                'email': {repr(m['email'])},")
    out.append(f"                'order': {order},")
    out.append("            },")
    order += 1

out.append("        ]")

with open(r'c:\jojo\school\jhst-journal\scratch_generate.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(out))
