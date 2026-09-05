from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
from zipfile import ZipFile,ZIP_DEFLATED
from pypdf import PdfReader
import json,re
R=Path(__file__).resolve().parents[1]
manifest=json.loads((R/'outputs/pdf-manifest.json').read_text(encoding='utf-8'))
pdfs=[R/'entrega/pdfs'/b['file'] for b in manifest]
assert len(pdfs)==7
packages=[('Essencial',7.90,pdfs[:1]),('Plus',12.90,pdfs[:2]),('Completo',17.90,pdfs)]
dest=R/'entrega/pacotes';dest.mkdir(exist_ok=True)
summary=[]
for title,price,files in packages:
 out=dest/f'Horta-Infinita-{title}.zip'
 guide='HORTA INFINITA - '+title.upper()+'\n\nObrigado pela compra!\n\n'
 guide+='Abra os PDFs abaixo na ordem sugerida. Guarde uma cópia para consulta e imprima as páginas de planejamento se desejar.\n\n'
 for i,p in enumerate(files,1):guide+=f'{i}. {p.name}\n'
 guide+='\nOs arquivos são materiais digitais de leitura. Não incluem videoaulas, plantas, ferramentas ou dispositivos. Para dúvidas sobre acesso e pagamento, consulte os dados do seu pedido na plataforma de compra.\n\nResultados de cultivo dependem de espécie, cultivar, clima, espaço e cuidados. Consulte as referências de cada PDF. Uso pessoal; não redistribuir comercialmente.\n'
 with ZipFile(out,'w',ZIP_DEFLATED) as z:
  for p in files:z.write(p,p.name)
  z.writestr('COMECE-AQUI.txt',guide.encode('utf-8'))
 with ZipFile(out) as z:
  assert z.testzip() is None
  assert len([x for x in z.namelist() if x.endswith('.pdf')])==len(files)
 summary.append({'plan':title,'price':price,'pdfs':len(files),'pages':sum(len(PdfReader(p).pages) for p in files),'zip':out.name,'bytes':out.stat().st_size})

class SiteParser(HTMLParser):
 def __init__(self):super().__init__();self.refs=[];self.ids=[];self.checkout={};self.anchors=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  for key in ('src','poster'):
   if a.get(key):self.refs.append(a[key])
  if tag=='link' and a.get('rel')=='stylesheet':self.refs.append(a['href'])
  if tag=='a':
   href=a.get('href','')
   if href.startswith('#'):self.anchors.append(href[1:])
   elif href and not urlparse(href).scheme:self.refs.append(href)
   if 'checkout-link' in a.get('class',''):self.checkout[a['data-tier']]=href
parser=SiteParser();markup=(R/'index.html').read_text(encoding='utf-8');parser.feed(markup)
assert len(parser.ids)==len(set(parser.ids)),'IDs duplicados'
assert all(a in parser.ids for a in parser.anchors),'Âncora sem destino'
expected={'essencial':'https://pay.lowify.com.br/checkout?product_id=kjttls','plus':'https://pay.lowify.com.br/go.php?offer=laixs9z','completo':'https://pay.lowify.com.br/go.php?offer=82j9nx7'}
assert parser.checkout==expected,parser.checkout
assert not any(s in markup for s in ('17,99','pay.exemplo','[Razão Social','Depoimentos Reais','vsl-placeholder'))
sitefiles={R/'index.html',R/'styles.css',R/'script.js'}
for ref in parser.refs:
 if not urlparse(ref).scheme:
  p=R/unquote(ref.split('?')[0]);assert p.is_file(),ref;sitefiles.add(p)
assert all(p.suffix.lower()!='.pdf' for p in sitefiles),'PDF pago exposto no site'
for p in sitefiles:
 if p.suffix.lower() in ('.png','.jpg','.jpeg'):raise AssertionError('Imagem da página não convertida: '+str(p))
sitezip=R/'entrega/Site-Horta-Infinita.zip'
with ZipFile(sitezip,'w',ZIP_DEFLATED) as z:
 for p in sorted(sitefiles):z.write(p,p.relative_to(R).as_posix())
with ZipFile(sitezip) as z:assert z.testzip() is None
allzip=R/'entrega/Horta-Infinita-Entrega-Completa.zip'
with ZipFile(allzip,'w',ZIP_DEFLATED) as z:
 z.write(sitezip,'SITE-PARA-HOSPEDAR/'+sitezip.name)
 for p in dest.glob('*.zip'):z.write(p,'PACOTES-PARA-LOWIFY/'+p.name)
 for p in pdfs:z.write(p,'PDFS-INDIVIDUAIS/'+p.name)
 for name in ['horta-infinita-guia-mockup.webp','horta-infinita-bonus-mockup.webp','horta-infinita-colheita-cena.webp']:z.write(R/'imagens'/name,'MIDIA/'+name)
 z.write(R/'video/horta-infinita-gancho.mp4','MIDIA/horta-infinita-gancho.mp4')
 for name in ['GUIA-DE-ENTREGA.md','OFERTAS-E-VALIDACAO.md']:
  if (R/'entrega'/name).exists():z.write(R/'entrega'/name,name)
 z.write(R/'outputs/prompts-imagens.txt','MIDIA/prompts-imagens.txt')
with ZipFile(allzip) as z:assert z.testzip() is None
result={'packages':summary,'site_zip':sitezip.name,'site_bytes':sitezip.stat().st_size,'site_asset_count':len(sitefiles),'all_zip':allzip.name,'all_bytes':allzip.stat().st_size,'checks':['Todas as imagens referenciadas em WebP','Âncoras válidas e IDs únicos','Três checkouts correspondem aos links fornecidos','Pacotes contêm 1, 2 e 7 PDFs','ZIP do site não contém PDFs pagos','Integridade de todos os ZIPs verificada']}
(R/'outputs/delivery-manifest.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(result,indent=2,ensure_ascii=False))
