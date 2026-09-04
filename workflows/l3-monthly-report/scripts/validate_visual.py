#!/usr/bin/env python3
import argparse,re,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('template');p.add_argument('generated');a=p.parse_args()
def read(x):return Path(x).read_text(encoding='utf-8').replace('\r\n','\n')
def block(t,tag):
    m=re.search(rf'<{tag}[^>]*>(.*?)</{tag}>',t,re.S|re.I);return m.group(1) if m else None
def ids(t):return re.findall(r'<section\b[^>]*\bid=["\']([^"\']+)["\']',t,re.I)
t=read(a.template);g=read(a.generated);e=[]
for tag in ('style','script'):
    if block(t,tag)!=block(g,tag):e.append(f'{tag} block differs from institutional template')
expected=['overview','trend','sessions','wrong','intervention','mock','habit','route','next']
if ids(g)!=expected:e.append(f'section order/ids differ: expected={expected} generated={ids(g)}')
for phrase in ('示例学生：','模拟数据，仅用于确认结构与呈现','Math英文条件理解是本月突出问题','9月阶段模拟测试</td><td>9/28</td><td>84 / 100'):
    if phrase in g:e.append(f'demo residue detected: {phrase}')
if e:
    print('FAIL');[print('-',x) for x in e];sys.exit(1)
print('PASS')
