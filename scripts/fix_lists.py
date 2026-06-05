import bs4

def is_header_li(li):
    # Check if the first element inside the li is a <strong> tag (ignoring whitespace)
    # Also handle if it's wrapped in a <p>
    for child in li.children:
        if isinstance(child, bs4.NavigableString):
            if child.strip():
                return False
            continue
        if child.name == 'strong':
            return True
        if child.name == 'p':
            for pchild in child.children:
                if isinstance(pchild, bs4.NavigableString):
                    if pchild.strip():
                        return False
                    continue
                if pchild.name == 'strong':
                    return True
                break
        return False
    return False

def fix_lists(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = bs4.BeautifulSoup(html, 'html.parser')
    lists = soup.find_all(['ol', 'ul'])

    for lst in lists:
        current_header_li = None
        current_sub_ul = None

        # Iterate over a copy of children so we can modify the DOM safely
        for li in lst.find_all('li', recursive=False):
            if is_header_li(li):
                current_header_li = li
                # Create a <ul> inside this li
                current_sub_ul = soup.new_tag('ul')
                li.append(current_sub_ul)
            else:
                if current_header_li is not None and current_sub_ul is not None:
                    # Move this li into the sub_ul
                    # We just detach the li and append it to the ul
                    li.extract()
                    current_sub_ul.append(li)
                else:
                    # Not preceded by a header, leave it alone
                    pass

    # For any empty <ul> created (where a header had no sub-items), remove them
    for ul in soup.find_all('ul'):
        if not ul.contents:
            ul.decompose()

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

if __name__ == '__main__':
    fix_lists('docs/Journal_Manual_Export.html')
    print("Lists fixed successfully.")
