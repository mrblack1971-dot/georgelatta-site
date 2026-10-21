#!/usr/bin/env python3
"""Builds travels/index.html, one page per trip, and the homepage Travel Journal cards from travels/trips.json."""
import json,os,re
R=os.path.dirname(os.path.abspath(__file__))
trips=sorted(json.load(open(f'{R}/travels/trips.json')),key=lambda t:t['sort'],reverse=True)
def pic(t,pre,alt=None,cls=''):
    if not t: return f'<div class="tp-ph {cls}" aria-hidden="true">Photo coming soon</div>'
    return f'<img class="{cls}" src="{pre}images/{t}-sm.webp" srcset="{pre}images/{t}-sm.webp 500w, {pre}images/{t}.webp 1000w" sizes="(max-width:700px) 100vw, 33vw" alt="{alt or ""}" loading="lazy" decoding="async">'
def card(t,pre,link):
    d='<span class="draft-tag">Draft</span>' if t.get('draft') else ''
    return f'<article class="trip"{" data-status=\"DRAFT\"" if t.get("draft") else ""}><a href="{link}">{pic(t["image"],pre,t["alt"])}<div class="trip-body"><p class="trip-date">{t["date"]} {d}</p><h3>{t["title"]}</h3><p>{t["teaser"]}</p><span class="more">Read more &rarr;</span></div></a></article>'
def page(title,pre,body,desc):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | George Latta</title><meta name="description" content="{desc}"><meta name="theme-color" content="#14213d">
<link rel="stylesheet" href="{pre}styles.css"></head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="nav"><a class="brand" href="{pre}index.html">George <span>Latta</span></a>
<nav aria-label="Main"><a href="{pre}index.html#about">About</a><a href="{pre}index.html#backroads">Backroads</a><a href="{pre}travels/">Travel Journal</a><a href="{pre}index.html#contact">Contact</a></nav></header>
<main id="main">{body}</main>
<footer><p>&copy; 2026 George Latta &middot; Laurens, South Carolina</p></footer></body></html>
'''
cards=''.join(card(t,'../',f'{t["slug"]}/') for t in trips)
open(f'{R}/travels/index.html','w').write(page('Travel Journal','../',f'<section class="wrap"><p class="kicker">Backroads &amp; Memories</p><h1 class="ph1">Travel Journal</h1><p>Places I&rsquo;ve seen and things I&rsquo;ve done along the way.</p><div class="trips">{cards}</div></section>','Travel journal of George Latta: Backroads & Memories.'))
for t in trips:
    os.makedirs(f'{R}/travels/{t["slug"]}',exist_ok=True)
    paras=''.join(b if b.startswith('<!--') else f'<p>{b}</p>' for b in t['body'])
    ph=''.join(f'<figure class="gi"><a href="../../images/{p}.webp">{pic(p,"../../",c)}</a><figcaption>{c}</figcaption></figure>' for p,c in t.get('photos',[]))
    hero=pic(t['image'],'../../',t['alt'],'trip-hero')
    d='<!-- STATUS: DRAFT stub, needs George\'s story -->' if t.get('draft') else ''
    body=f'{d}<article class="wrap trip-page"><p class="kicker"><a href="../">&larr; Travel Journal</a></p><h1 class="ph1">{t["title"]}</h1><p class="trip-date">{t["date"]}</p>{hero}<div class="prose">{paras}</div>{"<div class=\"gallery\">"+ph+"</div>" if ph else ""}</article>'
    open(f'{R}/travels/{t["slug"]}/index.html','w').write(page(t['title'],'../../',body,t['teaser']))
home=open(f'{R}/index.html').read()
block='<!--TRIPS-->'+''.join(card(t,'',f'travels/{t["slug"]}/') for t in trips[:3])+'<!--/TRIPS-->'
home=re.sub(r'<!--TRIPS-->.*?<!--/TRIPS-->',block,home,flags=re.S)
open(f'{R}/index.html','w').write(home)
print('built',len(trips),'trips')
