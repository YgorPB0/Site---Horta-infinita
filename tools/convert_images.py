from pathlib import Path
from PIL import Image, ImageOps
import json

ROOT = Path(__file__).resolve().parents[1]
report = []
for folder in ('imagens', 'depoimentos'):
    for src in sorted((ROOT / folder).iterdir()):
        if src.suffix.lower() not in ('.jpg', '.jpeg', '.png'):
            continue
        dst = src.with_suffix('.webp')
        with Image.open(src) as original:
            im = ImageOps.exif_transpose(original)
            im.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
            im = im.convert('RGBA' if 'A' in im.getbands() else 'RGB')
            im.save(dst, 'WEBP', quality=88 if folder == 'depoimentos' else 83, method=6)
        with Image.open(dst) as check:
            check.load()
            assert check.width > 0 and check.height > 0
        report.append({'original': str(src.relative_to(ROOT)), 'webp': str(dst.relative_to(ROOT)), 'before': src.stat().st_size, 'after': dst.stat().st_size})
(ROOT / 'outputs' / 'conversao-webp.json').write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps({'files': len(report), 'before': sum(r['before'] for r in report), 'after': sum(r['after'] for r in report)}, indent=2))
