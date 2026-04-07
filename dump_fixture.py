import os
import subprocess

def dump_fixture():
    # Make sure fixtures directory exists
    os.makedirs('journal/fixtures', exist_ok=True)
    
    # Run dumpdata and capture stdout as binary
    result = subprocess.run(
        ['python', 'manage.py', 'dumpdata', 'journal.Page', 'journal.PageSection', '--indent', '4'], 
        capture_output=True,
        check=True
    )
    
    # Decode as UTF-8 and save safely
    data = result.stdout.decode('utf-8')
    with open('journal/fixtures/cms_initial_data.json', 'w', encoding='utf-8') as f:
        f.write(data)
        
    print("Successfully dumped journal.Page and journal.PageSection to journal/fixtures/cms_initial_data.json with UTF-8 encoding!")

if __name__ == '__main__':
    dump_fixture()
