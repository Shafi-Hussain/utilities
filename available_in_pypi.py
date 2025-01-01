import requests
from bs4 import BeautifulSoup
from packaging.version import Version
from packaging.tags import sys_tags
from packaging.utils import parse_wheel_filename, parse_sdist_filename, canonicalize_name


def find_package(pkg, version, tags):
    r = requests.get(f'https://pypi.org/simple/{canonicalize_name(pkg)}/')
    s = BeautifulSoup(r.content, 'lxml')

    V = Version(version)

    for a in s.find_all('a'):
        txt = a.get_text(strip=True)
        if txt.endswith(".whl"):
            name, ver, bld_tag, pkg_tags = parse_wheel_filename(txt)
            if V == ver and any(t1 == t2 for t1 in tags for t2 in pkg_tags):
                # wheel available
                return 0, name, version

    for a in s.find_all('a'):
        txt = a.get_text(strip=True)
        if txt.endswith(".tar.gz") or txt.endswith(".tgz") or txt.endswith(".zip"):
            try:
                name, ver = parse_sdist_filename(txt)
                if V == ver:
                    # sdist available
                    return 1, name, version
            except Exception as _:
                pass
    return -1, pkg, version


stags = list(sys_tags())
with open('req.txt', 'r') as f:
    lines = [i.split('==') for i in f.read().split("\n") if i]
    # jobs = Parallel(n_jobs=-1)(delayed(find_package)(x, y, stags) for x, y in lines)
    for x, y in lines:
        a, b, c = find_package(x, y, stags)
        print(f"{b}=={c} | {'WHEEL' if a == 0 else 'TARBALL'} | {'******' if a == -1 else ''}")
