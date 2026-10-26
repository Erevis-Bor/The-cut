#!/usr/bin/env python3
"""Generate a timestamped UK streaming snapshot for The Cut.

Requires TMDB_READ_TOKEN (Bearer token) or TMDB_API_KEY (v3 key). No credentials
are ever included in the generated snapshot, web app, or commit history.

Uses only country='GB' flatrate/subscription offers as INCLUDED, not rent/buy.
TV provider availability is series-level; specific seasons may differ.
"""
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TOKEN=os.getenv('TMDB_READ_TOKEN')
API_KEY=os.getenv('TMDB_API_KEY')
if not (TOKEN or API_KEY):
    sys.exit('Missing TMDB_READ_TOKEN or TMDB_API_KEY. Add a GitHub Actions repository secret, or set it locally.')

raw=(ROOT/'data.js').read_text(encoding='utf-8')
start=raw.index('window.CUT_CATALOGUE=')+len('window.CUT_CATALOGUE=')
catalogue, _ = json.JSONDecoder().raw_decode(raw[start:].lstrip())
existing={}
metadata_path=ROOT/'metadata.js'
if metadata_path.exists():
    old=metadata_path.read_text(encoding='utf-8')
    try:
        existing=json.loads(old[old.index('window.CUT_METADATA=')+len('window.CUT_METADATA='):].rstrip(';\n'))['items']
    except (ValueError,KeyError):
        existing={}

PROVIDER_IDS={
  'Netflix': {8,175,1796},
  'Prime Video': {9,119,2100},
  'Disney+': {122,337},
  'NOW': {39,591},
  'BBC iPlayer': {38},
  'Apple TV': {350}, # Apple subscription. ID 2 is the Apple TV Store and is excluded.
}
# Provider ids may evolve; names are only a fallback for non-ambiguous services.
NAME_FALLBACK={
  'Netflix': {'Netflix','Netflix Standard with Ads'},
  'Prime Video': {'Amazon Prime Video','Amazon Prime Video with Ads'},
  'Disney+': {'Disney Plus','Disney+'},
  'NOW': {'Now TV','Now TV Cinema'},
  'BBC iPlayer': {'BBC iPlayer'},
  'Apple TV': set(), # Apple TV is overloaded; require the verified subscription provider ID.
}

def norm(v):return re.sub('[^a-z0-9]+','',v.casefold())

def api(path,query=None):
    params=dict(query or {})
    if not TOKEN:params['api_key']=API_KEY
    url='https://api.themoviedb.org/3/'+path+'?'+urllib.parse.urlencode(params)
    headers={'Accept':'application/json','User-Agent':'TheCutPersonalWatchlist/4.0'}
    if TOKEN:headers['Authorization']='Bearer '+TOKEN
    last=None
    for attempt in range(4):
        try:
            req=urllib.request.Request(url,headers=headers)
            with urllib.request.urlopen(req,timeout=25) as r:return json.load(r)
        except urllib.error.HTTPError as e:
            last=e
            if e.code not in (429,500,502,503,504):raise
        except (TimeoutError,urllib.error.URLError) as e:last=e
        time.sleep(2**attempt)
    raise last

def match_item(p):
    media='movie' if p['type']=='film' else 'tv'
    result=api('search/'+media,{'query':p['title'],'language':'en-GB','page':1,'include_adult':'false'})
    candidates=[]
    for item in result.get('results',[]):
        name=item.get('title') if media=='movie' else item.get('name')
        original=item.get('original_title') if media=='movie' else item.get('original_name')
        release=(item.get('release_date') or item.get('first_air_date') or '')[:4]
        year=int(release) if release.isdigit() else None
        exact=norm(p['title']) in (norm(name or ''),norm(original or ''))
        near=year is not None and abs(p['year']-year)<=1
        if exact and near:candidates.append((abs(p['year']-year),-float(item.get('popularity') or 0),item))
    if not candidates:return None
    return sorted(candidates)[0][2]

def classification(entry):
    uk=entry.get('results',{}).get('GB')
    if not uk:return {'ukData':False,'included':[],'possibleNow':False,'rentalOnly':False,'rentOrBuy':False}
    options=uk.get('flatrate',[])
    plans=[d.get('provider_name','') for d in options]
    ids={x.get('provider_id') for x in options}
    included=[]
    for service, valid_ids in PROVIDER_IDS.items():
        matched=bool(ids & valid_ids) or any(norm(n) in {norm(x) for x in NAME_FALLBACK[service]} for n in plans)
        if matched and service!='NOW': included.append(service)
    # NOW Cinema vs Entertainment memberships cannot be inferred from 'NOW' alone.
    possible_now=bool(ids & PROVIDER_IDS['NOW']) or any(norm(n) in {norm(x) for x in NAME_FALLBACK['NOW']} for n in plans)
    rent=bool(uk.get('rent') or uk.get('buy'))
    return {'ukData':True,'included':included,'possibleNow':possible_now,'rentalOnly':bool(rent and not options),'rentOrBuy':rent,
            'ukFlatrate':plans,'watchPage':uk.get('link','')}

out={}
for i,p in enumerate(catalogue,1):
    try:
        match=match_item(p)
        if not match:
            if p['id'] in existing:out[p['id']]=existing[p['id']]
            print(f'{i}/{len(catalogue)}: unmatched {p["title"]}')
            continue
        media='movie' if p['type']=='film' else 'tv'
        available=api(f'{media}/{match["id"]}/watch/providers')
        out[p['id']]={'checked':True,'tmdbId':match['id'],'posterPath':match.get('poster_path'),
                      **classification(available)}
        if i%25==0:print(f'{i}/{len(catalogue)} checked',flush=True)
        time.sleep(0.12)
    except Exception as exc:
        print(f'Warning {i} {p["title"]}: {exc}',file=sys.stderr)
        if p['id'] in existing:out[p['id']]=existing[p['id']]
        time.sleep(1)

snapshot={'updatedAt':dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'),
 'source':'TMDB watch providers, powered by JustWatch','region':'GB','items':out}
metadata_path.write_text('/* Generated UK streaming and poster snapshot. TMDB + JustWatch attribution required. */\nwindow.CUT_METADATA='+json.dumps(snapshot,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
print('Wrote',len(out),'matched out of',len(catalogue),'to',metadata_path)
