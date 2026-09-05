from pathlib import Path
from io import BytesIO
from xml.sax.saxutils import escape
import json, math, subprocess
from PIL import Image, ImageOps
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader
from book_content import BOOKS,SOURCES

R=Path(__file__).resolve().parents[1]
OUT=R/'entrega'/'pdfs';OUT.mkdir(parents=True,exist_ok=True)
QA=R/'outputs'/'pdf-qa';QA.mkdir(parents=True,exist_ok=True)
W,H=500,700; M=39; CW=W-M*2
GREEN=HexColor('#1F4D36');INK=HexColor('#213C2D');CREAM=HexColor('#F7F4EA');PALE=HexColor('#E9F0E2');MUTED=HexColor('#53695A');LINE=HexColor('#CFDCCB')
for name,file in [('Body','segoeui.ttf'),('Bold','segoeuib.ttf'),('Italic','segoeuii.ttf')]:pdfmetrics.registerFont(TTFont(name,'C:/Windows/Fonts/'+file))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Italic',boldItalic='Bold')
styles={
 'body':ParagraphStyle('body',fontName='Body',fontSize=11.6,leading=16.8,textColor=INK,spaceAfter=9),
 'small':ParagraphStyle('small',fontName='Body',fontSize=9.2,leading=13,textColor=MUTED),
 'title':ParagraphStyle('title',fontName='Bold',fontSize=25,leading=29,textColor=GREEN),
 'tip':ParagraphStyle('tip',fontName='Body',fontSize=10,leading=14,textColor=GREEN),
 'cell':ParagraphStyle('cell',fontName='Body',fontSize=10,leading=14,textColor=INK),
 'ref':ParagraphStyle('ref',fontName='Body',fontSize=9.5,leading=14,textColor=INK),
}
metrics=[]
def para(c,text,y,style='body',x=M,width=CW):
 p=Paragraph(text,styles[style]);_,h=p.wrap(width,H);p.drawOn(c,x,y-h);return y-h
def photo(c,name,x,y,w,h):
 with Image.open(R/'imagens'/name) as im:
  im=ImageOps.fit(im.convert('RGB'),(int(w*2),int(h*2)),method=Image.Resampling.LANCZOS)
  encoded=BytesIO();im.save(encoded,format='JPEG',quality=86,optimize=True);encoded.seek(0)
  c.drawImage(ImageReader(encoded),x,y,w,h)
def footer(c,book,n):
 c.setStrokeColor(LINE);c.line(M,39,W-M,39)
 c.setFont('Body',8);c.setFillColor(MUTED);c.drawString(M,24,'HORTA INFINITA  /  '+book['title']);c.drawRightString(W-M,24,f'{n:02d}')
def header(c,book,n,kicker):
 c.setFillColor(CREAM);c.rect(0,0,W,H,fill=1,stroke=0)
 c.setFont('Bold',9);c.setFillColor(GREEN);c.drawString(M,H-33,'HORTA INFINITA')
 c.setFont('Body',8);c.drawRightString(W-M,H-33,'GUIAS DE CULTIVO')
 c.setStrokeColor(LINE);c.line(M,H-44,W-M,H-44)
 c.setFillColor(MUTED);c.setFont('Bold',8.5);c.drawString(M,H-68,kicker)
 footer(c,book,n)
def cover(c,b):
 c.setFillColor(CREAM);c.rect(0,0,W,H,fill=1,stroke=0)
 photo(c,b['cover'],0,0,W,355)
 c.setFillColor(GREEN);c.rect(0,345,W,13,fill=1,stroke=0)
 c.setFillColor(GREEN);c.setFont('Bold',12);c.drawString(M,650,'HORTA INFINITA')
 c.setFillColor(MUTED);c.setFont('Bold',8.8);c.drawString(M,620,b['tag'])
 st=ParagraphStyle('cover',fontName='Bold',fontSize=39,leading=43,textColor=GREEN)
 p=Paragraph(escape(b['title']),st);_,h=p.wrap(CW,200);p.drawOn(c,M,590-h)
 y=570-h;y=para(c,escape(b['subtitle']),y,'body')
 c.setFillColor(MUTED);c.setFont('Body',9);c.drawString(M,379,'EDIÇÃO 2026  ·  MATERIAL DIGITAL EM PDF')
 c.showPage()
def draw_table(c,rows,y):
 cols=len(rows[0]);cw=[CW/cols]*cols
 if cols==2:cw=[CW*.35,CW*.65]
 data=[]
 for ri,row in enumerate(rows):
  data.append([Paragraph(('<b>'+escape(str(s))+'</b>') if ri==0 else escape(str(s)),styles['cell']) for s in row])
 table=Table(data,colWidths=cw,hAlign='LEFT')
 table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),PALE),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),9),('LINEBELOW',(0,0),(-1,0),.7,LINE),('LINEBELOW',(0,1),(-1,-1),.4,LINE),('ROWBACKGROUNDS',(0,1),(-1,-1),[white,HexColor('#F1F5EC')])]))
 _,h=table.wrap(CW,H);table.drawOn(c,M,y-h);return y-h-14
def diagram(c,kind,y):
 # Diagramas didáticos simples; desenhos vetoriais explicam conceitos.
 height=92
 if kind=='light':
  labels=[('MANHÃ','Observe'),('MEIO-DIA','Registre'),('TARDE','Compare')]
 elif kind=='water':labels=[('TOQUE','Confira umidade'),('DECIDA','Observe a planta'),('REGISTRE','Acompanhe')]
 elif kind=='drain':labels=[('RECIPIENTE','Furos livres'),('SUBSTRATO','Estrutura porosa'),('REGA','Excesso escoa')]
 else:labels=[('LUZ','Energia'),('SOLUÇÃO','Água e nutrientes'),('RAÍZES','Oxigênio')]
 gap=10;bw=(CW-2*gap)/3
 for i,(a,b) in enumerate(labels):
  x=M+i*(bw+gap);c.setFillColor(PALE);c.roundRect(x,y-height+10,bw,height-10,10,fill=1,stroke=0)
  c.setFillColor(GREEN);c.setFont('Bold',9);c.drawCentredString(x+bw/2,y-28,a);c.setFont('Body',8.2);c.drawCentredString(x+bw/2,y-47,b)
 return y-height-10
def content_page(c,b,p,num):
 header(c,b,num,p['kicker'])
 y=para(c,escape(p['title']),H-85,'title')-17
 if p['image']:
  photo(c,p['image'],M,y-126,CW,126);y-=141
 for s in p['paras']:y=para(c,escape(s),y)-9
 if p['diagram']:y=diagram(c,p['diagram'],y)
 for i,s in enumerate(p['steps'],1):
  c.setFillColor(GREEN);c.setFont('Bold',9.5);c.drawString(M,y-12,f'{i:02d}')
  y=para(c,escape(s),y,'body',M+28,CW-28)-8
 if p['table']:y=draw_table(c,p['table'],y)
 for label in p['fields']:
  y=para(c,escape(label),y,'small')-17
  c.setStrokeColor(LINE);c.line(M,y,W-M,y);y-=18
 if p['tip']:
  pp=Paragraph('<b>NA PRÁTICA</b><br/>'+escape(p['tip']),styles['tip']);_,hh=pp.wrap(CW-26,H)
  c.setFillColor(PALE);c.roundRect(M,y-hh-23,CW,hh+18,8,fill=1,stroke=0);pp.drawOn(c,M+13,y-hh-12);y-=hh+33
 if p['refs']:y=para(c,'Referências: '+', '.join(p['refs'])+'. Consulte os links ao final.',y,'small')-5
 assert y>=50, f"OVERFLOW {b['slug']} p{num} {p['title']}: y={y:.1f}"
 metrics.append({'book':b['slug'],'page':num,'title':p['title'],'last_y':round(y,2)})
 c.showPage()
def toc(c,b,refs_pages):
 header(c,b,2,'SUMÁRIO')
 y=para(c,'Seu caminho de leitura.',H-85,'title')-22
 for i,p in enumerate(b['pages'],3):
  y=para(c,escape(p['title']),y,'small',M,CW-32)-6
  c.setFillColor(GREEN);c.setFont('Bold',9);c.drawRightString(W-M,y+6,str(i))
  c.setStrokeColor(LINE);c.line(M,y,W-M,y);y-=11
 y=para(c,'Referências e notas editoriais',y,'small')-6
 c.setFont('Bold',9);c.setFillColor(GREEN);c.drawRightString(W-M,y+6,str(3+len(b['pages'])))
 assert y>50,(b['slug'],'toc overflow',y)
 c.showPage()
def refpage(c,b,items,num,last):
 header(c,b,num,'REFERÊNCIAS E NOTAS')
 y=para(c,'Para consultar e aprofundar.',H-85,'title')-18
 for key in items:
  title,url=SOURCES[key]
  y=para(c,f'<b>{key} · {escape(title)}</b>',y,'ref')-3
  y=para(c,f'<link href="{escape(url)}" color="#346B45"><u>Abrir fonte original</u></link>',y,'small')-15
 if last:
  y=para(c,'<b>Sobre esta edição</b><br/>Texto editorial original, com referências públicas consultadas em setembro de 2026. Fotos de ambientação e mockups são ilustrativos; diagramas e formulários são materiais didáticos. As instituições citadas não participaram da criação e não endossam esta publicação.',y,'small')-12
  y=para(c,'As fontes estrangeiras são usadas para princípios de cultivo. Meses, cultivares e práticas específicas de outras regiões não devem ser transferidos automaticamente para o Brasil. Para manejo local, consulte assistência técnica da sua região.',y,'small')-12
  y=para(c,'© 2026 Horta Infinita. Material para uso pessoal. Reprodução e impressão para consulta própria permitidas; redistribuição comercial não autorizada.',y,'small')
 assert y>50,(b['slug'],'reference overflow',y)
 c.showPage()

manifest=[]
for b in BOOKS:
 used=list(dict.fromkeys(k for p in b['pages'] for k in p['refs']))
 chunks=[used[i:i+7] for i in range(0,len(used),7)] or [[]]
 path=OUT/(b['slug']+'.pdf')
 c=canvas.Canvas(str(path),pagesize=(W,H),pageCompression=1)
 c.setTitle('Horta Infinita | '+b['title']);c.setAuthor('Horta Infinita');c.setSubject(b['subtitle'])
 cover(c,b);toc(c,b,len(chunks))
 for n,p in enumerate(b['pages'],3):content_page(c,b,p,n)
 for i,chunk in enumerate(chunks):refpage(c,b,chunk,3+len(b['pages'])+i,i==len(chunks)-1)
 c.save()
 reader=PdfReader(path)
 assert len(reader.pages)==2+len(b['pages'])+len(chunks)
 for n,p in enumerate(reader.pages,1):
  txt=p.extract_text();assert txt and len(txt)>30,(path,n,'empty')
  assert '\ufffd' not in txt and '\u25a0' not in txt,(path,n,'bad glyph')
 manifest.append({'file':path.name,'title':b['title'],'pages':len(reader.pages),'bytes':path.stat().st_size,'sources':used})
 print(path.name,len(reader.pages),'páginas')
(R/'outputs/pdf-manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8')
(QA/'layout-bounds.json').write_text(json.dumps(metrics,indent=2,ensure_ascii=False),encoding='utf-8')
print('TOTAL',sum(x['pages'] for x in manifest))
