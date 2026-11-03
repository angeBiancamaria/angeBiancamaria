#!/usr/bin/env python3
"""Apply a seasonal skin to the EXISTING profile graphics, without extra banners."""
from __future__ import annotations
import argparse, datetime as dt, random, re, hashlib
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
def decorations(theme,w,h,kind):
    """Safe decoration zones: 0-35px border, no particles over text."""
    accent,secondary,_,shape=PALETTES[theme]
    rng=random.Random('safe-v6-'+theme+kind)
    out=['<g class="seasonal-decor" pointer-events="none">']
    out.append(f'<rect x="10" y="10" width="{w-20}" height="{h-20}" rx="17" fill="none" stroke="{accent}" stroke-width="3" opacity=".65"/>')
    out.append(f'<rect x="20" y="20" width="{w-40}" height="{h-40}" rx="14" fill="none" stroke="{secondary}" stroke-width="1.3" stroke-dasharray="12 12" opacity=".3"/>')
    # The title is intentionally NOT placed inside either card: it now lives in README text.
    # All particles are restricted to the very top/bottom border strips.
    for i in range(24):
        x=40+(i*(w-80)/23)
        y=(28 if i%2 else h-27)
        r=3+(i%3)
        if shape=='snow':
            mark=f'<path d="M{-r} 0H{r} M0 {-r}V{r}" stroke="{accent}" stroke-width="2"/>'
        elif shape=='leaf':
            mark=f'<path d="M0 {-r}Q{r*1.5} 0 0 {r}Q{-r*1.5} 0 0 {-r}" fill="{accent}"/>'
        elif shape=='flower':
            mark=f'<circle r="{r}" fill="{accent}"/><circle r="1.5" fill="{secondary}"/>'
        elif shape=='bat':
            mark=f'<path d="M{-r*2} 0Q{-r} {-r} 0 0Q{r} {-r} {r*2} 0L0 {r}Z" fill="{accent}"/>'
        elif shape=='egg':
            mark=f'<ellipse rx="{r}" ry="{r*1.5}" fill="{accent}"/>'
        elif shape=='sun':
            mark=f'<circle r="{r}" fill="{accent}"/>'
        elif shape=='star':
            mark=f'<path d="M0 {-r}L{r/3} {-r/3}L{r} 0L{r/3} {r/3}L0 {r}L{-r/3} {r/3}L{-r} 0L{-r/3} {-r/3}Z" fill="{accent}"/>'
        else:
            mark=f'<rect x="{-r/2}" y="{-r/2}" width="{r}" height="{r}" fill="{accent}"/>'
        out.append(f'<g transform="translate({x:.1f} {y})">{mark}<animate attributeName="opacity" values=".35;1;.35" dur="{3+i%4}s" repeatCount="indefinite"/></g>')
    out.append('</g>')
    return '\\n'.join(out)

def scene_details(theme,w,h):
    """Large recognizable themed illustrations anchored at card edges, never covering the map or goals."""
    a,b,_,_=PALETTES[theme]
    x=w-112; y=h-118
    out=['<g class="seasonal-scene" pointer-events="none">']
    if theme=='birthday':
        out += [
          f'<g transform="translate({x} {y})"><ellipse cx="32" cy="92" rx="60" ry="8" fill="{b}" opacity=".24"/>'
          '<rect x="-10" y="35" width="86" height="50" rx="8" fill="#f8a4c9" stroke="#fff0df" stroke-width="3"/>'
          '<path d="M-10 47 Q2 59 14 47 Q26 59 38 47 Q50 59 62 47 Q72 57 76 47 V35 H-10Z" fill="#fff1e8"/>'
          '<rect x="-15" y="20" width="96" height="17" rx="7" fill="#ffd17d"/>'
          '<path d="M14 20 V-7 M36 20 V-7 M58 20 V-7" stroke="#fff2da" stroke-width="6"/>'
          '<path d="M14 -9 Q5 -22 14 -29 Q23 -22 14 -9 M36 -9 Q27 -22 36 -29 Q45 -22 36 -9 M58 -9 Q49 -22 58 -29 Q67 -22 58 -9" fill="#ffcc51">'
          '<animate attributeName="opacity" values=".7;1;.7" dur="1.2s" repeatCount="indefinite"/></path></g>',
          f'<g transform="translate({w-190} 130)"><path d="M0 0 Q-24 -30 0 -55 Q28 -40 0 0" fill="{a}"/><path d="M0 0 Q-18 25 0 50" stroke="{b}" fill="none" stroke-width="2"/><animateTransform attributeName="transform" type="rotate" additive="sum" values="-4;4;-4" dur="4s" repeatCount="indefinite"/></g>'
        ]
    elif theme=='halloween':
        out += [
          f'<g transform="translate({x} {y+18})"><ellipse cx="30" cy="47" rx="54" ry="45" fill="#ff8d32" stroke="#ffbd64" stroke-width="3"/>'
          '<path d="M30 2 Q25 -14 38 -20" stroke="#64aa63" stroke-width="9" fill="none"/>'
          '<path d="M-3 33 L12 20 L17 37Z M40 37 L48 20 L63 33Z M8 53 Q30 78 53 53 L46 51 L40 62 L31 52 L22 62 L15 51Z" fill="#211325"/>'
          '<ellipse cx="30" cy="47" rx="45" ry="36" stroke="#e06a24" fill="none" stroke-width="2"/></g>',
          f'<g transform="translate({w-220} 100)" fill="#c38aff"><path d="M0 10 Q-22 -10 -48 8 L-32 4 L-23 15 L-9 8 L0 20 L9 8 L23 15 L32 4 L48 8 Q22 -10 0 10Z"/><animateTransform attributeName="transform" type="translate" additive="sum" values="0 0;0 18;0 0" dur="5s" repeatCount="indefinite"/></g>'
        ]
    elif theme=='christmas':
        out += [
          f'<g transform="translate({x} {y-3})"><path d="M30 -14 L-20 50 H-4 L-30 79 H90 L64 50 H80Z" fill="#29936d" stroke="#75dfb4" stroke-width="3"/>'
          '<rect x="22" y="79" width="16" height="20" fill="#a77958"/>'
          '<path d="M30 -30 L36 -15 L52 -15 L39 -5 L44 11 L30 1 L16 11 L21 -5 L8 -15 L24 -15Z" fill="#ffd17d"/>'
          '<circle cx="12" cy="35" r="5" fill="#ff737d"/><circle cx="48" cy="47" r="5" fill="#ffd17d"/><circle cx="30" cy="67" r="5" fill="#eaf8ff"/>'
          '<circle cx="30" cy="67" r="5" fill="#fff"><animate attributeName="opacity" values="0;1;0" dur="2s" repeatCount="indefinite"/></circle></g>'
        ]
    elif theme=='winter':
        out += [
          f'<g transform="translate({x} {y})"><circle cx="30" cy="58" r="39" fill="#e4f7ff"/><circle cx="30" cy="3" r="29" fill="#f5fbff"/>'
          '<circle cx="20" cy="-4" r="4" fill="#253b53"/><circle cx="41" cy="-4" r="4" fill="#253b53"/>'
          '<path d="M30 1 L57 8 L30 13Z" fill="#ff9c45"/><path d="M-2 27 H65" stroke="#8bd9ff" stroke-width="9"/>'
          '<circle cx="30" cy="43" r="4" fill="#253b53"/><circle cx="30" cy="60" r="4" fill="#253b53"/></g>'
        ]
    elif theme=='spring':
        out += [
          f'<g transform="translate({x} {y})"><path d="M30 95 Q12 32 30 -4" fill="none" stroke="#71bd79" stroke-width="7"/>'
          '<path d="M25 65 Q-14 31 -12 55 Q-5 72 25 65 M29 46 Q69 13 75 36 Q63 53 29 46" fill="#71bd79"/>'
          '<g fill="#ffc4dc"><circle cx="30" cy="-15" r="20"/><circle cx="10" cy="1" r="20"/><circle cx="50" cy="1" r="20"/><circle cx="19" cy="25" r="20"/><circle cx="43" cy="25" r="20"/></g>'
          '<circle cx="30" cy="7" r="15" fill="#ffe38e"/></g>'
        ]
    elif theme=='summer':
        out += [
          f'<g transform="translate({x+20} {y+12})"><circle cx="25" cy="24" r="39" fill="#ffd17d"/>'
          '<circle cx="25" cy="24" r="55" fill="none" stroke="#ffd17d" stroke-width="5" stroke-dasharray="6 14"/>'
          '<path d="M-55 98 Q-15 78 25 98 T105 98" stroke="#65d8e7" stroke-width="7" fill="none"/>'
          '<path d="M-55 111 Q-15 91 25 111 T105 111" stroke="#65d8e7" stroke-width="4" fill="none" opacity=".6"/></g>'
        ]
    elif theme=='autumn':
        out += [
          f'<g transform="translate({x} {y})"><path d="M26 95 Q42 30 24 -20" stroke="#a86b47" stroke-width="8" fill="none"/>'
          '<path d="M24 15 Q-26 -22 -14 29 Q3 52 24 15 M24 15 Q80 -27 80 19 Q50 51 24 15" fill="#f3a866" stroke="#e6ba6b" stroke-width="3"/>'
          '<path d="M25 40 Q-17 21 -9 61 Q8 79 25 40" fill="#c16b3c"/></g>'
        ]
    elif theme=='easter':
        out += [
          f'<g transform="translate({x} {y})"><ellipse cx="26" cy="40" rx="39" ry="55" fill="#ffc4dc" stroke="#fff1fa" stroke-width="3"/>'
          '<path d="M-7 28 Q24 12 60 28 M-10 51 Q24 35 63 51" stroke="#b8b0ff" stroke-width="9" fill="none"/>'
          '<circle cx="26" cy="-2" r="6" fill="#fff1fa"/><circle cx="26" cy="81" r="6" fill="#fff1fa"/></g>'
        ]
    # Small moving particles near the borders; keep main content unobstructed.
    if theme in ('winter','christmas','birthday','autumn','spring'):
        glyph={'winter':'❄','christmas':'✦','birthday':'✦','autumn':'◆','spring':'✿'}[theme]
        for i in range(12):
            px=45+(i*73)%(w-90)
            py=55+(i*37)%(h-110)
            if w*.23<px<w*.85 and h*.2<py<h*.8:
                py=48 if i%2 else h-48
            out.append(f'<text x="{px}" y="{py}" fill="{a}" font-size="{13+i%4*3}" opacity=".65">{glyph}'
                       f'<animateTransform attributeName="transform" type="translate" values="0 -7;0 11;0 -7" dur="{4+i%5}s" repeatCount="indefinite"/>'
                       '</text>')
    out.append('</g>')
    return '\n'.join(out)

def decorate_svg(source,theme,kind):
 accent,secondary,bg,_=PALETTES[theme]
 s=source
 for old,new in [('#111827',bg),('#0b1220',bg),('#60a5fa',accent),('#93c5fd',secondary),('#2563eb',accent),('#ef4444',secondary),('#303b52',accent),('#172554',bg),('#080d18',bg)]:
  s=s.replace(old,new)
 m=re.search(r'<svg[^>]*viewBox="0 0 (\d+) (\d+)"',s)
 if not m:raise ValueError('SVG missing viewBox')
 w,h=map(int,m.groups())
 return s.replace('</svg>',decorations(theme,w,h,kind)+'\n</svg>')

def update_image_refs(readme: str, theme: str) -> str:
    """Switch both cards to stable, theme-specific paths; preserve surrounding HTML."""
    for stem, old in (("corsica_card", "corsica_current"), ("my_goals", "goals_current")):
        target = f"img/seasonal/{stem}_{theme}.svg"
        # Handles relative paths, raw.githubusercontent.com URLs and old ?v= digests.
        pattern = rf"img/seasonal/(?:{stem}_(?:winter|spring|summer|autumn|halloween|christmas|easter|birthday)|{old})\.svg(?:\?(?:v=[0-9a-f]+|test=[a-zA-Z0-9_-]+))?"
        readme, count = re.subn(pattern, target, readme)
        if count == 0:
            raise ValueError(f"README missing seasonal image reference for {stem}; refusing to silently skip it")
    return readme


SEASONAL_COPY={
 'winter':('❄️ WINTER MODE','Cold outside, ideas in motion.','Building projects one commit at a time.'),
 'spring':('🌸 SPRING BLOOM','New season, new ideas.','Time to make projects grow.'),
 'summer':('☀️ SUMMER VIBES','Sunshine, code and creativity.','Keeping the momentum going.'),
 'autumn':('🍂 AUTUMN SEASON','Fresh ideas are falling into place.','A season for building and learning.'),
 'halloween':('🎃 HALLOWEEN NIGHT','Trick or commit?','No bugs allowed to haunt this repository.'),
 'christmas':('🎄 MERRY CHRISTMAS','A little festive magic in every commit.','Wishing you a wonderful holiday season!'),
 'easter':('🐣 HAPPY EASTER','A few Easter eggs hidden in the code.','New discoveries are always around the corner.'),
 'birthday':('🎂 HAPPY BIRTHDAY — JANUARY 9','Level up! Another year, another adventure.','Today is a special day for this developer.'),
}
BLOCK_START='<!-- SEASONAL_TEXT_START -->'
BLOCK_END='<!-- SEASONAL_TEXT_END -->'

def update_seasonal_text(readme,theme):
    title,lead,sub=SEASONAL_COPY[theme]
    block=f'{BLOCK_START}\n<div align="center">\n\n### {title}\n\n**{lead}**  \n*{sub}*\n\n</div>\n{BLOCK_END}'
    if BLOCK_START in readme and BLOCK_END in readme:
        return re.sub(re.escape(BLOCK_START)+r'.*?'+re.escape(BLOCK_END),lambda _:block,readme,flags=re.S)
    # Insert before the Corsica card, never inside the generated daily quote.
    anchor='<!-- Corsica location card -->'
    if anchor not in readme:
        raise ValueError('Cannot find Corsica location card anchor; README left untouched')
    return readme.replace(anchor,block+'\n\n'+anchor,1)

# The headings and small contextual notes change, but all personal facts, goals,
# project descriptions, skills tables, daily quotes, links and the snake stay intact.
SECTION_THEMES={
'winter': ['❄️ Winter objectives','🧠 Developer profile · Frost mode','⭐ Featured project · Winter build','📖 Currently Learning · Winter workshop','🧰 Languages, Frameworks & Tools · Frost edition','📊 GitHub Stats · Winter streak','📫 Contact'],
'spring': ['🌱 Growing goals','🧠 Developer profile · Fresh start','⭐ Featured project · New growth','🌸 Currently Learning · Growing skills','🧰 Languages, Frameworks & Tools · Spring edition','📊 GitHub Stats · Spring progress','📫 Contact'],
'summer': ['☀️ Summer goals','🧠 Developer profile · Sunny mode','⭐ Featured project · Summer build','🌊 Currently Learning · Summer lab','🧰 Languages, Frameworks & Tools · Summer edition','📊 GitHub Stats · Summer streak','📫 Contact'],
'autumn': ['🍂 Autumn objectives','🧠 Developer profile · Harvest season','⭐ Featured project · Autumn build','📚 Currently Learning · Autumn studies','🧰 Languages, Frameworks & Tools · Autumn edition','📊 GitHub Stats · Autumn progress','📫 Contact'],
'halloween': ['🎯 Spooky objectives','🧪 Developer profile · Secret laboratory','🦇 Featured project · Haunted build','🎃 Currently Learning · Haunted lab','🧰 Languages, Frameworks & Tools · Dark arts of code','📊 GitHub Stats · Spooky streak','📫 Contact'],
'christmas': ['🎁 Holiday goals','🧠 Developer profile · Festive mode','⭐ Featured project · Holiday workshop','🎄 Currently Learning · Winter workshop','🧰 Languages, Frameworks & Tools · Festive edition','📊 GitHub Stats · Holiday streak','📫 Contact'],
'easter': ['🐣 Springtime objectives','🧠 Developer profile · Easter edition','🥚 Featured project · Hidden gems','🐣 Currently Learning · Easter discoveries','🧰 Languages, Frameworks & Tools · Easter edition','📊 GitHub Stats · Easter streak','📫 Contact'],
'birthday': ['🎯 Next-level goals','🧠 Developer profile · Player one','🎮 Featured project · Level-up build','🎂 Currently Learning · Level up!','🧰 Languages, Frameworks & Tools · Birthday edition','📊 GitHub Stats · Achievement unlocked','📫 Contact'],
}
SECTION_BASE=[
'🎯 Current Goal','🧠 Profile','⭐ Featured Project',
'📖 Currently Learning & improving','🧰 Languages, Frameworks & Tools',
'📊 GitHub Stats','📫 Contact'
]
SECTION_NOTES={
'winter':['Quiet season, ambitious plans.','Building steadily, one feature at a time.','Experimenting with technologies during the colder days.','Keeping the stack sharp.','Every contribution counts.'],
'spring':['Fresh season, steady progress.','New ideas are taking shape.','Growing skills one experiment at a time.','Tools for new beginnings.','Progress is blooming.'],
'summer':['Long days, big ideas.','Building something worth sharing.','Exploring technologies under the summer sun.','A bright toolkit for new projects.','Keeping the streak alive.'],
'autumn':['Time to turn plans into results.','Collecting ideas, shipping features.','A new season of learning.','The toolkit behind the projects.','Harvesting progress, commit by commit.'],
'halloween':['No goal is too frightening to tackle.','Enter the developer’s workshop.','Experimenting in the haunted laboratory.','No dark magic required — just code.','Hunting bugs, not ghosts.'],
'christmas':['Wrapping up progress, not ambitions.','A little festive creativity.','New skills are on the wish list.','The workshop is open for business.','Every commit is a small gift.'],
'easter':['Discovering new possibilities.','Something new is hatching.','Finding new skills and hidden gems.','A basket full of technologies.','Collecting commits, not eggs.'],
'birthday':['A new level, the same ambitions.','Another year of creating and improving.','Experience points gained through learning.','Inventory: languages, frameworks and tools.','Achievement unlocked: another year of code.'],
}
SUB_LABELS={
'winter':['❄️ Frontend','🧊 Backend','🔧 Frameworks & Libraries','🛠️ Tools'],
'spring':['🌼 Frontend','🌱 Backend','🌸 Frameworks & Libraries','🛠️ Tools'],
'summer':['☀️ Frontend','🌊 Backend','🏖️ Frameworks & Libraries','🛠️ Tools'],
'autumn':['🍁 Frontend','🍂 Backend','📚 Frameworks & Libraries','🛠️ Tools'],
'halloween':['🕸️ Frontend','🧪 Backend','🔮 Frameworks & Libraries','🦇 Tools'],
'christmas':['🎄 Frontend','🎁 Backend','✨ Frameworks & Libraries','🛠️ Tools'],
'easter':['🐣 Frontend','🥚 Backend','🌸 Frameworks & Libraries','🛠️ Tools'],
'birthday':['🎉 Frontend','🎂 Backend','🎮 Frameworks & Libraries','🛠️ Tools'],
}
NOTE_START='<!-- SEASONAL_SECTION_NOTE:'
def update_readme_sections(readme,theme):
    headings=SECTION_THEMES[theme]
    # Match known originals and all generated variants; refuse if a section
    # cannot be found instead of silently corrupting a custom README.
    for i,base in enumerate(SECTION_BASE):
        variants=[base]+[SECTION_THEMES[t][i] for t in SECTION_THEMES]
        pattern=r'(?m)^## (?:'+ '|'.join(re.escape(v) for v in variants)+r')\s*$'
        readme,count=re.subn(pattern,lambda m:'## '+headings[i],readme,count=1)
        if count!=1:
            raise ValueError(f'Missing expected heading {base!r}; no README saved')
    # Remove previous notes and replace them under the five relevant headings.
    readme=re.sub(r'(?m)^<!-- SEASONAL_SECTION_NOTE:\d+ -->\n.*?\n<!-- /SEASONAL_SECTION_NOTE -->\n\n?', '',readme,flags=re.S)
    indices=[0,2,3,4,5]
    for j,i in enumerate(indices):
        heading='## '+headings[i]
        note=f'<!-- SEASONAL_SECTION_NOTE:{i} -->\n*{SECTION_NOTES[theme][j]}*\n<!-- /SEASONAL_SECTION_NOTE -->'
        readme=readme.replace(heading+'\n',heading+'\n\n'+note+'\n',1)
    # Replace only four literal labels that sit outside the HTML table rows.
    for index,base in enumerate(['Frontend:','Backend:','framework/librairie:','Tools:']):
        variants=[base]+[SUB_LABELS[t][index]+':' for t in SUB_LABELS]
        pattern=r'(<div align="center">)(?:'+'|'.join(re.escape(v) for v in variants)+r')(</div>)'
        readme,count=re.subn(pattern,lambda m:m.group(1)+SUB_LABELS[theme][index]+':'+m.group(2),readme,count=1)
        if count!=1:
            raise ValueError(f'Missing expected technology label {base!r}; no README saved')
    return readme

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--date')
    p.add_argument('--theme', choices=PALETTES)
    p.add_argument('--preview-all', action='store_true', help='kept for backwards compatibility')
    p.add_argument('--print-theme', action='store_true')
    args=p.parse_args()
    day=dt.date.fromisoformat(args.date) if args.date else dt.datetime.now(ZoneInfo('Europe/Paris')).date()
    theme=args.theme or theme_for(day)
    if args.print_theme:
        print(theme)
        return
    out=ROOT/'img/seasonal'
    out.mkdir(parents=True, exist_ok=True)
    # Generate every theme so each README URL resolves to an existing committed file.
    for source,stem in (('corsica_card.svg','corsica_card'),('my_goals.svg','my_goals')):
        original=(ROOT/'img'/source).read_text(encoding='utf-8')
        for t in PALETTES:
            (out/f'{stem}_{t}.svg').write_text(decorate_svg(original,t,stem),encoding='utf-8')
    readme=ROOT/'README.md'
    s=update_image_refs(readme.read_text(encoding='utf-8'),theme)
    s=update_seasonal_text(s,theme)
    s=update_readme_sections(s,theme)
    accent=PALETTES[theme][0].lstrip('#')
    s=re.sub(r'(&color=)(?:gradient|[0-9a-fA-F]{6})(?=&section=header)',lambda m:m.group(1)+accent,s,count=1)
    s=re.sub(r'(pause=1000&color=)[0-9A-Fa-f]{6}',lambda m:m.group(1)+accent.upper(),s,count=1)
    readme.write_text(s,encoding='utf-8')
    print(f'{day} -> {theme}; README points to dedicated SVG files')

if __name__=='__main__':main()
