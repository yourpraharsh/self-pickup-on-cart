# Fill @@NEWn@@ in index.html with phone-screen crops of three screens already in the old page.
import re, base64, hashlib, io, sys
from PIL import Image
old = open('/tmp/old.html', encoding='utf-8').read()
PAT = re.compile(r'data:[a-z]+/[a-z0-9.+-]+;base64,[A-Za-z0-9+/=]+')
media = {hashlib.sha1(m.encode()).hexdigest(): m for m in PAT.findall(old)}
jobs = [('58508d8a774bc96887faaa048ab5e0c226070616', 134), ('982e8f53a2453619003659a64db21e4062141b60', 136), ('0d8d50e681c00dd244d3cbe491e22c4e63375d5b', 182)]
page = open('index.html', encoding='utf-8').read()
for i, (sha, fh) in enumerate(jobs):
    im = Image.open(io.BytesIO(base64.b64decode(media[sha].split(',', 1)[1]))).convert('RGB')
    v = im.crop((0, 0, 720, 1600)); v.paste(im.crop((0, im.height - fh, 720, im.height)), (0, 1600 - fh))
    b = io.BytesIO(); v.save(b, 'WEBP', quality=86, method=5)
    page = page.replace('@@NEW%d@@' % i, 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode())
assert '@@NEW' not in page
want = sys.argv[1]
assert hashlib.sha256(PAT.sub('@@M@@', page).encode()).hexdigest() == want, 'page text differs from the build'
open('index.html', 'w', encoding='utf-8').write(page)
print('filled 3 screens; text hash ok')
