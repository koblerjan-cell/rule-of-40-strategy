import markdown, re
md = open('README.md', encoding='utf-8').read()
m = markdown.Markdown(extensions=['tables', 'toc', 'sane_lists'], extension_configs={'toc': {'permalink': False}})
body = m.convert(md)
# split intro (before first h2) and sections
parts = re.split(r'(?=<h2 id=)', body)
intro, sections = parts[0], parts[1:]
nav, out = [], []
for s in sections:
    mm = re.match(r'<h2 id="([^"]+)">(.*?)</h2>', s)
    sid, title = mm.group(1), mm.group(2)
    num = re.match(r'(\d+)\.\s*(.*)', title)
    label = num.group(2) if num else title
    n = num.group(1).zfill(2) if num else ''
    nav.append(f'<a href="#{sid}"><span>{n}</span>{label}</a>')
    s = s.replace(mm.group(0), f'<h2 id="{sid}"><span class="num">{n}</span>{label}</h2>', 1)
    out.append(f'<section>{s}</section>')
# intro: pull title, status blockquote
intro = re.sub(r'<h1[^>]*>.*?</h1>', '', intro, count=1, flags=re.S)
intro = intro.replace('<hr />', '')
html = open('template.html', encoding='utf-8').read()
html = html.replace('{{NAV}}', '\n'.join(nav)).replace('{{INTRO}}', intro).replace('{{BODY}}', '\n'.join(out))
open('index.html', 'w', encoding='utf-8').write(html)
print(len(sections), 'sections')
