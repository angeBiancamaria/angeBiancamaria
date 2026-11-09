#!/usr/bin/env python3
"""Generate self-hosted GitHub profile SVG cards. Stdlib only; no external image API."""
import argparse, collections, datetime as dt, html, json, os, random, urllib.request, base64, tempfile, sys, statistics, hashlib
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from seasonal import PALETTES, theme_for
ROOT=Path(__file__).resolve().parents[1]
USER=os.getenv('PROFILE_USER','angeBiancamaria')
OUT=ROOT/'img'/'developer'
CACHE=ROOT/'stats'/'developer_cards_cache.json'
CARDS=['streak','pulse','languages','rpg','timeline','achievements','automation']
THEMES=['winter','spring','summer','autumn','halloween','christmas','easter','birthday']
VARIANTS=('normal','cheapy','strike','sleepy')
VARIANT_LINES={'cheapy':['The budget was cut. Again.','My crown is made of CSS.','Please do not tell the original.'],'strike':['I demand paid vacations and better textures.','No more commits without better working conditions!','My union demands actual pixels.'],'sleepy':['Five more minutes...','Even villains need weekends.','Shhh. The repository can wait.']}
SPECIAL_RATE=10 # 8% Cheapy, 2% Cheapy on strike

LINES={
 'winter':['Cold hands, sinister plans.','Wake me when it is spring.','Snow problem. Probably.'],
 'spring':['Flowers bloom. Chaos follows.','I definitely did not steal these flowers.','Even villains deserve a picnic.'],
 'summer':['I am melting. Tell my story.','The sun and I have unresolved issues.','I need ice cream.'],
 'autumn':['Coffee first. World domination later.','A perfect day for questionable decisions.','The leaves are falling. I am thriving.'],
 'halloween':['The ghosts are unionizing.','Boo. That will be five dollars.','Trust me. I am probably a witch.'],
 'christmas':['Santa knows what you did.','I have been mostly nice this year.','I wrapped your bugs. You are welcome.'],
 'easter':['The eggs know too much.','I am not sharing my chocolate.','Some secrets are better left buried.'],
 'birthday':['Level up! No patch notes included.','Cake is a valid life goal.','Another year, still suspiciously alive.']}
class API:
 def __init__(self): self.token=os.getenv('GH_STATS_TOKEN') or os.getenv('GH_TOKEN') or os.getenv('GITHUB_TOKEN','');self.cache={};self.errors=[];self.fetched=set()
 def get(self,path,params=''):
  url='https://api.github.com/'+path.lstrip('/')+params
  if url in self.cache:return self.cache[url]
  req=urllib.request.Request(url,headers={'Accept':'application/vnd.github+json','User-Agent':'profile-developer-cards','X-GitHub-Api-Version':'2022-11-28',**({'Authorization':'Bearer '+self.token} if self.token else {})})
  try:
   with urllib.request.urlopen(req,timeout=18) as response: data=json.load(response)
  except Exception as exc: self.errors.append(f'{path}: {exc}');data=[]
  if isinstance(data,(dict,list)) and data!=[]:
   self.fetched.add(url)
  self.cache[url]=data;return data
 def pages(self,path,max_pages=5):
  result=[]
  for page in range(1,max_pages+1):
   part=self.get(path,('?' if '?' not in path else '&')+f'per_page=100&page={page}')
   if not isinstance(part,list):break
   result+=part
   if len(part)<100:break
  return result

def esc(x):return html.escape(str(x),quote=True)
def txt(x,y,s,size=15,color='#cbd5e1',weight=400,anchor='start'):
 return f'<text x="{x}" y="{y}" font-family="Segoe UI,Arial,sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{esc(s)}</text>'
def card(name,theme,body,width=820,height=205,foot=None):
 a,b,bg,_=PALETTES[theme]
 content=f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{esc(name)}"><rect width="{width}" height="{height}" rx="18" fill="#0d1117"/><rect x="1.5" y="1.5" width="{width-3}" height="{height-3}" rx="17" fill="none" stroke="{a}" stroke-width="2" opacity=".72"/><path d="M22 55 H{width-22}" stroke="{b}" opacity=".35"/>{txt(26,35,name,20,a,700)}{body}'
 if foot:content+=txt(26,height-18,foot,11,'#8896aa')
 return content+'</svg>'
def chibi(theme,x=720,y=78):
 # Deliberately small, recognizable vector mascot; no remote assets or copyrighted art.
 a,b,_,_=PALETTES[theme]
 headwear={'winter':'❄','spring':'✿','summer':'☀','autumn':'◆','halloween':'☾','christmas':'★','easter':'✿','birthday':'★'}[theme]
 return f'''<g transform="translate({x} {y})" aria-label="Chaty chibi mascot">
 <path d="M18 57 Q-5 86 16 102 L65 102 Q90 82 65 57" fill="{a}" stroke="#7f89a8" stroke-width="2"/>
 <path d="M14 43 Q-3 4 33 0 Q80 -3 72 47 L81 93 Q67 108 60 83 L18 83 Q5 104 0 89Z" fill="#348b70" stroke="#75d8b1" stroke-width="2"/>
 <ellipse cx="41" cy="44" rx="29" ry="31" fill="#f6d7cf"/>
 <path d="M12 31 Q18 -5 56 12 L75 36 Q52 23 45 16 Q29 38 12 31Z" fill="#348b70"/>
 <ellipse cx="29" cy="46" rx="5" ry="7" fill="#8565c9"/><ellipse cx="54" cy="46" rx="5" ry="7" fill="#8565c9"/>
 <circle cx="30" cy="43" r="2" fill="white"/><circle cx="55" cy="43" r="2" fill="white"/>
 <path d="M36 58 Q45 64 52 56" fill="none" stroke="#743f58" stroke-width="2" stroke-linecap="round"/>
 <path d="M19 79 L62 79 L70 102 L9 102Z" fill="{b}"/>
 <path d="M20 80 L40 94 L62 80" fill="none" stroke="#e9e4f9" stroke-width="3"/>
 <circle cx="42" cy="7" r="12" fill="{a}"/><text x="42" y="12" font-size="14" text-anchor="middle" fill="#0d1117">{headwear}</text>
 </g>'''
def bar(y,label,value,maxval,a,x=250,w=470):
 length=0 if not maxval else int(w*value/maxval)
 return txt(26,y+14,label,13)+f'<rect x="{x}" y="{y}" width="{w}" height="15" rx="7" fill="#253149"/><rect x="{x}" y="{y}" width="{length}" height="15" rx="7" fill="{a}"/>'+txt(x+w+12,y+13,value,12)
def contribution_calendar(api,day):
 """Fetch one-year contribution counts with GraphQL; may include private count only when authorized."""
 if not api.token:
  api.errors.append('GraphQL contribution calendar: no token supplied; configure GH_STATS_TOKEN')
  return {}
 start=(day-dt.timedelta(days=365)).isoformat()+"T00:00:00Z"
 end=(day+dt.timedelta(days=1)).isoformat()+"T00:00:00Z"
 query='query($login:String!,$from:DateTime!,$to:DateTime!){user(login:$login){contributionsCollection(from:$from,to:$to){contributionCalendar{weeks{contributionDays{date contributionCount}}}}}}'
 payload=json.dumps({'query':query,'variables':{'login':USER,'from':start,'to':end}}).encode()
 req=urllib.request.Request('https://api.github.com/graphql',data=payload,headers={'Authorization':'Bearer '+api.token,'Content-Type':'application/json','User-Agent':'profile-developer-cards'})
 try:
  with urllib.request.urlopen(req,timeout=20) as res: data=json.load(res)
  if data.get('errors'):
   raise ValueError('GitHub GraphQL: '+ '; '.join(str(e.get('message','unknown')) for e in data['errors'])[:300])
  if not data.get('data',{}).get('user'):
   raise ValueError('GitHub GraphQL returned no user data (check token permissions and PROFILE_USER)')
  weeks=data['data']['user']['contributionsCollection']['contributionCalendar']['weeks']
  result={d['date']:d['contributionCount'] for w in weeks for d in w['contributionDays']}
  if not result:api.errors.append('GraphQL returned empty calendar')
  return result
 except Exception as exc:api.errors.append('GraphQL contribution calendar: '+str(exc));return {}

def streak_stats(calendar,day):
 if not calendar:return None
 active={dt.date.fromisoformat(d) for d,c in calendar.items() if c>0}
 cursor=day if day in active else day-dt.timedelta(days=1)
 current=0
 while cursor in active:current+=1;cursor-=dt.timedelta(days=1)
 longest=0;run=0
 for d in sorted(dt.date.fromisoformat(x) for x in calendar):
  run=run+1 if d in active else 0;longest=max(longest,run)
 return current,longest,sum(calendar.values())

def load_data(api):
 repos=[r for r in api.pages(f'users/{USER}/repos?type=owner&sort=pushed',5) if not r.get('fork') and not r.get('archived')]
 events=api.pages(f'users/{USER}/events/public',3) # GitHub events are a limited recent window, NOT complete history
 pushes=[]
 for e in events:
  if e.get('type')=='PushEvent':
   date=e.get('created_at','')[:10];count=e.get('payload',{}).get('size')
   if count is None:count=len(e.get('payload',{}).get('commits',[]))
   pushes.append((date,int(count or 0),e.get('repo',{}).get('name','')))
 languages=collections.Counter()
 for r in repos[:35]:
  if r.get('name')==USER:continue
  langs=api.get(f'repos/{USER}/{r["name"]}/languages')
  if isinstance(langs,dict):languages.update({k:v for k,v in langs.items() if isinstance(v,int)})
 workflows=api.get(f'repos/{USER}/{USER}/actions/runs?per_page=100')
 runs=workflows.get('workflow_runs',[]) if isinstance(workflows,dict) else []
 return repos,pushes,languages,runs

def compact_card(name,theme,body,foot='',width=520,height=214):
 a,b,_,_=PALETTES[theme]
 return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{esc(name)}">'
  f'<rect width="{width}" height="{height}" rx="15" fill="#0d1117"/><rect x="1.5" y="1.5" width="{width-3}" height="{height-3}" rx="14" fill="none" stroke="{a}" stroke-width="2" opacity=".8"/>'
  f'<path d="M18 50H{width-18}" stroke="{b}" opacity=".4"/>' +txt(19,34,name,20,a,700)+body+(txt(19,height-12,foot,10,'#9aa8be') if foot else '')+'</svg>')

def mascot_image(theme,x,y,w=178,h=116,variant='normal'):
 # Self-contained image: no external hosting or requests, survives GitHub image proxy.
 asset=OUT/'chaty'/((theme if variant=='normal' else variant)+'.png')
 if variant!='normal' and not asset.exists():asset=OUT/'chaty'/(theme+'.png')
 if not asset.exists():asset=OUT/'chaty.png'
 if not asset.exists():return ''
 encoded=base64.b64encode(asset.read_bytes()).decode('ascii')
 return f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="data:image/png;base64,{encoded}" preserveAspectRatio="xMidYMid meet"/>'

def choose_variant(day,force=None):
 """One deterministic draw per Paris calendar day; no random changes on reruns."""
 if force:
  if force not in VARIANTS:raise ValueError('Unknown variant')
  return force
 roll=int.from_bytes(hashlib.sha256(('chaty-v9:'+day.isoformat()).encode()).digest()[:8],'big')%100
 if roll<2:return 'strike'
 if roll<10:return 'cheapy'
 if day.weekday()>=5:return 'sleepy'
 return 'normal'

def quote_for(theme,day,variant,streak=None):
 pool=LINES[theme] if variant=='normal' else VARIANT_LINES[variant]
 quote=random.Random(day.isoformat()+theme+variant).choice(pool)
 if variant=='normal':
  if streak and streak[0] in (7,30,100,365):quote='A new streak milestone? Impressive.'
  elif int(hashlib.sha256((day.isoformat()+theme).encode()).hexdigest(),16)%41==0:quote='If anyone asks, I was never here.'
 return quote

def generate(theme,day,repos,pushes,languages,runs,errors,calendar=None, previous_pushes=None, releases=None, snapshot_note=None, variant='normal', last_checked=None):
 a,b,_,_=PALETTES[theme]; d30=day-dt.timedelta(days=30);d7=day-dt.timedelta(days=7)
 recent=[p for p in pushes if p[0]>=d7.isoformat()]
 days=len({p[0] for p in recent});recent30=[p for p in pushes if p[0]>=d30.isoformat()]
 total=sum(p[1] for p in recent30);updated=[r for r in repos if (r.get('pushed_at') or '')[:10]>=d30.isoformat()]
 # Contextual reactions override the daily line only when the event is verifiable.
 streak=streak_stats(calendar or {},day)
 quote=quote_for(theme,day,variant,streak)
 # Streak banner: contribution heatmap and one seasonal Chaty with quote beneath her.
 body=''
 if streak:
  current,longest,year_total=streak
  body+=txt(26,105,str(current),38,a,700)+txt(104,101,'CURRENT STREAK',12)
  body+=txt(26,144,f'{longest} days · longest',14,b)
  body+=txt(26,177,f'{year_total} contributions (365d)',13,'#d1d5e3')
  # GitHub calendar includes Sunday-to-Saturday weeks; 52 columns fit the middle panel.
  first=day-dt.timedelta(days=364)
  first-=dt.timedelta(days=(first.weekday()+1)%7)
  counts=[int(v) for v in (calendar or {}).values()]
  ceiling=max(1,sorted(counts)[int(.90*(len(counts)-1))]) if counts else 1
  for week in range(53):
   for weekday in range(7):
    date=first+dt.timedelta(days=week*7+weekday)
    if date>day:continue
    value=(calendar or {}).get(date.isoformat(),0)
    opacity=0.16 if not value else .3+.7*min(1,value/ceiling)
    body+=f'<rect x="{214+week*7.3:.1f}" y="{75+weekday*13}" width="5.9" height="10" rx="1.5" fill="{a}" opacity="{opacity:.2f}"/>'
  body+=txt(214,187,'Last 365 days · contributions',11,'#94a3b8')
 else:
  body+=txt(26,109,'Streak data unavailable',22,a,700)
  body+=txt(26,145,'GitHub GraphQL data required',14,'#bac4d4')
 if snapshot_note:body+=txt(26,218,snapshot_note[:72],11,'#f3b56e')
 body+=mascot_image(theme,632,49,171,109,variant)
 # Keep the dialogue directly below the character, inside her own column.
 import textwrap
 quote_lines=textwrap.wrap(quote,width=27,break_long_words=False)[:2]
 for i,line in enumerate(quote_lines):body+=txt(718,181+i*17,'“'+line+'”' if len(quote_lines)==1 else line,12,b,400,'middle')
 body+=txt(718,226,'— '+('Cheapy' if variant in ('cheapy','strike') else 'Mini-Chaty')+' ♡',11,'#a8b3ca',400,'middle')
 (OUT/'streak.svg').write_text(card('GITHUB STREAK',theme,body,820,245),encoding='utf-8')
 # All six cards use the same dimensions so they can sit side by side.
 body=txt(22,90,str(days),31,a,700)+txt(83,88,'active push days (7d)',14)
 body+=txt(22,132,str(total),29,b,700)+txt(94,130,'commits in recent public events (30d)',12)
 body+=txt(22,172,f'{len(updated)} repositories updated (30d)',15)
 # Compare two complete 30-day windows only if an actual events sample spans both.
 older_start=(day-dt.timedelta(days=60)).isoformat()
 older=[p for p in pushes if older_start<=p[0]<d30.isoformat()]
 if pushes and min(p[0] for p in pushes)<=older_start and older:
  prior=sum(p[1] for p in older)
  comparison='vs previous 30d: '+('+' if total>=prior else '')+str(total-prior)+' commits'
  body+=txt(300,174,comparison,11,b)

 (OUT/'pulse.svg').write_text(compact_card('DEVELOPER PULSE',theme,body,'Public events: limited recent history'),encoding='utf-8')
 top=languages.most_common(5);body='';grand=sum(languages.values()) or 1
 for i,(lang,val) in enumerate(top):
  y=65+i*27;body+=txt(20,y+13,lang[:16],13)
  body+=f'<rect x="170" y="{y}" width="245" height="14" rx="7" fill="#243047"/>'
  body+=f'<rect x="170" y="{y}" width="{245*val/grand:.1f}" height="14" rx="7" fill="{a}"/>'
  body+=txt(425,y+12,f'{100*val/grand:.1f}%',12,b)
 if not top:body+=txt(22,110,'Language data unavailable (offline preview).',15)
 (OUT/'languages.svg').write_text(compact_card('LANGUAGE DNA',theme,body,'Code bytes in up to 35 public repos'),encoding='utf-8')
 stars=sum(int(r.get('stargazers_count',0)) for r in repos)
 xp=len(repos)*20+stars*10+len(updated)*5;level=1+xp//200;progress=xp%200
 body=txt(22,101,f'Lv. {level}',42,a,700)+txt(210,96,f'{xp} XP',22,b,700)
 body+=f'<rect x="22" y="121" width="474" height="16" rx="8" fill="#243047"/><rect x="22" y="121" width="{474*progress/200:.1f}" height="16" rx="8" fill="{a}"/>'
 body+=txt(22,170,'20 XP / repo  ·  10 XP / star  ·  5 XP / active repo',12)
 (OUT/'rpg.svg').write_text(compact_card('DEVELOPER RPG',theme,body,'Fun progression, not a skill rating'),encoding='utf-8')
 body=''
 for i,r in enumerate(sorted(repos,key=lambda r:r.get('pushed_at') or '',reverse=True)[:4]):
  y=76+i*31;body+=txt(22,y,r.get('name','repo')[:29],14,a,600)+txt(375,y,(r.get('pushed_at') or '')[:10],12,'#b9c5d7')
 if releases:
  first=next((r for r in sorted(repos,key=lambda r:r.get('pushed_at') or '',reverse=True) if r.get('name') in releases),None)
  if first:body+=txt(22,202,'Latest release: '+first['name'][:20]+' · '+str(releases[first['name']])[:18],10,b)
 if not repos:body=txt(22,109,'No repository data available.',15)
 (OUT/'timeline.svg').write_text(compact_card('PROJECT TIMELINE',theme,body,'Recent pushes; not release dates'),encoding='utf-8')
 achievements=[('FIRST REPO',len(repos)>=1),('10 REPOS',len(repos)>=10),('25 REPOS',len(repos)>=25),('FIRST STAR',stars>=1),('10 STARS',stars>=10),('ACTIVE MONTH',bool(updated))]
 # Secret achievements require observable data; never award for unknown/private activity.
 secrets=[]
 if len([k for k,v in languages.items() if v>0])>=5:secrets.append('POLYGLOT')
 if streak and streak[0]>=30:secrets.append('UNSTOPPABLE')
 if len(repos)>=20:secrets.append('COLLECTOR')
 body=''
 for i,(label,unlocked) in enumerate(achievements):
  x=20+(i%3)*168;y=80+(i//3)*65
  body+=f'<rect x="{x}" y="{y-22}" width="157" height="47" rx="9" fill="{a if unlocked else "#263044"}" opacity="{.25 if unlocked else .6}"/>'
  body+=txt(x+9,y+5,('✓ ' if unlocked else '○ ')+label,12,a if unlocked else '#b1bbca',600)
 (OUT/'achievements.svg').write_text(compact_card('ACHIEVEMENT CABINET',theme,body,'Secrets: '+(', '.join(secrets) if secrets else 'not unlocked yet')),encoding='utf-8')
 completed=[r for r in runs if r.get('status')=='completed'];success=sum(r.get('conclusion')=='success' for r in completed)
 durations=[]
 for r in completed:
  try:
   start=dt.datetime.fromisoformat(r['run_started_at'].replace('Z','+00:00'))
   end=dt.datetime.fromisoformat(r['updated_at'].replace('Z','+00:00'))
   delta=(end-start).total_seconds()
   if 0<=delta<=86400:durations.append(delta)
  except (KeyError,ValueError,TypeError):pass
 failure=sum(r.get('conclusion')=='failure' for r in completed);rate=round(100*success/len(completed)) if completed else None
 body=txt(22,99,f'{rate}%' if rate is not None else 'N/A',37,a,700)+txt(173,94,'successful runs',16)
 body+=txt(22,145,f'✓ {success} succeeded     ✕ {failure} failed',16,b)
 body+=txt(22,179,f'{len(completed)} completed runs sampled',13)
 if durations:body+=txt(315,179,f'Avg {round(statistics.mean(durations))}s',12,b)
 if completed:body+=txt(315,145,'Latest: '+str(completed[0].get('conclusion') or 'unknown')[:12],12)
 (OUT/'automation.svg').write_text(compact_card('AUTOMATION HEALTH',theme,body,'Up to 100 recent workflow runs'),encoding='utf-8')
 meta={'generated_at':dt.datetime.now(dt.timezone.utc).isoformat(),'theme':theme,'public_repos':len(repos),'sampled_public_events':len(pushes),'api_errors':errors,'variant':variant,'data_last_checked_at':last_checked}
 (OUT/'data.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')

def cache_read():
 try:
  data=json.loads(CACHE.read_text(encoding='utf-8'))
  if data.get('schema')==1 and data.get('user')==USER:return data
 except (OSError,ValueError,TypeError):pass
 return {}

def atomic_json(path,obj):
 path.parent.mkdir(parents=True,exist_ok=True)
 with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',dir=path.parent,delete=False,suffix='.tmp') as handle:
  json.dump(obj,handle,ensure_ascii=False,indent=2)
  tmp=Path(handle.name)
 os.replace(tmp,path)

def validate_cards():
 import xml.etree.ElementTree as ET
 for name in CARDS:
  path=OUT/(name+'.svg')
  if not path.exists() or path.stat().st_size<250:raise RuntimeError('Missing or empty card: '+str(path))
  ET.parse(path)

def main():
 p=argparse.ArgumentParser()
 p.add_argument('--theme',choices=THEMES)
 p.add_argument('--offline',action='store_true',help='Generate preview only if --allow-preview-overwrite is also set')
 p.add_argument('--allow-preview-overwrite',action='store_true',help='Explicitly overwrite cards with offline preview placeholders')
 p.add_argument('--date')
 p.add_argument('--force-variant',choices=VARIANTS,help='Preview only; never set this in the scheduled workflow')
 p.add_argument('--self-test',action='store_true')
 args=p.parse_args()
 if args.self_test:
  import xml.etree.ElementTree as ET
  assert theme_for(dt.date(2026,1,9))=='birthday'
  assert streak_stats({'2026-11-04':2,'2026-11-05':1},dt.date(2026,11,6))==(2,2,3)
  for path in OUT.glob('*.svg'):ET.parse(path)
  print('Self-test passed; existing SVGs parse successfully.')
  return
 try:day=dt.date.fromisoformat(args.date) if args.date else dt.datetime.now(ZoneInfo('Europe/Paris')).date()
 except ZoneInfoNotFoundError:
  day=dt.datetime.now(dt.timezone.utc).date()
  print('Warning: timezone data missing; using UTC date (install tzdata for Europe/Paris)')
 theme=args.theme or theme_for(day);variant=choose_variant(day,args.force_variant);OUT.mkdir(parents=True,exist_ok=True)
 if args.offline and not args.allow_preview_overwrite:
  print('SAFE MODE: offline preview will NOT overwrite existing cards.')
  print('For deliberate preview generation, add --allow-preview-overwrite on a test branch.')
  return
 if args.offline:
  repos=[];pushes=[];langs=collections.Counter();runs=[];errors=['Offline preview: placeholders'];calendar={}
 else:
  api=API();cache=cache_read()
  repos,pushes,langs,runs=load_data(api)
  calendar=contribution_calendar(api,day);errors=api.errors
  # Never replace real, previously valid data with API failures or empty placeholders.
  fresh={'repos':repos,'pushes':pushes,'languages':dict(langs),'runs':runs,'calendar':calendar}
  # A legitimate empty response can be accepted for pushes/runs, but not for the core
  # profile/repository/calendar data without corroboration.
  healthy_repos=isinstance(repos,list) and bool(repos) and not any('users/'+USER+'/repos' in e for e in errors)
  healthy_calendar=bool(calendar) and not any('GraphQL contribution calendar' in e for e in errors)
  if not healthy_repos: fresh['repos']=[]
  if not healthy_calendar: fresh['calendar']={}
  if any('users/'+USER+'/events/public' in e for e in errors):fresh['pushes']=[]
  if any('/languages' in e for e in errors):fresh['languages']={}
  if any('/actions/runs' in e for e in errors):fresh['runs']=[]
  if not healthy_repos and not cache.get('repos'):
   print('ERROR: No repository data; retaining previously generated SVGs.');sys.exit(2)
  if not healthy_calendar and not cache.get('calendar'):
   print('WARNING: Contribution calendar unavailable; preserving other valid statistics and marking streak unavailable.')
   for err in errors:
    if 'GraphQL' in err: print('  '+err)

  for key in ('repos','pushes','languages','runs','calendar'):
   if not fresh[key] and cache.get(key):
    fresh[key]=cache[key]
    print('Using cached '+key+' (last valid snapshot)')
  repos=fresh['repos'];pushes=fresh['pushes'];langs=collections.Counter(fresh['languages']);runs=fresh['runs'];calendar=fresh['calendar']
  # Persist the effective fallback values, never overwrite the cache with failed responses.
  # An empty but successful events response is allowed, while failed requests retain prior values.
  snapshot={'schema':1,'user':USER,'last_checked_at':dt.datetime.now(dt.timezone.utc).isoformat(),
   'last_fresh_repos_at':dt.datetime.now(dt.timezone.utc).isoformat() if healthy_repos else cache.get('last_fresh_repos_at'),
   'last_fresh_calendar_at':dt.datetime.now(dt.timezone.utc).isoformat() if healthy_calendar else cache.get('last_fresh_calendar_at'),**fresh}
  atomic_json(CACHE,snapshot)
 snapshot_note=None
 if not args.offline and (not healthy_repos or not healthy_calendar):
  stamp=cache.get('last_fresh_calendar_at','unknown')[:10]
  snapshot_note='Cached GitHub data · last verified '+stamp
 generate(theme,day,repos,pushes,langs,runs,errors,calendar,snapshot_note=snapshot_note,variant=variant,last_checked=None if args.offline else cache.get('last_fresh_calendar_at'))
 validate_cards()
 print(f'Generated and validated 7 local SVG cards ({theme}, {variant}); API warnings: {len(errors)}')
 for error in errors[:8]:print('  Warning:',error)
if __name__=='__main__':main()
