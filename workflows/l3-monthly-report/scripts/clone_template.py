#!/usr/bin/env python3
import argparse, shutil
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('template')
p.add_argument('output')
a = p.parse_args()
src, dst = Path(a.template), Path(a.output)
if not src.exists():
    raise SystemExit(f'Template not found: {src}')
dst.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(src, dst)
print(dst)
