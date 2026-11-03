#!/usr/bin/env python3
"""Apply a seasonal skin to the EXISTING profile graphics, without extra banners."""
from __future__ import annotations
import argparse, datetime as dt, random, re
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT=Path(__file__).resolve().parents[1]
PALETTES={
 'winter':('#8bd9ff','#c9f2ff','#18283c','snow'),
 'spring':('#a7e4a2','#ffc4dc','#142b2b','flower'),
 'summer':('#ffd17d','#65d8e7','#152b3a','sun'),
 'autumn':('#f3a866','#e6ba6b','#2a1d21','leaf'),
 'halloween':('#ff9a42','#c38aff','#241529','bat'),
 'christmas':('#ff737d','#75dfb4','#172d2a','star'),
 'easter':('#ffc4dc','#b8b0ff','#2b263a','egg'),
 'birthday':('#ff86cf','#ffd17d','#2d1a35','confetti'),
}

def easter(year):
 a=year%19;b=year//100;c=year%100;d=b//4;e=b%4;f=(b+8)//25;g=(b-f+1)//3
 h=(19*a+b-d-g+15)%30;i=c//4;k=c%4;l=(32+2*e+2*i-h-k)%7
 m=(a+11*h+22*l)//451;n=(h+l-7*m+114)//31;day=(h+l-7*m+114)%31+1
 return dt.date(year,n,day)

def theme_for(day):
 m,d=day.month,day.day
 if (m,d)==(1,9):return 'birthday'
 if (m==12 and d>=15) or (m==1 and d<=6):return 'christmas'
 if m==10 and d>=20:return 'halloween'
 if abs((day-easter(day.year)).days)<=4:return 'easter'
 if m in (12,1,2):return 'winter'
 if m in (3,4,5):return 'spring'
 if m in (6,7,8):return 'summer'
 return 'autumn'


TITLES={
 'winter':('WINTER MODE','❄'), 'spring':('SPRING BLOOM','✿'),
 'summer':('SUMMER VIBES','☀'), 'autumn':('AUTUMN SEASON','◆'),
 'halloween':('HALLOWEEN NIGHT','☾'), 'christmas':('MERRY CHRISTMAS','✦'),
 'easter':('HAPPY EASTER','✿'), 'birthday':("HAPPY BIRTHDAY • 09 JAN",'★')
}
def decorations(theme,w,h):
 accent,secondary,_,shape=PALETTES[theme]
 rng=random.Random('ange-strong-v3-'+theme+str(w))
 out=['<g class="seasonal-decor" pointer-events="none">']
 # Animated neon perimeter + top season label: no second name banner.
 out.append(f'<rect x="14" y="14" width="{w-28}" height="{h-28}" rx="18" fill="none" stroke="{accent}" stroke-width="3" opacity=".7"/>')
 out.append(f'<rect x="23" y="23" width="{w-46}" height="{h-46}" rx="14" fill="none" stroke="{secondary}" stroke-width="1.3" stroke-dasharray="10 9" opacity=".38"/>')
 out.append(f'<path d="M35 27 H{min(w-35,280)}" stroke="{secondary}" stroke-width="5" stroke-linecap="round"><animate attributeName="opacity" values=".35;1;.35" dur="4s" repeatCount="indefinite"/></path>')
 title,_=TITLES[theme]
 # Seasonal label in top-right safe area of both existing cards.
 label_width=min(300,14+len(title)*9)
 out.append(f'<rect x="{w-label_width-35}" y="32" width="{label_width}" height="34" rx="9" fill="#0b101a" fill-opacity=".92" stroke="{accent}" stroke-width="2"/>')
 out.append(f'<text x="{w-47}" y="54" text-anchor="end" font-family="Arial,sans-serif" font-size="15" font-weight="bold" letter-spacing="1" fill="{secondary}">{title}</text>')
 # Large recognizable edge motifs, animated in SVG (GitHub may limit SVG animation).
 for i in range(34):
  side=i%4
  if side==0:x=rng.randint(25,w-25);y=rng.randint(70,85)
  elif side==1:x=rng.randint(25,w-25);y=rng.randint(h-75,h-25)
  elif side==2:x=rng.randint(20,78);y=rng.randint(80,h-60)
  else:x=rng.randint(w-78,w-20);y=rng.randint(80,h-60)
  r=rng.randint(5,11)
  if shape=='snow':
   mark=f'<path d="M{-r} 0H{r} M0 {-r}V{r} M{-r*.7:.1f} {-r*.7:.1f}L{r*.7:.1f} {r*.7:.1f} M{r*.7:.1f} {-r*.7:.1f}L{-r*.7:.1f} {r*.7:.1f}" stroke="{accent}" stroke-width="2.5"/>'
  elif shape=='leaf':
   mark=f'<path d="M0 {-r}Q{r*2} 0 0 {r}Q{-r*2} 0 0 {-r}Z" fill="{accent}" stroke="{secondary}" stroke-width="1"/>'
  elif shape=='flower':
   mark=''.join(f'<circle cx="{dx}" cy="{dy}" r="{r*.62:.1f}" fill="{accent}"/>' for dx,dy in [(-r,0),(r,0),(0,-r),(0,r)])+f'<circle r="{r*.6:.1f}" fill="{secondary}"/>'
  elif shape=='bat':
   mark=f'<path d="M{-2*r} 0Q{-r} {-2*r} 0 0Q{r} {-2*r} {2*r} 0L{r} {r*.3}L0 {-r*.4}L{-r} {r*.3}Z" fill="{accent}"/>'
  elif shape=='egg':
   mark=f'<ellipse rx="{r*.8}" ry="{r*1.3}" fill="{accent}"/><path d="M{-r*.6} 0H{r*.6}" stroke="{secondary}" stroke-width="3"/>'
  elif shape=='sun':
   mark=f'<circle r="{r}" fill="{accent}"/><circle r="{r*1.55}" fill="none" stroke="{secondary}" stroke-width="2" stroke-dasharray="3 4"/>'
  elif shape=='star':
   mark=f'<path d="M0 {-r*1.6}L{r*.4} {-r*.4}L{r*1.6} 0L{r*.4} {r*.4}L0 {r*1.6}L{-r*.4} {r*.4}L{-r*1.6} 0L{-r*.4} {-r*.4}Z" fill="{accent}"/>'
  else:
   mark=f'<rect x="{-r/2}" y="{-r/2}" width="{r}" height="{r*.6}" rx="1" fill="{rng.choice([accent,secondary])}"/>'
  dur=5+i%5
  out.append(f'<g transform="translate({x} {y})" opacity=".85">{mark}<animateTransform attributeName="transform" type="translate" additive="sum" values="0 0;0 {-5-i%8};0 0" dur="{dur}s" repeatCount="indefinite"/><animate attributeName="opacity" values=".4;.95;.4" dur="{dur}s" repeatCount="indefinite"/></g>')
 # Festive decorative string across the bottom, or seasonal light line.
 out.append(f'<path d="M35 {h-31}Q{w//2} {h-54} {w-35} {h-31}" stroke="{secondary}" stroke-width="2" fill="none" opacity=".7"/>')
 for i in range(16):
  x=50+i*(w-100)/15
  y=h-31-((x-35)*(w-35-x)/(w*w))*90
  out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="{accent}"><animate attributeName="opacity" values=".3;1;.3" dur="{2+i%4}s" repeatCount="indefinite"/></circle>')
 out.append('</g>')
 return '\n'.join(out)

def decorate_svg(source,theme):
 accent,secondary,bg,_=PALETTES[theme]
 s=source
 for old,new in [('#111827',bg),('#0b1220',bg),('#60a5fa',accent),('#93c5fd',secondary),('#2563eb',accent),('#ef4444',secondary),('#303b52',accent),('#172554',bg),('#080d18',bg)]:
  s=s.replace(old,new)
 m=re.search(r'<svg[^>]*viewBox="0 0 (\d+) (\d+)"',s)
 if not m:raise ValueError('SVG missing viewBox')
 w,h=map(int,m.groups())
 return s.replace('</svg>',decorations(theme,w,h)+'\n</svg>')

def main():
 p=argparse.ArgumentParser();p.add_argument('--date');p.add_argument('--theme',choices=PALETTES);p.add_argument('--preview-all',action='store_true');p.add_argument('--print-theme',action='store_true')
 args=p.parse_args();day=dt.date.fromisoformat(args.date) if args.date else dt.datetime.now(ZoneInfo('Europe/Paris')).date()
 theme=args.theme or theme_for(day)
 if args.print_theme:print(theme);return
 out=ROOT/'img/seasonal';out.mkdir(parents=True,exist_ok=True)
 for source,name in [('corsica_card.svg','corsica_current.svg'),('my_goals.svg','goals_current.svg')]:
  original=(ROOT/'img'/source).read_text(encoding='utf-8')
  (out/name).write_text(decorate_svg(original,theme),encoding='utf-8')
  if args.preview_all:
   for t in PALETTES:(out/f'{Path(source).stem}_{t}.svg').write_text(decorate_svg(original,t),encoding='utf-8')
 # Update existing animated header palette and typing animation color, no second name banner.
 readme=ROOT/'README.md';s=readme.read_text(encoding='utf-8')
 accent,secondary,_,_=PALETTES[theme]
 s=re.sub(r'(&color=)(?:gradient|[0-9a-fA-F]{6})(?=&section=header)',lambda m:m.group(1)+accent.lstrip('#'),s,count=1)
 s=re.sub(r'(&color=)(?:gradient|[0-9a-fA-F]{6})(?=&section=header)',lambda m:m.group(1)+accent.lstrip('#'),s,count=1)
 s=re.sub(r'(pause=1000&color=)[0-9A-Fa-f]{6}',lambda m:m.group(1)+accent.lstrip('#').upper(),s,count=1)
 readme.write_text(s,encoding='utf-8')
 print(f'{day} -> {theme} (existing header, Corsica card, goals)')
if __name__=='__main__':main()
