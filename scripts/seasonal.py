#!/usr/bin/env python3
"""Render a deterministic seasonal SVG banner, using Europe/Paris calendar dates."""
from __future__ import annotations
import argparse
from datetime import datetime, date
from pathlib import Path
from zoneinfo import ZoneInfo
from xml.sax.saxutils import escape
import math, random

THEMES = {
 'default': ('FRONTIER // ALWAYS CREATING','#0b111c','#6dd8ce','#283f54','✦'),
 'winter': ('WINTER // CODE IN THE COLD','#101d34','#8bd9ff','#344e78','❄'),
 'spring': ('SPRING // NEW IDEAS BLOOM','#162b29','#a7e4a2','#386d63','✿'),
 'summer': ('SUMMER // KEEP BUILDING','#15283d','#ffd17d','#436f9a','☀'),
 'autumn': ('AUTUMN // REFACTOR AND RISE','#261b20','#f3a866','#71443b','◆'),
 'halloween': ('HALLOWEEN // NIGHT SHIFT','#1c102a','#ff9a42','#6e3778','✦'),
 'christmas': ('CHRISTMAS // MERRY COMMITMAS','#12292b','#ff6c70','#317969','✧'),
 'easter': ('EASTER // FRESH START','#263047','#ffbfdb','#7772a9','✿'),
}

def easter_sunday(year):
 a=year%19;b=year//100;c=year%100;d=b//4;e=b%4;f=(b+8)//25;g=(b-f+1)//3
 h=(19*a+b-d-g+15)%30;i=c//4;k=c%4;l=(32+2*e+2*i-h-k)%7
 m=(a+11*h+22*l)//451;month=(h+l-7*m+114)//31;day=(h+l-7*m+114)%31+1
 return date(year,month,day)

def theme_for(day):
 m,d=day.month,day.day
 # Holiday windows override the underlying meteorological season.
 if (m==12 and d>=15) or (m==1 and d<=6):return 'christmas'
 if m==10 and d>=20:return 'halloween'
 if abs((day-easter_sunday(day.year)).days)<=7:return 'easter'
 if m in (12,1,2):return 'winter'
 if m in (3,4,5):return 'spring'
 if m in (6,7,8):return 'summer'
 return 'autumn'

def render(theme):
 name,bg,accent,mid,symbol=THEMES[theme]
 random.seed('angeBiancamaria-'+theme)
 W,H=900,260
 out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(name)}">',
 f'<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="{bg}"/><stop offset="1" stop-color="{mid}"/></linearGradient><pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{accent}" stroke-opacity=".09"/></pattern></defs>',
 '<rect width="900" height="260" rx="20" fill="url(#bg)"/><rect width="900" height="260" rx="20" fill="url(#grid)"/>',
 f'<rect x="16" y="16" width="868" height="228" rx="14" fill="none" stroke="{accent}" stroke-opacity=".42"/>',
 f'<path d="M35 53H132 M768 207H865" stroke="{accent}" stroke-width="4"/>']
 for i in range(38):
  x=random.randint(24,875);y=random.randint(25,231);size=random.choice([2,3,4,5]);opacity=random.choice(['.2','.35','.5','.7'])
  if theme=='winter':out.append(f'<g stroke="{accent}" stroke-opacity="{opacity}" stroke-width="1.5"><path d="M{x-size} {y}h{size*2} M{x} {y-size}v{size*2} M{x-size*.7:.1f} {y-size*.7:.1f}l{size*1.4:.1f} {size*1.4:.1f} M{x+size*.7:.1f} {y-size*.7:.1f}l{-size*1.4:.1f} {size*1.4:.1f}"/></g>')
  elif theme=='halloween':out.append(f'<path d="M{x-size*2} {y}q{size} {-size*2} {size*2} 0q{size} {-size*2} {size*2} 0" stroke="{accent}" stroke-opacity="{opacity}" fill="none" stroke-width="2"/>')
  elif theme=='autumn':out.append(f'<path d="M{x} {y-size}q{size*2} {size} 0 {size*2}q{-size*2} {-size} 0 {-size*2}" fill="{accent}" opacity="{opacity}"/>')
  elif theme=='easter':out.append(f'<ellipse cx="{x}" cy="{y}" rx="{size}" ry="{size*1.5}" fill="{accent}" opacity="{opacity}"/>')
  elif theme=='christmas':out.append(f'<circle cx="{x}" cy="{y}" r="{size}" fill="{accent}" opacity="{opacity}"/>')
  elif theme=='spring':out.append(f'<g fill="{accent}" opacity="{opacity}"><circle cx="{x-size}" cy="{y}" r="{size}"/><circle cx="{x+size}" cy="{y}" r="{size}"/><circle cx="{x}" cy="{y-size}" r="{size}"/><circle cx="{x}" cy="{y+size}" r="{size}"/></g>')
  else:out.append(f'<circle cx="{x}" cy="{y}" r="{size}" fill="{accent}" opacity="{opacity}"/>')
 # Text with safe zones and strong contrast.
 out += ['<rect x="158" y="66" width="585" height="131" rx="18" fill="#090e18" fill-opacity=".78"/>',
 '<text x="450" y="119" text-anchor="middle" font-family="Verdana,Arial,sans-serif" font-size="34" font-weight="700" fill="#f2f6ff">ANGE BIANCAMARIA</text>',
 f'<text x="450" y="157" text-anchor="middle" font-family="Verdana,Arial,sans-serif" font-size="17" letter-spacing="2" fill="{accent}">{escape(name)}</text>',
 '<text x="450" y="181" text-anchor="middle" font-family="Verdana,Arial,sans-serif" font-size="12" fill="#bdc8d5">FULL STACK DEVELOPER  ·  CORSICA</text>',
 '</svg>']
 return '\n'.join(out)+'\n'

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--date',help='YYYY-MM-DD (test/preview)');ap.add_argument('--theme',choices=THEMES,help='Force a theme for preview');ap.add_argument('--all',action='store_true',help='Also generate every theme preview');args=ap.parse_args()
 day=date.fromisoformat(args.date) if args.date else datetime.now(ZoneInfo('Europe/Paris')).date()
 selected=args.theme or theme_for(day)
 dest=Path(__file__).resolve().parents[1]/'img'/'seasonal';dest.mkdir(parents=True,exist_ok=True)
 target=dest/'current.svg';content=render(selected)
 if not target.exists() or target.read_text(encoding='utf-8')!=content:target.write_text(content,encoding='utf-8')
 if args.all:
  for key in THEMES:(dest/f'{key}.svg').write_text(render(key),encoding='utf-8')
 print(f'{day}: {selected} -> {target}')
if __name__=='__main__':main()
