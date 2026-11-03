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

def decorations(theme,w,h):
 accent,secondary,_,shape=PALETTES[theme]
 rng=random.Random('ange-season-'+theme+str(w))
 out=['<g class="seasonal-decor" pointer-events="none">']
 # Decorate only edges, keeping text, the Corsica silhouette and target centers legible.
 for i in range(30):
  x=rng.choice([rng.randint(12,90),rng.randint(w-100,w-12),rng.randint(95,w-95)])
  y=rng.randint(12,h-12)
  if 95<x<w-95 and 65<y<h-65:continue
  r=rng.randint(3,7)
  if shape=='snow':mark=f'<path d="M{x-r} {y}h{2*r} M{x} {y-r}v{2*r} M{x-r*.7:.1f} {y-r*.7:.1f}l{r*1.4:.1f} {r*1.4:.1f} M{x+r*.7:.1f} {y-r*.7:.1f}l{-r*1.4:.1f} {r*1.4:.1f}" stroke="{accent}" stroke-width="1.6"/>'
  elif shape=='leaf':mark=f'<path d="M{x} {y-r}q{r*2} {r} 0 {r*2}q{-r*2} {-r} 0 {-r*2}" fill="{accent}"/>'
  elif shape=='flower':mark=''.join(f'<circle cx="{x+dx}" cy="{y+dy}" r="{r*.6:.1f}" fill="{accent}"/>' for dx,dy in [(-r,0),(r,0),(0,-r),(0,r)])+f'<circle cx="{x}" cy="{y}" r="{r*.45}" fill="{secondary}"/>'
  elif shape=='bat':mark=f'<path d="M{x-2*r} {y}q{r} {-2*r} {2*r} 0q{r} {-2*r} {2*r} 0" stroke="{accent}" fill="none" stroke-width="2"/>'
  elif shape=='egg':mark=f'<ellipse cx="{x}" cy="{y}" rx="{r*.8}" ry="{r*1.2}" fill="{accent}"/><path d="M{x-r*.5} {y}h{r}" stroke="{secondary}" stroke-width="2"/>'
  elif shape=='sun':mark=f'<circle cx="{x}" cy="{y}" r="{r}" fill="{accent}"/>'
  elif shape=='star':mark=f'<path d="M{x} {y-r}L{x+r*.3} {y-r*.3}L{x+r} {y}L{x+r*.3} {y+r*.3}L{x} {y+r}L{x-r*.3} {y+r*.3}L{x-r} {y}L{x-r*.3} {y-r*.3}Z" fill="{accent}"/>'
  else:mark=f'<rect x="{x}" y="{y}" width="{r}" height="{r*.55}" rx="1" fill="{rng.choice([accent,secondary])}" transform="rotate({rng.randint(-50,50)} {x} {y})"/>'
  out.append(f'<g opacity="{rng.choice([.25,.4,.55,.75])}">{mark}</g>')
 out.append('</g>')
 return '\n'.join(out)

def decorate_svg(source,theme):
 accent,secondary,bg,_=PALETTES[theme]
 s=source
 # Keep every existing shape and label; only replace accent strokes and dark backgrounds.
 for old,new in [('#111827',bg),('#0b1220',bg),('#60a5fa',accent),('#93c5fd',secondary),('#2563eb',accent),('#ef4444',secondary)]:
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
