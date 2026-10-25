#!/usr/bin/env python3
"""Polish pass: social/share meta, canonical URLs, icons, follow-along footer, share images, sitemap.
Run after build_travels.py (build_travels.py calls it automatically). Idempotent."""
import os,re,glob,html,datetime
from PIL import Image,ImageDraw,ImageFont,ImageOps
R=os.path.dirname(os.path.abspath(__file__))
SITE='https://georgelatta.com/'   # canonical domain (custom domain is live)
NAVY=(20,33,61);GOLD=(201,162,39);CREAM=(250,247,240)
F='/usr/share/fonts/truetype/sand-box/google/IBM Plex Serif/IBMPlexSerif-'
FB={'personal':('https://www.facebook.com/TheYellowTurtle','George Latta'),
    'masonic':('https://www.facebook.com/MasonicLifeGL','Masonic Life'),
    'backroads':('https://www.facebook.com/profile.php?id=61594585006391','Backroads &amp; Memories')}
ICON='<svg aria-hidden="true" focusable="false" viewBox="0 0 24 24" width="18" height="18"><path fill="currentColor" d="M14 8V6.3c0-.8.2-1.3 1.4-1.3H17V2.2c-.3 0-1.3-.2-2.4-.2-2.4 0-4 1.4-4 4.1V8H8v3h2.6v9H14v-9h2.7l.4-3z"/></svg>'
def fbtn(k,cls='fb'):
    u,n=FB[k];return f'<a class="{cls}" href="{u}" rel="noopener me" target="_blank">{ICON}<span>{n}<span class="sr"> on Facebook (opens in a new tab)</span></span></a>'
FOOT=('<footer><div class="follow"><p class="follow-h">Follow along on Facebook</p><div class="follow-row">'+''.join(fbtn(k) for k in FB)+
      '</div></div><p>&copy; 2026 George Latta &middot; Laurens, South Carolina</p></footer>')
def font(w,s):return ImageFont.truetype(F+w+'.ttf',s)
def wrap(d,t,f,maxw):
    out,line=[], ''
    for w in t.split():
        x=(line+' '+w).strip()
        if d.textlength(x,font=f)<=maxw: line=x
        else: out.append(line); line=w
    return out+[line]
def share(slug,title,kicker,img):
    W,H=1200,630;c=Image.new('RGB',(W,H),NAVY);d=ImageDraw.Draw(c)
    if img and os.path.exists(f'{R}/images/{img}.webp'):
        p=Image.open(f'{R}/images/{img}.webp').convert('RGB')
        pw=600;tall=p.height/p.width>1.3;p=ImageOps.fit(p,(pw,H),centering={'az-14-bell-rock-sedona-george':(0.85,0.4)}.get(img,(0.5,0.05 if tall else 0.4)));c.paste(p,(W-pw,0));d.rectangle([W-pw-6,0,W-pw,H],fill=GOLD);tw=W-pw-110
    else:
        tw=W-120;d.ellipse([W-330,H-330,W+90,H+90],outline=GOLD,width=6)
    d.rectangle([0,0,W,10],fill=GOLD)
    d.text((60,70),kicker.upper(),font=font('SemiBold',26),fill=GOLD)
    sz=64
    while True:
        f=font('Bold',sz);ls=wrap(d,title,f,tw)
        if len(ls)<=4 or sz<=40:break
        sz-=4
    y=130
    for l in ls[:4]: d.text((60,y),l,font=f,fill=(255,255,255)); y+=int(sz*1.2)
    d.text((60,H-100),'George Latta',font=font('Bold',34),fill=(255,255,255))
    d.text((60,H-58),'georgelatta.com',font=font('Regular',24),fill=(215,222,238))
    c.save(f'{R}/og/{slug}.jpg','JPEG',quality=84,optimize=True,progressive=True)
    return f'og/{slug}.jpg'
def icons():
    svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#14213d"/><rect x="4" y="4" width="56" height="56" rx="11" fill="none" stroke="#c9a227" stroke-width="2.5"/><text x="32" y="43" text-anchor="middle" font-family="Georgia,serif" font-weight="700" font-size="29" fill="#c9a227">GL</text></svg>'
    open(f'{R}/favicon.svg','w').write(svg)
    def png(s):
        c=Image.new('RGBA',(s,s),(0,0,0,0));d=ImageDraw.Draw(c);r=int(s*.22)
        d.rounded_rectangle([0,0,s-1,s-1],r,fill=NAVY)
        if s>=48:d.rounded_rectangle([s*.06,s*.06,s*.94,s*.94],int(s*.17),outline=GOLD,width=max(2,s//26))
        f=font('Bold',int(s*.48));d.text((s/2,s*.53),'GL',font=f,fill=GOLD,anchor='mm');return c
    png(180).convert('RGB').save(f'{R}/apple-touch-icon.png')
    png(32).save(f'{R}/favicon-32.png');png(192).save(f'{R}/icon-192.png');png(512).save(f'{R}/icon-512.png')
    png(48).save(f'{R}/favicon.ico',sizes=[(16,16),(32,32),(48,48)])
    open(f'{R}/site.webmanifest','w').write('{"name":"George Latta","short_name":"George Latta","icons":[{"src":"icon-192.png","sizes":"192x192","type":"image/png"},{"src":"icon-512.png","sizes":"512x512","type":"image/png"}],"theme_color":"#14213d","background_color":"#faf7f0","display":"browser"}\n')
def pages():
    out=[]
    for f in sorted(glob.glob(f'{R}/**/index.html',recursive=True))+[f'{R}/404.html']:
        rel=os.path.relpath(f,R)
        if rel.startswith(('new/','.')):continue
        out.append(rel)
    return out
def run():
    icons();urls=[]
    for rel in pages():
        p=f'{R}/{rel}';h=open(p).read()
        path='' if rel=='index.html' else rel[:-len('index.html')] if rel.endswith('index.html') else None
        depth=rel.count('/');pre='../'*depth
        if rel=='404.html':pre=''   # 404 uses a <base> tag set in its head
        title=html.unescape(re.search(r'<title>(.*?)</title>',h).group(1))
        desc=re.search(r'<meta name="description" content="(.*?)"',h).group(1)
        m=re.search(r'class="trip-hero" src="[^"]*images/([^"]+?)-sm\.webp',h) or re.search(r'<img[^>]*src="[^"]*images/([^"]+?)-sm\.webp',h)
        img=m.group(1) if m else None
        slug='home' if rel=='index.html' else 'default' if rel=='404.html' else path.strip('/').replace('/','--')
        short=re.sub(r'\s*\|\s*George Latta$','',title)
        kick={'travels':'Travel Journal','traveling-man':'Traveling Man'}.get(rel.split('/')[0],'Laurens, South Carolina') if '/' in rel else 'Laurens, South Carolina'
        if rel=='index.html':short='George Latta';kick='Life Coach · Leader · Retired'
        if rel=='404.html':short='Page not found';img=None
        ogi=SITE+share(slug,short,kick,img)
        can=SITE+(path or '') if path is not None else None
        meta=['<!--SEO-->']
        if can:meta.append(f'<link rel="canonical" href="{can}">')
        else:meta.append('<meta name="robots" content="noindex">')
        ot=html.escape(title,quote=True)
        meta+= [f'<meta property="og:type" content="{"website" if rel=="index.html" else "article"}">','<meta property="og:site_name" content="George Latta">','<meta property="og:locale" content="en_US">',
          f'<meta property="og:title" content="{ot}">',f'<meta property="og:description" content="{desc}">',
          *( [f'<meta property="og:url" content="{can}">'] if can else []),
          f'<meta property="og:image" content="{ogi}">','<meta property="og:image:width" content="1200">','<meta property="og:image:height" content="630">',
          f'<meta property="og:image:alt" content="{ot}">','<meta name="twitter:card" content="summary_large_image">',
          f'<meta name="twitter:title" content="{ot}">',f'<meta name="twitter:description" content="{desc}">',f'<meta name="twitter:image" content="{ogi}">',
          f'<link rel="icon" href="{pre}favicon.ico" sizes="any">',f'<link rel="icon" href="{pre}favicon.svg" type="image/svg+xml">',
          f'<link rel="apple-touch-icon" href="{pre}apple-touch-icon.png">',f'<link rel="manifest" href="{pre}site.webmanifest">','<!--/SEO-->']
        h=re.sub(r'<!--SEO-->.*?<!--/SEO-->','',h,flags=re.S)
        h=re.sub(r'<meta property="og:[^>]*>','',h)
        h=h.replace('<link rel="stylesheet"','\n'.join(meta)+'\n<link rel="stylesheet"',1)
        h=re.sub(r'<footer>.*?</footer>',FOOT,h,flags=re.S)
        h=re.sub(r'<!--FB:(\w+)-->.*?<!--/FB-->',lambda m:f'<!--FB:{m.group(1)}--><p class="fb-cta">{fbtn(m.group(1),"btn fbbtn")}</p><!--/FB-->',h,flags=re.S)
        open(p,'w').write(h)
        if can:urls.append(can)
    today=datetime.date.today().isoformat()
    open(f'{R}/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>\n' for u in urls)+'</urlset>\n')
    open(f'{R}/robots.txt','w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n')
    print('seo:',len(urls),'pages')
if __name__=='__main__':run()
