#!/usr/bin/env python3
"""Gera a cartilha E5 a partir de capturas REAIS ja aprovadas pelo verificador oficial.

Nao sintetiza pacotes: exige o dump do claro.pcap e extrai a linha
Authorization: Bearer que realmente passou pelo roteador isolado.
"""
from pathlib import Path
from html import escape
import re

from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parent
EVID = ROOT / "evidencias"
TOKEN = (ROOT / "token.txt").read_text(encoding="utf-8").strip()
RAW = (EVID / "captura-http-completa.txt").read_text(encoding="utf-8", errors="replace")
if not TOKEN or TOKEN == "GRUPO-EXEMPLO-TROQUE-ISTO":
    raise SystemExit("ERRO: token de exemplo ou vazio.")
if f"Authorization: Bearer {TOKEN}" not in RAW:
    raise SystemExit("ERRO: nao encontrei token autentico na captura HTTP.")
for name in ("claro.pcap", "cifrado.pcap"):
    if not (ROOT / name).is_file() or (ROOT / name).stat().st_size < 40:
        raise SystemExit("ERRO: pcap real nao encontrado: " + name)

# Extrai apenas linhas efetivamente presentes no dump da captura. Nao inventar bytes.
patterns = ("GET /", "Host:", "User-Agent:", "Accept:", "Authorization: Bearer")
actual = []
for ln in RAW.splitlines():
    for p in patterns:
        if p in ln:
            v = ln[ln.index(p):].strip()
            if len(v) > 115:
                v = v[:112] + "..."
            if v not in actual:
                actual.append(v)
            break
actual = actual[:9]
if not any(f"Authorization: Bearer {TOKEN}" in ln for ln in actual):
    raise SystemExit("ERRO: linha de autorizacao nao recuperada.")
(EVID / "trecho-captura-http.txt").write_text(
    "Trechos textuais extraidos de claro.pcap via tcpdump -A -r (nao sao dados simulados).\n"
    + "\n".join(actual) + "\n", encoding="utf-8"
)

sans = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
mono = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
mono_bold = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
for name, path in (("Sans",sans),("SansBold",bold),("Mono",mono),("MonoBold",mono_bold)):
    if not Path(path).exists():
        raise SystemExit(f"Fonte ausente: {path}")
    pdfmetrics.registerFont(TTFont(name,path))
fs = ImageFont.truetype(sans, 23)
fb = ImageFont.truetype(bold, 28)
fm = ImageFont.truetype(mono, 20)
fmb = ImageFont.truetype(mono_bold, 20)
img = Image.new("RGB",(1300,480),(16,25,45))
d=ImageDraw.Draw(img)
d.rounded_rectangle((8,8,1292,472),radius=24,outline=(73,100,131),width=3)
d.rounded_rectangle((18,18,1282,103),radius=18,fill=(28,43,66))
d.text((49,37),"CAPTURA REAL • LABORATÓRIO ISOLADO",font=fb,fill=(234,247,255))
d.text((52,114),"claro.pcap  /  HTTP  /  porta 8080  /  dados lidos no roteador",font=fs,fill=(150,190,222))
for i,ln in enumerate(actual[:7]):
    y=170+i*40
    if ln.startswith("Authorization: Bearer"):
        d.rounded_rectangle((32,y-5,1265,y+34),radius=8,fill=(100,57,37))
        font=fmb; color=(255,227,170)
    else:
        font=fm; color=(226,239,253)
    # 78 caracteres da fonte mono de 20 px cabem na largura.
    d.text((46,y),ln[:78],font=font,fill=color)
img_path=EVID/"captura-http-real.png"
img.save(img_path,optimize=True)

PAGE_W,PAGE_H=A4
pdf_path=ROOT/"cartilha.pdf"
c=canvas.Canvas(str(pdf_path),pagesize=A4)
c.setTitle("Senha sem cadeado: guia de Wi-Fi seguro — Entrega 5")
navy=HexColor("#10203B")
ink=HexColor("#182B45")
muted=HexColor("#526277")
cyan=HexColor("#087F92")
orange=HexColor("#D96C2D")
white=HexColor("#FFFFFF")

def text(s,x,y,size=10,font="Sans",color=ink):
    c.setFillColor(color);c.setFont(font,size);c.drawString(x,y,s)

def wrap(s,max_w,size=9.6,font="Sans"):
    words=s.split()
    out=[]; row=""
    for word in words:
        probe=(row+" "+word).strip()
        if pdfmetrics.stringWidth(probe,font,size)>max_w and row:
            out.append(row);row=word
        else: row=probe
    if row:out.append(row)
    return out

def para(s,x,y,width,size=9.6,leading=13.8,font="Sans",color=ink):
    for ln in wrap(s,width,size,font):
        text(ln,x,y,size,font,color);y-=leading
    return y

c.setFillColor(HexColor("#F5F8FB"));c.rect(0,0,PAGE_W,PAGE_H,fill=1,stroke=0)
c.setFillColor(navy);c.rect(0,PAGE_H-129,PAGE_W,129,fill=1,stroke=0)
text("GUIA PRÁTICO • SEGURANÇA DIGITAL",36,806,9.5,"SansBold",HexColor("#83DFE1"))
text("SENHA SEM CADEADO?",36,772,22,"SansBold",white)
text("Saiba o que acontece e como se proteger no celular.",36,746,11,"Sans",white)
text("Teste educativo feito apenas entre máquinas do nosso laboratório.",36,726,8.8,"Sans",HexColor("#CAD6E4"))

text("O QUE A NOSSA CAPTURA MOSTROU",36,689,11.5,"SansBold",ink)
para("Quando usamos uma conexão sem proteção (HTTP), o segredo inventado apareceu legível no caminho da rede. Abaixo está um trecho verdadeiro do nosso arquivo claro.pcap.",36,672,520,9.2,13.4)
c.drawImage(ImageReader(img),36,447,width=523,height=193,mask="auto")
text("No teste com HTTPS, a rede teve tráfego, mas o segredo não apareceu em texto legível.",37,433,8.8,"SansBold",cyan)

c.setFillColor(HexColor("#DDEDF4"));c.roundRect(36,353,523,65,9,fill=1,stroke=0)
text("COMO CONFERIR NO CELULAR",50,398,10.6,"SansBold",navy)
para("Toque no ícone ao lado do endereço do site e veja as informações da conexão. Procure HTTPS e ausência de alertas. O desenho do ícone muda conforme o navegador. Confira também se o endereço é realmente o oficial.",50,381,490,8.7,12.2)

text("3 ATITUDES QUE PROTEGEM VOCÊ",36,330,11,"SansBold",ink)
actions=[
("1","NÃO DIGITE SENHAS EM SITE NÃO SEGURO","Se aparecer “Não seguro” ou erro de certificado, feche a página e entre pelo endereço oficial."),
("2","CUIDADO COM WI-FI PÚBLICO","Para banco e contas importantes, prefira os dados móveis. Se usar o Wi-Fi, confira HTTPS e o endereço."),
("3","SE JÁ DIGITOU, AJA","Troque a senha no site oficial e ative a verificação em duas etapas.")
]
y=308
for number,heading,desc in actions:
    c.setFillColor(orange);c.roundRect(36,y-48,27,44,8,fill=1,stroke=0)
    text(number,44,y-29,13,"SansBold",white)
    text(heading,75,y-8,9.2,"SansBold",ink)
    para(desc,75,y-23,477,8.5,12.0)
    y-=62

c.setStrokeColor(HexColor("#C7D1DC")); c.line(36,113,559,113)
para("Importante: HTTPS ajuda a proteger o conteúdo durante o transporte, mas não comprova que um site seja verdadeiro. No laboratório usamos certificado autoassinado; em sites reais, nunca ignore avisos de certificado.",36,100,523,8.0,11.4,color=muted)
text("Fonte visual: captura HTTP real do próprio grupo • Demonstração com segredo fictício.",36,52,7.7,"Sans",muted)
text("Redes e Sistemas Distribuídos • Entrega 5 — Extensão",36,36,7.7,"SansBold",cyan)
c.showPage();c.save()
print("OK: PDF gerado a partir de PCAP real:", pdf_path)
