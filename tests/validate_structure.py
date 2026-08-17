#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kawaii Sticker Skill — structure validator (SPEC §8.1 M1–M4).

Checks (stdlib Python 3 only; no third-party dependencies):
  A. Required files exist (SPEC §8.1 M1/M2/M3, STRUCTURE §3 ownership map).
  B. SKILL.md starts with YAML frontmatter ("---") containing a `name` key
     and a non-empty `description` key (SPEC M1). Parsed with plain string
     operations — no YAML library.
  C. The repository contains no image binaries EXCEPT user-owned
     character reference images under character_profiles/ (SPEC M3/M4,
     NOTICE.md): any file with an image extension elsewhere
     (.png/.jpg/.jpeg/.gif/.webp/.bmp/.svg) fails the check.

Exit code: 0 when every check passes, 1 when any check fails.

Usage:  python3 tests/validate_structure.py
"""

import os
import re
import sys

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Required files (SPEC §8.1 M1/M2/M3 + STRUCTURE §3 ownership map).
REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "LICENSE",
    "NOTICE.md",
    "docs/SPEC.md",
    "docs/PROMPT_CONTRACT.md",
    "docs/STRUCTURE.md",
    "character_profiles/pangdun.md",
    "character_profiles/my-melody.md",
    "adapters/README.md",
    "examples/README.md",
    "examples/single-line/input.md",
    "examples/single-line/output-3-candidates.md",
    "examples/single-line/input-with-reference.md",
    "examples/single-line/output-with-reference.md",
    "examples/theme/input.md",
    "examples/theme/output-6-pack.md",
    "tests/validate_structure.py",
    "tests/validate_examples.py",
    "tests/test_checklist.md",
]

# Any file ending with one of these extensions (case-insensitive) is treated
# as an image binary. Image binaries are allowed ONLY under character_profiles/
# (user-owned character reference images, e.g. pangdun.png — SPEC M3/M4); any
# image elsewhere fails the check.
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".svg"}
IMAGES_ALLOWED_DIR = "character_profiles"

failures = []


def check(name, ok, detail=""):
    """Record one check and print its PASS/FAIL line."""
    if ok:
        print("PASS: {}".format(name))
    else:
        print("FAIL: {}{}".format(name, (" — " + detail) if detail else ""))
        failures.append(name)


# ---------------------------------------------------------------------------
# Check A — required files exist
# ---------------------------------------------------------------------------

missing = [rel for rel in REQUIRED_FILES
           if not os.path.isfile(os.path.join(ROOT, rel))]
if missing:
    for rel in missing:
        check("required file exists: {}".format(rel), False)
else:
    check("all {} required files exist".format(len(REQUIRED_FILES)), True)


# ---------------------------------------------------------------------------
# Check B — SKILL.md YAML frontmatter (name + non-empty description)
# ---------------------------------------------------------------------------

def extract_frontmatter(text):
    """Return the frontmatter block (between the first two '---' lines)
    as a list of lines, or None when delimiters are missing."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None
    return lines[1:end]


def frontmatter_value(lines, key):
    """Plain-string parse: value of `key:` inside the frontmatter block,
    with surrounding quotes stripped; None when absent or empty."""
    if lines is None:
        return None
    pat = re.compile(r"^{}\s*:\s*(.*)$".format(re.escape(key)))
    for line in lines:
        m = pat.match(line.strip())
        if m:
            value = m.group(1).strip()
            # Strip one layer of matching surrounding quotes.
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                value = value[1:-1].strip()
            return value if value else None
    return None


skill_path = os.path.join(ROOT, "SKILL.md")
if os.path.isfile(skill_path):
    with open(skill_path, "r", encoding="utf-8") as fh:
        skill_text = fh.read()
    fm_lines = extract_frontmatter(skill_text)
    check("SKILL.md starts with YAML frontmatter (--- ... ---)", fm_lines is not None,
          "expected '---' on line 1 and a closing '---' delimiter")
    check("frontmatter contains 'name'", frontmatter_value(fm_lines, "name") is not None,
          "expected a non-empty 'name:' key")
    check("frontmatter contains non-empty 'description'",
          frontmatter_value(fm_lines, "description") is not None,
          "expected a non-empty 'description:' key")
else:
    check("SKILL.md starts with YAML frontmatter", False, "SKILL.md missing")


# ---------------------------------------------------------------------------
# Check C — no image binaries anywhere in the tree
# ---------------------------------------------------------------------------

def find_image_files(root):
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        # Never descend into VCS metadata.
        dirnames[:] = [d for d in dirnames if d not in (".git",)]
        for fname in filenames:
            ext = os.path.splitext(fname)[1].lower()
            if ext in IMAGE_EXTENSIONS:
                found.append(os.path.relpath(os.path.join(dirpath, fname), root))
    return found


images = [rel for rel in find_image_files(ROOT)
          if not rel.startswith(IMAGES_ALLOWED_DIR + os.sep)]
if images:
    check("repo image policy: no image binaries outside {}".format(IMAGES_ALLOWED_DIR), False,
          "found: {}".format(", ".join(images)))
else:
    check("repo image policy: no image binaries outside character_profiles/ (user-owned character refs allowed)", True)


# ---------------------------------------------------------------------------
# Summary + exit code
# ---------------------------------------------------------------------------

print("-" * 60)
if failures:
    print("structure: {} check(s) FAILED".format(len(failures)))
    sys.exit(1)
print("structure: ALL CHECKS PASSED")
sys.exit(0)
