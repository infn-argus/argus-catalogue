"""Release what was merged since the last tag: the next version, its CHANGELOG section, and the tag.

Run by .github/workflows/release.yml after the validator passes on main. Prints `version=vX.Y.Z` for the workflow,
or nothing when there is nothing to release (no change under collections/ since the last tag, or HEAD tagged).

- The version: a minor step when a collection or an entry was added, a patch step otherwise (0.x: no major).
- The CHANGELOG: an "unreleased" section a person wrote at the top is kept, dated and given the version; without
  one, a section is written from the subjects of the commits that changed collections/ since the last tag.
"""
import datetime
import re
import subprocess
import sys
from pathlib import Path

TAG = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")


def git(*args: str) -> str:
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout.strip()


def last_tag() -> str | None:
    tags = [t for t in git("tag", "--list", "v*").split() if TAG.match(t)]
    return max(tags, key=lambda t: tuple(int(x) for x in TAG.match(t).groups())) if tags else None


def next_version(last: str | None, diff: str, added_collections: bool) -> str:
    if last is None:
        return "v0.1.0"
    major, minor, patch = (int(x) for x in TAG.match(last).groups())
    added_entries = any(line.startswith("+- id:") for line in diff.splitlines())
    if added_collections or added_entries:
        return f"v{major}.{minor + 1}.0"
    return f"v{major}.{minor}.{patch + 1}"


def changelog(text: str, version: str, today: str, subjects: list[str], released: set[str]) -> str:
    head, sep, rest = text.partition("\n## ")
    if sep:
        first, _, body = rest.partition("\n")
        m = re.match(r"^(v\d+\.\d+\.\d+) — unreleased\s*$", first)
        if m and m.group(1) not in released:              # written by a person: dated, with this release's version
            return f"{head}\n## {version} — {today}\n{body}"
    items = "\n".join(f"- {s}" for s in subjects) or "- Maintenance."
    section = f"## {version} — {today}\n\n{items}\n"
    return f"{head}\n{section}\n## {rest}" if sep else f"{text.rstrip()}\n\n{section}"


def main() -> int:
    last = last_tag()
    if last and git("rev-parse", "HEAD") == git("rev-list", "-n", "1", last):
        return 0
    span = f"{last}..HEAD" if last else "HEAD"
    if last and not git("diff", "--name-only", last, "HEAD", "--", "collections/"):
        return 0
    diff = git("diff", last, "HEAD", "--", "collections/") if last else ""
    added_collections = bool(git("diff", "--name-only", "--diff-filter=A", last, "HEAD", "--",
                                 "collections/*/collection.yaml")) if last else True
    version = next_version(last, diff, added_collections)
    subjects = [s for s in git("log", "--no-merges", "--format=%s", span, "--", "collections/").splitlines()
                if s and not s.startswith("Release v")]
    path = Path("CHANGELOG.md")
    released = set(git("tag", "--list", "v*").split())
    path.write_text(changelog(path.read_text() if path.exists() else "# Changelog\n", version,
                              datetime.date.today().isoformat(), subjects, released))
    print(f"version={version}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
