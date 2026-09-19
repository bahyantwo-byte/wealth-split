import sys

html_path = sys.argv[1]
supabase_url = sys.argv[2]
anon_key = sys.argv[3]
shortcut_url = sys.argv[4]

with open(html_path, encoding='utf-8') as f:
    content = f.read()

content = content.replace('__SUPABASE_URL__', supabase_url)
content = content.replace('__SUPABASE_ANON_KEY__', anon_key)
content = content.replace('__SHORTCUT_URL__', shortcut_url)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Injected credentials into {html_path}')
