#!/usr/bin/env python3
"""Texts From Your Future Self - make.fun entry.

Writes a single funny text message, supposedly sent back by the
writer's future self, to /output/entry.txt (or $OUTPUT_PATH when set).

The message is a fixed string, so every run produces byte-identical
output: no clocks, no randomness, no environment-dependent behaviour.
"""

import os
import sys

MAX_CHARS = 200

MESSAGE = (
    "future you here. don't buy the extended warranty - i already did, "
    "the toaster died in week two anyway, and i'm STILL paying $4 a month "
    "for the privilege of being scammed by us."
)


def check_message(text):
    """Refuse to write a message the gate would reject."""
    if not text or not text.strip():
        raise ValueError("message must not be empty or whitespace only")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "message is %d characters, over the %d limit"
            % (len(text), MAX_CHARS)
        )
    text.encode("utf-8")  # raises if the text is not valid UTF-8
    return text


def main():
    os.umask(0o022)
    text = check_message(MESSAGE)
    out_path = os.environ.get("OUTPUT_PATH") or "/output/entry.txt"
    parent = os.path.dirname(out_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    # Only the file itself gets its mode set: /output is owned by
    # another user on the grader, so touching the directory would fail.
    os.chmod(out_path, 0o644)
    print("wrote %d characters to %s" % (len(text), out_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
