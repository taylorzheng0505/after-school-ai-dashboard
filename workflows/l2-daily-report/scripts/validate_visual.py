#!/usr/bin/env python3
import argparse, re, sys
from pathlib import Path

p=argparse.ArgumentParser(); p.add_argument('template'); p.add_argument('generated'); a=p.parse_args()

def read(path): return Path(path).read_text(encoding='utf-8').replace('\r\n','\n')
def block(text,tag):
    m=re.search(rf'<{tag}[^>]*>(.*?)</{tag}>',text,re.S|re.I); return m.group(1) if m else None
def section_ids(text): return re.findall(r'<section\b[^>]*\bid=["\']([^"\']+)["\']',text,re.I)

t=read(a.template); g=read(a.generated); errors=[]
for tag in ('style','script'):
    if block(t,tag)!=block(g,tag): errors.append(f'{tag} block differs from institutional template')
name=Path(a.template).resolve().parts
is_l3=any('l3-daily-report' in x for x in name)
expected=['tasks','wrong','lesson','habit','note'] if is_l3 else ['tasks','wrong','habit','note']
if section_ids(g)!=expected: errors.append(f'section order/ids differ: expected={expected} generated={section_ids(g)}')
# These are forbidden only in generated dynamic image-specific inline/style additions. The locked style block is already equality-checked.
body_wo_style=re.sub(r'<style[^>]*>.*?</style>','',g,flags=re.S|re.I)
for forbidden in (r'object-fit\s*:\s*cover', r'max-height\s*:', r'<style[^>]*>.*?<style'):
    if re.search(forbidden,body_wo_style,re.S|re.I): errors.append(f'forbidden visual pattern detected outside locked style: {forbidden}')
if errors:
    print('FAIL'); [print('-',e) for e in errors]; sys.exit(1)
print('PASS')
