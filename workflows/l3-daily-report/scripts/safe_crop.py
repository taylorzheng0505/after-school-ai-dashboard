#!/usr/bin/env python3
"""Conservatively crop a worksheet question from a full-page image.

The caller supplies an approximate normalized bbox x1,y1,x2,y2 in [0,1].
The script expands vertically to nearby whitespace bands, uses the detected
page content width, then validates that ink does not touch top/bottom edges.
If a safe tight crop cannot be established, it emits a larger fallback crop.
"""
import argparse, json
from pathlib import Path
from PIL import Image, ImageOps

p=argparse.ArgumentParser()
p.add_argument('input')
p.add_argument('output')
p.add_argument('--bbox', required=True, help='normalized x1,y1,x2,y2')
p.add_argument('--max-expand', type=float, default=0.20, help='max vertical expansion fraction of page')
p.add_argument('--pad', type=float, default=0.012, help='final vertical padding fraction of page')
a=p.parse_args()

img=Image.open(a.input).convert('RGB')
W,H=img.size
try:
    x1,y1,x2,y2=[float(x.strip()) for x in a.bbox.split(',')]
except Exception:
    raise SystemExit('--bbox must be x1,y1,x2,y2 normalized floats')
if not (0 <= x1 < x2 <= 1 and 0 <= y1 < y2 <= 1):
    raise SystemExit('bbox values must satisfy 0<=x1<x2<=1 and 0<=y1<y2<=1')

# Analyze a downscaled grayscale image for speed.
aw=min(1200,W)
ah=max(1, round(H*aw/W))
g=ImageOps.grayscale(img.resize((aw,ah)))
pix=g.load()
# Dark threshold deliberately permissive: captures handwriting and printed text.
dark=210

# Detect page content width from columns containing ink.
col_counts=[]
for x in range(aw):
    c=0
    for y in range(ah):
        if pix[x,y] < dark: c+=1
    col_counts.append(c/ah)
active=[i for i,v in enumerate(col_counts) if v>0.002]
if active:
    cx1=max(0, active[0]-round(0.012*aw))
    cx2=min(aw-1, active[-1]+round(0.012*aw))
else:
    cx1,cx2=0,aw-1

# Row ink density across page content width.
width=max(1,cx2-cx1+1)
row=[]
for y in range(ah):
    c=0
    for x in range(cx1,cx2+1):
        if pix[x,y] < dark: c+=1
    row.append(c/width)
blank_thresh=0.003
blank=[v < blank_thresh for v in row]
min_blank=max(5, round(0.0025*ah))

def find_band_up(start, limit):
    run=0
    for y in range(start, limit-1, -1):
        run = run+1 if blank[y] else 0
        if run>=min_blank:
            # lower edge of blank band: content starts just below it
            return min(ah-1, y+run+1)
    return None

def find_band_down(start, limit):
    run=0
    for y in range(start, limit+1):
        run = run+1 if blank[y] else 0
        if run>=min_blank:
            # upper edge of blank band: content ends just above it
            return max(0, y-run)
    return None

ay1=max(0,min(ah-1,round(y1*ah)))
ay2=max(0,min(ah-1,round(y2*ah)))
maxe=round(a.max_expand*ah)
up=find_band_up(ay1, max(0,ay1-maxe))
dn=find_band_down(ay2, min(ah-1,ay2+maxe))
# If no blank band, keep a generous fallback margin.
if up is None: up=max(0, ay1-round(0.04*ah))
if dn is None: dn=min(ah-1, ay2+round(0.06*ah))

pad=round(a.pad*ah)
up=max(0,up-pad); dn=min(ah-1,dn+pad)

# Convert to original coordinates. Use detected content width plus margin.
ox1=max(0, round(cx1/aw*W)-round(0.01*W))
ox2=min(W, round((cx2+1)/aw*W)+round(0.01*W))
oy1=max(0, round(up/ah*H))
oy2=min(H, round((dn+1)/ah*H))

# Safety validator: ink near top/bottom of the proposed crop means it is risky.
def edge_density(box, frac=0.025):
    c=img.crop(box)
    gg=ImageOps.grayscale(c.resize((min(1000,c.width), max(1,round(c.height*min(1000,c.width)/c.width)))))
    ww,hh=gg.size; pp=gg.load(); band=max(2,round(frac*hh))
    def dens(ys):
        total=max(1,ww*len(ys)); d=0
        for yy in ys:
            for xx in range(ww):
                if pp[xx,yy] < dark: d+=1
        return d/total
    return dens(range(0,band)), dens(range(max(0,hh-band),hh))

status='PASS'
for _ in range(3):
    td,bd=edge_density((ox1,oy1,ox2,oy2))
    if td<=0.012 and bd<=0.012: break
    # Expand conservatively if content touches an edge.
    if td>0.012: oy1=max(0,oy1-round(0.035*H))
    if bd>0.012: oy2=min(H,oy2+round(0.05*H))
else:
    status='FALLBACK'

# Final sanity: never return a very shallow strip.
if oy2-oy1 < 0.05*H:
    cy=(oy1+oy2)//2
    half=round(0.04*H)
    oy1=max(0,cy-half); oy2=min(H,cy+half)
    status='FALLBACK'

out=img.crop((ox1,oy1,ox2,oy2))
Path(a.output).parent.mkdir(parents=True, exist_ok=True)
out.save(a.output)
print(json.dumps({
    'status':status,
    'output':str(Path(a.output)),
    'crop_box_px':[ox1,oy1,ox2,oy2],
    'page_size_px':[W,H],
    'rule':'prefer extra context over truncation'
}, ensure_ascii=False))
