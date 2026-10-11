import json
import os
import re
import sys

MAX_INDEX = 512 * 1024
MAX_PACKAGE = 4 * 1024 * 1024
MAX_IMAGE = 1024 * 1024
BUILT_IN = {
    "TINY-16", "BEN-16", "BYOC-16", "STACK-16", "CISC-16", "COPRO-16", "FIELD-16", "HARVARD-16", "IRQ-16", "MOVE-16",
    "RISC-16", "ROM-16", "BLAZE-16", "DSP-16", "FLIP-16", "GPU-16", "TURBO-16", "WORM-16",
}
VERSION = re.compile(r"^v?\d+\.\d+(\.\d+)?$")


def safe_path(path):
    if not isinstance(path, str) or not path or len(path) > 200:
        return False
    if path.startswith("/") or any(c in path for c in "\\:?#"):
        return False
    return all(part not in ("", ".", "..") for part in path.split("/"))


def strip_comments(text):
    return re.sub(r"^\s*//.*$", "", text, flags=re.M)


def check(root):
    problems = []
    index_path = os.path.join(root, "index.json")
    if os.path.getsize(index_path) > MAX_INDEX:
        return [f"index.json is larger than {MAX_INDEX // 1024} KB"]
    try:
        index = json.loads(strip_comments(open(index_path, encoding="utf-8").read()))
    except json.JSONDecodeError as e:
        return [f"index.json is not valid JSON: {e}"]
    machines = index.get("machines")
    if not isinstance(machines, list):
        return ['index.json needs a "machines" list']
    names = set()
    for number, machine in enumerate(machines, 1):
        where = f"machine {number}"
        if not isinstance(machine, dict):
            problems.append(f"{where} is not an object")
            continue
        name = machine.get("name")
        where = f"{where} ({name})" if name else where
        if not isinstance(name, str) or not name.strip():
            problems.append(f"{where} has no name")
            continue
        if name in names:
            problems.append(f"{where}: the name is used twice")
        names.add(name)
        if name in BUILT_IN:
            problems.append(f"{where}: {name} is the name of a machine built into ExµArch")
        tagline = machine.get("tagline")
        if tagline is not None and (not isinstance(tagline, str) or len(tagline) > 50):
            problems.append(f"{where}: the tagline must be text of at most 50 characters")
        version = machine.get("minVersion")
        if version is not None and not (isinstance(version, str) and VERSION.match(version)):
            problems.append(f"{where}: minVersion must look like 1.39.0")
        tags = machine.get("tags")
        if tags is not None and not (isinstance(tags, list) and all(isinstance(t, str) for t in tags)):
            problems.append(f"{where}: tags must be a list of words")
        problems += check_file(root, where, name, machine.get("file"))
        image = machine.get("image")
        if image is not None:
            problems += check_image(root, where, image)
    return problems


def check_file(root, where, name, file):
    if not safe_path(file):
        return [f"{where}: file must be a path inside this repository, such as machines/zed8.json"]
    path = os.path.join(root, file)
    if not os.path.isfile(path):
        return [f"{where}: {file} is missing"]
    if os.path.getsize(path) > MAX_PACKAGE:
        return [f"{where}: {file} is larger than {MAX_PACKAGE // (1024 * 1024)} MB"]
    try:
        package = json.loads(strip_comments(open(path, encoding="utf-8").read()))
    except json.JSONDecodeError as e:
        return [f"{where}: {file} is not valid JSON: {e}"]
    problems = []
    if not isinstance(package, dict) or not isinstance(package.get("machine"), dict):
        problems.append(f'{where}: {file} is not an ExµArch package: export it with Export, which writes a "machine"')
    elif package.get("name") != name:
        problems.append(f'{where}: {file} is named "{package.get("name")}", not "{name}"')
    return problems


def check_image(root, where, image):
    if not safe_path(image) or not image.lower().endswith(".png"):
        return [f"{where}: image must be a .png inside this repository"]
    path = os.path.join(root, image)
    if not os.path.isfile(path):
        return [f"{where}: {image} is missing"]
    if os.path.getsize(path) > MAX_IMAGE:
        return [f"{where}: {image} is larger than {MAX_IMAGE // 1024} KB"]
    with open(path, "rb") as f:
        if f.read(8) != b"\x89PNG\r\n\x1a\n":
            return [f"{where}: {image} is not a PNG"]
    return []


if __name__ == "__main__":
    found = check(sys.argv[1] if len(sys.argv) > 1 else ".")
    for problem in found:
        print(f"::error file=index.json::{problem}")
    print(f"{len(found)} problem(s)" if found else "index.json and every machine in it are fine")
    sys.exit(1 if found else 0)
