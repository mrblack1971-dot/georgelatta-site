#!/usr/bin/env python3
"""Builds travels/index.html, one page per trip, and the homepage Travel Journal cards from travels/trips.json."""
import json,os,re
R=os.path.dirname(os.path.abspath(__file__))
def pic(t,pre,alt=None,cls=''):
    if not t: return f'<div class="tp-ph {cls}" aria-hidden="true">Photo coming soon</div>'
    return f'<img class="{cls}" src="{pre}images/{t}-sm.webp" srcset="{pre}images/{t}-sm.webp 500w, {pre}images/{t}.webp 1000w" sizes="(max-width:700px) 100vw, 33vw" alt="{alt or ""}" loading="lazy" decoding="async">'
def card(t,pre,link):
    d='<span class="draft-tag">Draft</span>' if t.get('draft') else ''
    return f'<article class="trip"{" data-status=\"DRAFT\"" if t.get("draft") else ""}><a href="{link}">{pic(t["image"],pre,t["alt"])}<div class="trip-body"><p class="trip-date">{t["date"]} {d}</p><h3>{t["title"]}</h3>{"<p class=\"trip-place\">"+t["place"]+"</p>" if t.get("place") else ""}<p>{t["teaser"]}</p><span class="more">Read more &rarr;</span></div></a></article>'
def page(title,pre,body,desc):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | George Latta</title><meta name="description" content="{desc}"><meta name="theme-color" content="#14213d">
<link rel="stylesheet" href="{pre}styles.css"></head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="nav"><a class="brand" href="{pre}index.html">George <span>Latta</span></a>
<nav aria-label="Main"><a href="{pre}index.html#about">About</a><a href="{pre}index.html#backroads">Backroads</a><a href="{pre}travels/">Travel Journal</a><a href="{pre}traveling-man/">Traveling Man</a><a href="{pre}index.html#contact">Contact</a></nav></header>
<main id="main">{body}</main>
<footer><p>&copy; 2026 George Latta &middot; Laurens, South Carolina</p></footer></body></html>
'''
def build(D,F,H,K,INTRO,M):
    trips=sorted(json.load(open(f'{R}/{D}/{F}')),key=lambda t:t['sort'],reverse=True)
    cards=''.join(card(t,'../',f'{t["slug"]}/') for t in trips)
    open(f'{R}/{D}/index.html','w').write(page(H,'../',f'<section class="wrap"><p class="kicker">{K}</p><h1 class="ph1">{H}</h1><p>{INTRO}</p><div class="trips">{cards}</div></section>',H+' | George Latta'))
    for t in trips:
        os.makedirs(f'{R}/{D}/{t["slug"]}',exist_ok=True)
        paras=''.join(b if b.startswith('<') else f'<p>{b}</p>' for b in t['body'])
        ph=''.join(f'<figure class="gi"><a href="../../images/{p}.webp">{pic(p,"../../",c)}</a><figcaption>{c}</figcaption></figure>' for p,c in t.get('photos',[]))
        hero=pic(t['image'],'../../',t['alt'],'trip-hero')
        d='<!-- STATUS: DRAFT stub, needs George\'s story -->' if t.get('draft') else ''
        body=f'{d}<article class="wrap trip-page"><p class="kicker"><a href="../">&larr; {H}</a></p><h1 class="ph1">{t["title"]}</h1><p class="trip-date">{t["date"]}{(" &middot; "+t["place"]) if t.get("place") else ""}</p>{hero}<div class="prose">{paras}</div>{"<div class=\"gallery\">"+ph+"</div>" if ph else ""}</article>'
        open(f'{R}/{D}/{t["slug"]}/index.html','w').write(page(t['title'],'../../',body,t['teaser']))
    home=open(f'{R}/index.html').read()
    block='<!--'+M+'-->'+''.join(card(t,'',f'{D}/{t["slug"]}/') for t in trips[:3])+'<!--/'+M+'-->'
    home=re.sub(r'<!--'+M+'-->.*?<!--/'+M+'-->',block,home,flags=re.S)
    open(f'{R}/index.html','w').write(home)
    print('built',len(trips),D)

build('travels','trips.json','Travel Journal','Backroads &amp; Memories','Places I&rsquo;ve seen and things I&rsquo;ve done along the way.','TRIPS')
build('traveling-man','visits.json','Traveling Man','Masonic travels','Visits to Grand Lodges and lodges around the country.','VISITS')
