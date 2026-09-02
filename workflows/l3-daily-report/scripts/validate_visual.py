#!/usr/bin/env python3
import argparse, re, sys
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('template')
p.add_argument('generated')
a = p.parse_args()

def read(path):
    return Path(path).read_text(encoding='utf-8').replace('\r\n','\n')

def block(text, tag):
    m = re.search(rf'<{tag}[^>]*>(.*?)</{tag}>', text, re.S|re.I)
    return m.group(1) if m else None

def section_ids(text):
    return re.findall(r'<section\b[^>]*\bid=["\']([^"\']+)["\']', text, re.I)

t = read(a.template)
g = read(a.generated)
errors=[]
for tag in ('style','script'):
    tb, gb = block(t, tag), block(g, tag)
    if tb != gb:
        errors.append(f'{tag} block differs from institutional template')
if section_ids(t) != section_ids(g):
    errors.append(f'section order/ids differ: template={section_ids(t)} generated={section_ids(g)}')
for forbidden in (r'object-fit\s*:\s*cover', r'max-height\s*:', r'<style[^>]*>.*?<style'):
    if re.search(forbidden, g, re.S|re.I):
        errors.append(f'forbidden visual pattern detected: {forbidden}')
if errors:
    print('FAIL')
    for e in errors: print('-', e)
    sys.exit(1)
print('PASS')
