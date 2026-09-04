#!/usr/bin/env python3
import argparse,re,sys
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('template'); p.add_argument('generated'); p.add_argument('--report-type',choices=['l2','l3']); a=p.parse_args()
def read(x): return Path(x).read_text(encoding='utf-8').replace('\r\n','\n')
def block(t,tag):
    m=re.search(rf'<{tag}[^>]*>(.*?)</{tag}>',t,re.S|re.I); return m.group(1) if m else None
def ids(t): return re.findall(r'<section\b[^>]*\bid=["\']([^"\']+)["\']',t,re.I)
t=read(a.template); g=read(a.generated); e=[]
for tag in ('style','script'):
    if block(t,tag)!=block(g,tag): e.append(f'{tag} block differs from institutional template')
rt=a.report_type or ('l3' if 'L3 学业管理周看板' in g else 'l2')
expected=['overview','daily','subject','ongoing','sessions','wrong','analysis','habit'] if rt=='l3' else ['overview','daily','subject','ongoing','wrong','habit']
if ids(g)!=expected: e.append(f'section order/ids differ: expected={expected} generated={ids(g)}')
for phrase in ('示例学生：','模拟数据，仅用于确认结构与呈现','Math P12；English Grammar；Chinese Reading','Science Project按学校节点下周继续'):
    if phrase in g: e.append(f'demo residue detected: {phrase}')
body=re.sub(r'<style[^>]*>.*?</style>','',g,flags=re.S|re.I)
for f in (r'object-fit\s*:\s*cover',r'max-height\s*:'):
    if re.search(f,body,re.S|re.I): e.append(f'forbidden visual pattern outside locked style: {f}')
if e:
    print('FAIL'); [print('-',x) for x in e]; sys.exit(1)
print('PASS')
