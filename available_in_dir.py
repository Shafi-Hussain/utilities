import os

from packaging.tags import sys_tags
from packaging.utils import parse_wheel_filename, canonicalize_name
from packaging.version import Version

stags = list(sys_tags())
available_wheels = [parse_wheel_filename(file) for file in os.listdir() if file.endswith(".whl")]

with open('req.txt', 'r') as f:
    lines = [i.split('==') for i in f.read().split("\n") if i]
    for x, y in lines:
        a, b = canonicalize_name(x), Version(y)
        for whl_name, whl_ver, bld_tags, whl_tags in available_wheels:
            if a == whl_name and b == whl_ver and any(t1 == t2 for t1 in whl_tags for t2 in stags):
                print(f"{x}=={y} | WHEEL |")
                break
        else:
            print(f"{x}=={y} | NOT FOUND |")
