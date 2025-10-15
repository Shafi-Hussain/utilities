import os
import sys
from json import loads
from io import StringIO
from pathlib import Path

try:
    from lddwrap import list_dependencies, _output_json
except ModuleNotFoundError:
    print("Please install pylddwrap: 'python -m pip install pylddwrap'")
    exit(1)

FULL_LIB_PATH = int(os.getenv("FULL_LIB_PATH", "0").strip()) # 0 or 1
VENV = Path(os.path.dirname(os.path.dirname(sys.executable)))
stream = StringIO()

libs_needed = set()
for library in VENV.rglob("*.so"):
    # Note: try-block is needed as I noticed "debugpy" build amd64 .so files which fail with lddwrap on ppc64le
    try:
        deps = list_dependencies(path=library)
    except:
        print("FAILED:", library)
    _output_json(deps=deps, stream=stream)
    missing_libs = list(map(lambda dep: dep["soname"] if not FULL_LIB_PATH else f'{library}->{dep["soname"]}' , filter(lambda dep: not dep["found"], loads(stream.getvalue()))))
    #if missing_libs:
    #    print(library, list(set(missing_libs)))
    libs_needed.update(missing_libs)
    stream.seek(0)
    stream.truncate(0)

stream.close()
print("\n".join(sorted(libs_needed)))
