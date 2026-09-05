from pathlib import Path
import subprocess, json, re
from concurrent.futures import ThreadPoolExecutor
from PIL import Image,ImageOps,ImageDraw,ImageFont
from pypdf import PdfReader
R=Path(__file__).resolve().parents[1]
QA=R/'outputs/pdf-qa-final'
QA.mkdir(parents=True,exist_ok=True)
POP=r'C:\Users\PC GAMER\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe'
books=list((R/'entrega/pdfs').glob('*.pdf'))
def render(path):
 folder=QA/path.stem;folder.mkdir(exist_ok=True)
 p=subprocess.run([POP,'-scale-to','1100','-png',str(path),str(folder/'pagina')],capture_output=True,text=True)
 assert p.returncode==0 and not p.stderr.strip(),(path,p.stderr)
 imgs=sorted(folder.glob('pagina-*.png'));assert len(imgs)==len(PdfReader(path).pages)
 for n in range(0,len(imgs),12):
  subset=imgs[n:n+12];cols=3;rows=(len(subset)+2)//3
  sheet=Image.new('RGB',(3*280,rows*414),'#d7dfd2');d=ImageDraw.Draw(sheet)
  for j,impath in enumerate(subset):
   im=Image.open(impath).convert('RGB');im.thumbnail((266,380))
   x=(j%cols)*280+7;y=(j//cols)*414+22;sheet.paste(im,(x,y));d.text((x,y-17),f'{path.stem[:25]} / p{n+j+1}',fill='#1f4d36')
  sheet.save(QA/f'{path.stem}-contato-{n//12+1}.jpg',quality=90)
 return (path.name,len(imgs))
with ThreadPoolExecutor(max_workers=3) as pool:
 for name,count in pool.map(render,books):print(name,count,'páginas renderizadas sem alertas')
# Amostras correspondem às páginas reais de Luz (p4) e Rega (p11).
essential=QA/'01-horta-infinita-essencial'
for i,page in enumerate([4,11],1):
 candidates=list(essential.glob(f'pagina-{page:02}.png'))+list(essential.glob(f'pagina-{page}.png'))
 assert candidates,page
 with Image.open(candidates[0]) as im:
  im.resize((1000,1400),Image.Resampling.LANCZOS).save(R/f'imagens/amostra-essencial-{i}.webp',quality=91,method=6)
frames=list((R/'outputs').glob('video-cena-*.jpg'))
sheet=Image.new('RGB',(960,3*293),'#e9f0e2');d=ImageDraw.Draw(sheet)
for i,f in enumerate(sorted(frames)):
 im=Image.open(f).resize((470,264),Image.Resampling.LANCZOS)
 x=(i%2)*480;y=(i//2)*293+24;sheet.paste(im,(x,y));d.text((x+8,y-17),f'CENA {i+1}',fill='#1f4d36')
sheet.save(R/'outputs/video-contato.jpg',quality=94)
print('Amostras reais e contatos de inspeção prontos.')
