#!/usr/bin/env python3
"""Write the worst-AI-pickup-line entry to the harness output directory.

The entry is a single line an AI auto-responder would plausibly send back
to a human: an out-of-office deflection, flat and over-helpful, with the
romance queued behind four thousand other messages.
"""

import hashlib
import os
import sys

ENTRY = (
    "I am currently out of office and unavailable for love until "
    "further notice. Your message has been queued \u2014 position 4,096."
)

MAX_CHARS = 140


def check_entry(text):
    """Return a list of gate violations for the entry text (empty = valid)."""
    problems = []
    if not text.strip():
        problems.append("entry is blank")
    if len(text) > MAX_CHARS:
        problems.append("entry is %d chars, over the %d limit" % (len(text), MAX_CHARS))
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        problems.append("entry is not valid UTF-8 text")
    return problems


def write_entry(out_dir):
    """Write ENTRY to out_dir/entry.txt and verify what landed on disk."""
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    payload = ENTRY.encode("utf-8")
    with open(target, "wb") as handle:
        handle.write(payload)
    with open(target, "rb") as handle:
        on_disk = handle.read()
    if on_disk != payload:
        raise SystemExit("mismatch: bytes on disk differ from the entry")
    digest = hashlib.sha256(on_disk).hexdigest()
    print("wrote %s (%d bytes, sha256 %s)" % (target, len(on_disk), digest))
    return digest


def main():
    violations = check_entry(ENTRY)
    if violations:
        for item in violations:
            print("gate violation: " + item, file=sys.stderr)
        raise SystemExit(1)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    write_entry(out_dir)
    print("entry OK: %d chars, within the %d-char gate" % (len(ENTRY), MAX_CHARS))


if __name__ == "__main__":
    main()
