from pathlib import Path
import sys, subprocess, wave, json, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'.tools'))
import imageio_ffmpeg
FF=imageio_ffmpeg.get_ffmpeg_exe()
W,H,FPS,SR=1280,720,24,24000
font=lambda n,b=False:ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf' if b else 'C:/Windows/Fonts/segoeui.ttf',n)
scenes=[
 ('horta-infinita-colheita-cena.webp','Seu próximo tempero\npode vir do seu vaso.','O prazer de colher começa com o primeiro cuidado.'),
 ('manjericao-vaso.webp','Um vaso.\nUm começo possível.','Luz adequada · Planta compatível · Atenção diária'),
 ('horta-infinita-guia-mockup.webp','Um guia por perto.\nUma dúvida a menos.','PDFs sobre plantio, rega e cuidados'),
 ('horta-infinita-bonus-mockup.webp','Comece pequeno.\nAvance no seu ritmo.','Escolha o conteúdo para a sua etapa.'),
 ('horta-infinita-colheita-cena.webp','Sua horta começa\ncom uma escolha.','Planos a partir de R$ 7,90 · Pagamento único')]
clips=[]; timing=[]; elapsed=0
for i,scene in enumerate(scenes):
 with wave.open(str(R/f'video/voz-{i}.wav'),'rb') as f:
  rate=f.getframerate(); channels=f.getnchannels(); assert f.getsampwidth()==2
  a=np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').astype(np.float32)/32768
  if channels>1:a=a.reshape(-1,channels).mean(axis=1)
  if rate!=SR:a=np.interp(np.arange(int(len(a)*SR/rate))*rate/SR,np.arange(len(a)),a)
  dur=max(5.0, len(a)/SR+1.05)
  samples=int(math.ceil(dur*FPS)/FPS*SR)
  b=np.zeros(samples,dtype=np.float32); start=int(.35*SR); b[start:start+len(a)]=a
  clips.append(b); timing.append((elapsed,elapsed+samples/SR));elapsed+=samples/SR
audio=np.concatenate(clips)
# Trilha original discreta, sintetizada localmente; nenhuma música de terceiros.
t=np.arange(len(audio))/SR; pad=np.zeros_like(t)
chords=[(130.81,164.81,196),(110,130.81,164.81),(87.31,110,130.81),(98,123.47,146.83)]
for k in range(int(elapsed/4)+1):
 start=k*4; mask=(t>=start)&(t<start+5.5); tt=t[mask]-start
 env=np.minimum(tt/.8,1)*np.clip((5.5-tt)/1.5,0,1)
 for freq in chords[k%4]:pad[mask]+=np.sin(2*np.pi*freq*tt)*env*.0032
audio=np.clip(audio*.91+pad,-.98,.98)
wav=R/'video/narracao-trilha.wav'
with wave.open(str(wav),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(SR);f.writeframes((audio*32767).astype('<i2').tobytes())
out=R/'video/horta-infinita-gancho.mp4'
args=[FF,'-y','-f','rawvideo','-vcodec','rawvideo','-s',f'{W}x{H}','-pix_fmt','rgb24','-r',str(FPS),'-i','-','-i',str(wav),'-c:v','libx264','-preset','fast','-crf','23','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart','-shortest',str(out)]
log=open(R/'outputs/video-render.log','w')
proc=subprocess.Popen(args,stdin=subprocess.PIPE,stderr=log)
photos=[ImageOps.fit(Image.open(R/'imagens'/s[0]).convert('RGB'),(W+160,H+90),method=Image.Resampling.LANCZOS) for s in scenes]
def frame(i,progress):
 photo=photos[i]; zoom=1+.045*progress
 ww,hh=int(W/zoom),int(H/zoom)
 cx=photo.width/2+22*math.sin(progress*math.pi); cy=photo.height/2
 im=photo.crop((int(cx-ww/2),int(cy-hh/2),int(cx+ww/2),int(cy+hh/2))).resize((W,H),Image.Resampling.BICUBIC).convert('RGBA')
 shade=np.zeros((H,W,4),np.uint8); shade[:,:,0:3]=(10,28,18)
 base=np.linspace(215,18,W) if i in (0,1,4) else np.full(W,85)
 shade[:,:,3]=base[None,:]; im=Image.alpha_composite(im,Image.fromarray(shade))
 d=ImageDraw.Draw(im)
 d.rounded_rectangle((62,46,303,87),20,fill=(239,245,222,240));d.text((80,53),'HORTA INFINITA',font=font(23,True),fill='#1F4D36')
 if i in (2,3):
  # Os dispositivos ficam na parte superior; tarja inferior evita cobrir as capas.
  d.rectangle((0,445,W,H),fill=(16,44,29,244)); y=460; size=47
 else:y=225;size=61
 for line in scenes[i][1].split('\n'):
  d.text((62,y),line,font=font(size,True),fill='#FFF9EA');y+=size+9
 d.text((64,630),scenes[i][2],font=font(29),fill='#E0EDD4')
 if i==4:d.rounded_rectangle((65,430,570,501),14,fill='#DCEBD7');d.text((89,443),'ESCOLHA SEU GUIA',font=font(33,True),fill='#1F4D36')
 d.rectangle((0,H-5,int(W*(timing[i][0]+progress*(timing[i][1]-timing[i][0]))/elapsed),H),fill='#DCEBD7')
 return im.convert('RGB')
for i,(start,end) in enumerate(timing):
 frames=round((end-start)*FPS)
 for n in range(frames):
  im=frame(i,n/max(1,frames-1))
  if n<6 and i>0:im=Image.blend(frame(i-1,1),im,(n+1)/6)
  proc.stdin.write(im.tobytes())
  if n==frames//2:im.save(R/f'outputs/video-cena-{i+1}.jpg',quality=92)
proc.stdin.close();code=proc.wait();log.close();assert code==0
poster=frame(0,.3);poster.save(R/'imagens/video-poster.webp',quality=85,method=6)
# Verificação de decodificação de todo vídeo, incluindo faixa de áudio.
v=subprocess.run([FF,'-v','error','-i',str(out),'-f','null','-'],capture_output=True,text=True)
assert v.returncode==0 and not v.stderr.strip(),v.stderr
manifest={'seconds':round(elapsed,2),'resolution':[W,H],'fps':FPS,'bytes':out.stat().st_size,'audio':'Narração sintetizada pt-BR (Microsoft Maria Desktop), trilha original sintetizada','visual':'Imagens estáticas com movimento, transições e textos; não é filmagem real.','timing':timing}
(R/'outputs/video-info.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(manifest,ensure_ascii=False))
