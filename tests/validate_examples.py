#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kawaii Sticker Skill — example contract validator (SPEC §8.1 M5/M6).

Parses the example output files under examples/ exactly per the conventions
in examples/README.md §2 (block format) and §3 (input marker) and validates
them against docs/PROMPT_CONTRACT.md §4 machine rules. Stdlib Python 3 only.

Checks performed (per output file):
  - exactly ONE fenced block with info string `kss-prompt`
    (start line matches ^```kss-prompt$, closing line matches ^```$)
  - block content is valid JSON (RFC 8259, JSON.parse-able) and top-level
    is a LIST whose length matches the mode: single_line -> 3, theme -> 6
  - every block carries all required contract fields:
    format_version, mode, character.feature_map, style_anchor, expression,
    pose_action, composition, sticker_elements, text, output
  - enum/const values, case-sensitive: format_version == "1.0";
    mode == expected; character.source in {"image","profile"};
    output.format == "png", output.background == "transparent",
    output.aspect_ratio == "1:1", output.text_baked is True
  - feature_map contains the identity fields (SPEC §4.3 ✅ set) with correct
    types (palette: object, signature_accessories: array of string)
  - text.content non-empty; single_line -> verbatim is True and content is
    byte-equal to the paired input marker (examples/README.md §3); the
    single-line input marker itself must equal "我真的会谢"
  - single_line: expression / pose_action / composition pairwise distinct
    (sticker_elements also pairwise distinct, as in all golden examples)
  - theme: the 6 text.content are pairwise distinct; the 6 expression
    values are pairwise distinct; the (expression, pose_action, composition)
    triplets are pairwise distinct
  - within one file all blocks share the SAME style_anchor, the SAME
    feature_map (deep compare), the SAME output and the SAME format_version
  - review_flags (when present): keys in the legal SPEC §8.1 set, all
    values boolean

Exit code: 0 when every check passes, 1 when any check fails.

Usage:  python3 tests/validate_examples.py
"""

import json
import os
import re
import sys

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXAMPLES = os.path.join(ROOT, "examples")

# Output file -> (paired input file, expected mode, expected block count).
OUTPUT_TARGETS = [
    ("single-line/output-3-candidates.md",
     "single-line/input.md", "single_line", 3),
    ("single-line/output-with-reference.md",
     "single-line/input-with-reference.md", "single_line", 3),
    ("theme/output-6-pack.md",
     "theme/input.md", "theme", 6),
]

EXPECTED_SINGLE_LINE_INPUT = "我真的会谢"

FENCE_START_RE = re.compile(r"^```kss-prompt$")
FENCE_END_RE = re.compile(r"^```$")
INPUT_MARKER_RE = re.compile(r"<!--\s*input:\s*(.*?)\s*-->")

REQUIRED_TOP_FIELDS = [
    "format_version", "mode", "character", "style_anchor",
    "expression", "pose_action", "composition", "sticker_elements",
    "text", "output",
]
FEATURE_MAP_IDENTITY_FIELDS = [
    "head_shape", "ears", "eyes", "nose_mouth",
    "palette", "signature_accessories",
]
TEXT_FIELDS = ["content", "verbatim"]
OUTPUT_FIELDS = ["format", "background", "aspect_ratio", "text_baked"]
LEGAL_REVIEW_FLAGS = {
    "verbatim_preserved", "text_baked", "transparent", "square_1to1",
    "readable_at_small", "no_watermark", "no_trademark",
}
VALID_MODES = {"single_line", "theme"}
VALID_SOURCES = {"image", "profile"}

failures = []


def check(name, ok, detail=""):
    """Record one check and print its PASS/FAIL line."""
    if ok:
        print("PASS: {}".format(name))
    else:
        print("FAIL: {}{}".format(name, (" — " + detail) if detail else ""))
        failures.append(name)


def read(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def rel(path):
    return os.path.relpath(path, ROOT)


# ---------------------------------------------------------------------------
# Block parsing (examples/README.md §2 + PROMPT_CONTRACT §4 rules 1-3)
# ---------------------------------------------------------------------------

def extract_blocks(md_text):
    """Return a list of (start_index, content, end_index) fenced blocks whose
    info string is exactly `kss-prompt`."""
    lines = md_text.splitlines()
    blocks = []
    i = 0
    while i < len(lines):
        if FENCE_START_RE.match(lines[i]):
            start = i
            j = i + 1
            while j < len(lines) and not FENCE_END_RE.match(lines[j]):
                j += 1
            if j >= len(lines):
                blocks.append((start, "\n".join(lines[i + 1:j]), None))
            else:
                blocks.append((start, "\n".join(lines[i + 1:j]), j))
            i = j + 1
        else:
            i += 1
    return blocks


def parse_output_file(relpath):
    """Return (mode, [contract objects], problems-list)."""
    problems = []
    full = os.path.join(EXAMPLES, relpath)
    text = read(full)

    blocks = extract_blocks(text)
    if len(blocks) != 1:
        problems.append("expected exactly 1 kss-prompt block, found {}".format(len(blocks)))
        return None, [], problems

    _, content, closing = blocks[0]
    if closing is None:
        problems.append("kss-prompt block is not closed with a ``` fence")
        return None, [], problems

    try:
        data = json.loads(content)
    except ValueError as exc:
        problems.append("block content is not valid JSON: {}".format(exc))
        return None, [], problems

    if not isinstance(data, list):
        problems.append("top-level JSON must be a LIST (array of contracts), got {}".format(type(data).__name__))
        return None, [], problems

    return None, data, problems


# ---------------------------------------------------------------------------
# Per-block contract validation (PROMPT_CONTRACT §4 rules 4, 6, 9)
# ---------------------------------------------------------------------------

def validate_block(obj, index, expected_mode):
    """Return a list of problem strings for one contract object."""
    problems = []

    missing = [f for f in REQUIRED_TOP_FIELDS if f not in obj]
    if missing:
        problems.append("block[{}] missing required fields: {}".format(index, ", ".join(missing)))

    if "format_version" in obj and obj["format_version"] != "1.0":
        problems.append("block[{}] format_version must be \"1.0\", got {!r}".format(index, obj["format_version"]))

    if "mode" in obj:
        if obj["mode"] not in VALID_MODES:
            problems.append("block[{}] mode {!r} not in {{single_line, theme}}".format(index, obj["mode"]))
        elif obj["mode"] != expected_mode:
            problems.append("block[{}] mode {!r} does not match expected {!r}".format(index, obj["mode"], expected_mode))

    character = obj.get("character")
    if isinstance(character, dict):
        source = character.get("source")
        if source not in VALID_SOURCES:
            problems.append("block[{}] character.source {!r} not in {{image, profile}}".format(index, source))
        fm = character.get("feature_map")
        if not isinstance(fm, dict):
            problems.append("block[{}] character.feature_map must be an object".format(index))
        else:
            missing_fm = [f for f in FEATURE_MAP_IDENTITY_FIELDS if f not in fm]
            if missing_fm:
                problems.append("block[{}] feature_map missing identity fields: {}".format(index, ", ".join(missing_fm)))
            if "palette" in fm and not isinstance(fm["palette"], dict):
                problems.append("block[{}] feature_map.palette must be an object".format(index))
            if "signature_accessories" in fm and not (
                    isinstance(fm["signature_accessories"], list)
                    and all(isinstance(x, str) for x in fm["signature_accessories"])):
                problems.append("block[{}] feature_map.signature_accessories must be an array of strings".format(index))
    else:
        problems.append("block[{}] character must be an object with source + feature_map".format(index))

    for field in ("style_anchor", "expression", "pose_action", "composition"):
        value = obj.get(field)
        if not isinstance(value, str) or not value.strip():
            problems.append("block[{}] {} must be a non-empty string".format(index, field))

    se = obj.get("sticker_elements")
    if not (isinstance(se, list) and all(isinstance(x, str) for x in se)):
        problems.append("block[{}] sticker_elements must be an array of strings".format(index))

    text = obj.get("text")
    if isinstance(text, dict):
        missing_text = [f for f in TEXT_FIELDS if f not in text]
        if missing_text:
            problems.append("block[{}] text missing fields: {}".format(index, ", ".join(missing_text)))
        content = text.get("content")
        if not isinstance(content, str) or not content.strip():
            problems.append("block[{}] text.content must be a non-empty string".format(index))
        if "verbatim" in text and not isinstance(text["verbatim"], bool):
            problems.append("block[{}] text.verbatim must be a boolean".format(index))
        if expected_mode == "single_line" and text.get("verbatim") is not True:
            problems.append("block[{}] single_line requires text.verbatim === true".format(index))
    else:
        problems.append("block[{}] text must be an object".format(index))

    output = obj.get("output")
    if isinstance(output, dict):
        missing_out = [f for f in OUTPUT_FIELDS if f not in output]
        if missing_out:
            problems.append("block[{}] output missing fields: {}".format(index, ", ".join(missing_out)))
        consts = [("format", "png"), ("background", "transparent"), ("aspect_ratio", "1:1")]
        for key, wanted in consts:
            if output.get(key) != wanted:
                problems.append("block[{}] output.{} must be {!r} (case-sensitive), got {!r}".format(
                    index, key, wanted, output.get(key)))
        if output.get("text_baked") is not True:
            problems.append("block[{}] output.text_baked must be true".format(index))
    else:
        problems.append("block[{}] output must be an object".format(index))

    rf = obj.get("review_flags")
    if rf is not None:
        if not isinstance(rf, dict):
            problems.append("block[{}] review_flags must be an object of booleans".format(index))
        else:
            for key, value in rf.items():
                if key not in LEGAL_REVIEW_FLAGS:
                    problems.append("block[{}] review_flags has illegal field {!r}".format(index, key))
                if not isinstance(value, bool):
                    problems.append("block[{}] review_flags.{!r} must be a boolean".format(index, key))

    return problems


# ---------------------------------------------------------------------------
# Pairwise-distinct helpers
# ---------------------------------------------------------------------------

def pairwise_distinct(values):
    return len(values) == len(set(values))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

print("== validate_examples.py ==")

# --- Input markers ---------------------------------------------------------
all_input_paths = sorted(set(pair[1] for pair in OUTPUT_TARGETS))
for in_rel in all_input_paths:
    in_full = os.path.join(EXAMPLES, in_rel)
    text = read(in_full)
    m = INPUT_MARKER_RE.search(text)
    if m is None:
        check("{}: input marker present".format(in_rel), False, "expected <!-- input: ... -->")
        continue
    marker = m.group(1).strip()
    check("{}: input marker present and non-empty".format(in_rel), bool(marker),
          "<!-- input: ... --> parsed empty")
    if "single-line" in in_rel:
        check("{}: single-line input marker == {!r}".format(in_rel, EXPECTED_SINGLE_LINE_INPUT),
              marker == EXPECTED_SINGLE_LINE_INPUT,
              "got {!r}".format(marker))

# --- Output files ----------------------------------------------------------
for out_rel, in_rel, expected_mode, expected_len in OUTPUT_TARGETS:
    label = out_rel
    _, contracts, problems = parse_output_file(out_rel)

    check("{}: exactly one kss-prompt block".format(label), not any("kss-prompt block" in p for p in problems),
          next((p for p in problems if "kss-prompt block" in p), ""))
    check("{}: block content is valid JSON, top-level list".format(label),
          not any("valid JSON" in p or "top-level JSON" in p for p in problems),
          " | ".join(p for p in problems if "valid JSON" in p or "top-level JSON" in p))
    if problems:
        check("{}: block is closed by a ``` fence".format(label),
              not any("not closed" in p for p in problems),
              next((p for p in problems if "not closed" in p), ""))
        continue

    check("{}: array length == {} ({} contracts)".format(label, expected_len, expected_mode),
          len(contracts) == expected_len,
          "got {}".format(len(contracts)))

    if len(contracts) != expected_len:
        continue

    # Per-block validation.
    block_problems = []
    for i, obj in enumerate(contracts):
        block_problems.extend(validate_block(obj, i, expected_mode))
    if block_problems:
        for p in block_problems:
            check("{}: {}".format(label, p), False)
    else:
        check("{}: every block has all required fields with valid types/enum/const".format(label), True)

    # Verbatim equality against the input marker (single_line).
    in_text = read(os.path.join(EXAMPLES, in_rel))
    m = INPUT_MARKER_RE.search(in_text)
    marker = m.group(1).strip() if m else ""
    if expected_mode == "single_line":
        ok = bool(marker) and all(
            c.get("text", {}).get("content", "").encode("utf-8") == marker.encode("utf-8")
            for c in contracts)
        check("{}: text.content byte-equal to input marker {!r} in EVERY block".format(label, marker),
              ok, "single_line copy must be verbatim (byte-level)")
        check("{}: every block text.content == {!r}".format(label, EXPECTED_SINGLE_LINE_INPUT),
              all(c.get("text", {}).get("content", "") == EXPECTED_SINGLE_LINE_INPUT for c in contracts))

    # Pairwise-distinct checks.
    def values(key):
        return [c.get(key) for c in contracts]

    if expected_mode == "single_line":
        for field in ("expression", "pose_action", "composition", "sticker_elements"):
            if field == "sticker_elements":
                # Lists are unhashable: compare via canonical JSON serialization.
                vals = [json.dumps(v, ensure_ascii=False, sort_keys=True) for v in values(field)]
            else:
                vals = values(field)
            check("{}: {} pairwise distinct across {} blocks".format(label, field, expected_len),
                  pairwise_distinct(vals),
                  "values: {}".format(values(field)))
    else:  # theme
        check("{}: text.content pairwise distinct across 6 blocks".format(label),
              pairwise_distinct([c.get("text", {}).get("content") for c in contracts]))
        check("{}: expression pairwise distinct across 6 blocks (distinct emotions)".format(label),
              pairwise_distinct(values("expression")),
              "values: {}".format(values("expression")))
        triplets = [(c.get("expression"), c.get("pose_action"), c.get("composition")) for c in contracts]
        check("{}: (expression, pose_action, composition) triplets pairwise distinct".format(label),
              pairwise_distinct(triplets),
              "duplicate: {}".format(triplets))

    # Within-file consistency (PROMPT_CONTRACT §4 rule 6).
    check("{}: all blocks share the same style_anchor".format(label),
          len(set(values("style_anchor"))) == 1,
          "anchors: {}".format(set(values("style_anchor"))))
    feature_maps = [c.get("character", {}).get("feature_map") for c in contracts]
    check("{}: all blocks share the same character.feature_map (deep)".format(label),
          len({json.dumps(fm, ensure_ascii=False, sort_keys=True) for fm in feature_maps}) == 1)
    outputs = [c.get("output") for c in contracts]
    check("{}: all blocks share the same output (deep)".format(label),
          len({json.dumps(o, ensure_ascii=False, sort_keys=True) for o in outputs}) == 1)
    check("{}: all blocks share the same format_version".format(label),
          len(set(values("format_version"))) == 1,
          "versions: {}".format(set(values("format_version"))))

    # review_flags already validated per block (legal keys + booleans).

# ---------------------------------------------------------------------------
# Summary + exit code
# ---------------------------------------------------------------------------

print("-" * 60)
if failures:
    print("examples: {} check(s) FAILED".format(len(failures)))
    sys.exit(1)
print("examples: ALL CHECKS PASSED")
sys.exit(0)
