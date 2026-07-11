#!/usr/bin/python3
"""run_tests.py — RUN mistletoe's own test suite and print a parseable summary.

Invoked via the `/mayhem/mistletoe-tests` ELF launcher (NOT directly), so the verify-repo
sabotage oracle can neuter the launcher and prove the test oracle is behavioral.

mistletoe ships a real unittest suite under test/ (hundreds of known-answer cases asserting
Markdown -> HTML / LaTeX / AST / renderer output exactly, plus the CommonMark conformance
checks). We run it with pytest (which collects the unittest TestCases), write a JUnit XML,
parse the counts, and print one line:

    RUNTESTS tests=<n> passed=<p> failed=<f> skipped=<s>

Exit 0 iff failed == 0. mayhem/test.sh parses that line into a CTRF report.
"""
from __future__ import annotations

import sys
import xml.etree.ElementTree as ET

import pytest

XML = "/tmp/mistletoe-junit.xml"
TESTS_DIR = "/mayhem/test"


def main() -> int:
    pytest.main(["-q", "-p", "no:cacheprovider", TESTS_DIR, "--junitxml", XML])

    root = ET.parse(XML).getroot()
    suites = root.findall("testsuite") or ([root] if root.tag == "testsuite" else [])
    if not suites:
        print("RUNTESTS tests=0 passed=0 failed=1 skipped=0")
        return 1

    tests = failed = skipped = 0
    for s in suites:
        tests += int(s.get("tests", 0))
        failed += int(s.get("failures", 0)) + int(s.get("errors", 0))
        skipped += int(s.get("skipped", 0))
    passed = tests - failed - skipped

    print(f"RUNTESTS tests={tests} passed={passed} failed={failed} skipped={skipped}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
