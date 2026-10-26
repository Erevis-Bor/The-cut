from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]
html=(root/'index.html').read_text(encoding='utf-8')
css=(root/'styles.css').read_text(encoding='utf-8')
html=re.sub(r'\s*<link rel="icon"[^>]+>', '', html)
html=re.sub(r'\s*<link rel="manifest"[^>]+>', '', html)
html=html.replace('<link rel="stylesheet" href="styles.css">','<style>'+css+'</style>')
bundled=[]
for name in ('data.js','metadata.js','app.js'):
    js=(root/name).read_text(encoding='utf-8').replace('</script','<\\/script')
    html=html.replace(f'<script src="{name}" defer></script>','')
    bundled.append('<script>'+js+'</script>')
html=html.replace('</body>', '\n'.join(bundled)+'\n</body>')
assert not re.search('<script src=', html)
out=root/'THE-CUT-v4-standalone.html'
out.write_text(html,encoding='utf-8')
print(out, out.stat().st_size)
