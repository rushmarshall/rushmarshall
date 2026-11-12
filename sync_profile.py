#!/usr/bin/env python3
"""Keep the profile README's numbers and publication list in step with the portfolio site.

Author: Sebastian R.O. Marshall

  python3 sync_profile.py --from <site repo>            rewrite README.md in place (no git)
  python3 sync_profile.py --from <site repo> --push     the same, then commit and push if README.md changed
  python3 sync_profile.py --selftest                    offline, assert-based checks

The site repo is the source of truth: publications.json gives the list and index.html gives the
Google Scholar totals the site already shows. Only the text between the STATS and PUBS markers in
README.md is rewritten. The site's daily sync (sync_scholar.py) calls this after it publishes, so
the profile follows the site without a schedule of its own.
"""
import datetime as dt
import html
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
README = os.path.join(ROOT, "README.md")
STATS = ("<!-- STATS:START -->", "<!-- STATS:END -->")
PUBS = ("<!-- PUBS:START -->", "<!-- PUBS:END -->")
# code repositories that belong to a paper, keyed by DOI
CODE = {"10.1016/j.jhydrol.2026.136599": "https://github.com/rushmarshall/mekong-swat-smap-enkf"}
BOOK_PREFIXES = ("10.1007/978-",)  # book chapters are labelled "Chapter", everything else "Paper"


def stat(page, attr):
    m = re.search(rf'data-target="(\d+)"\s+data-{attr}="\d+"', page)
    return int(m.group(1)) if m else None


def render_stats(pubs, page, today):
    c, h = stat(page, "citations"), stat(page, "hindex")
    if c is None or h is None:
        raise ValueError("site page carries no citation or h-index marker")
    n = len(pubs)
    return (f'{STATS[0]}<b>{n} publication{"" if n == 1 else "s"} · {c}+ citations</b><br>'
            f'h-index {h} · Google Scholar, {today:%B %Y}{STATS[1]}')


def render_pubs(pubs):
    out = [PUBS[0]]
    for p in sorted(pubs, key=lambda p: (-p["year"], -p["cites"], p["title"])):
        title = html.escape(p["title"].rstrip("."), quote=False)
        venue = html.escape(p["venue"], quote=False)
        m = re.match(r"^(.*?)(?=[,\s]+\d)", venue)  # the journal or book name runs up to the first number
        journal = m.group(1) if m else venue
        tail = venue[len(journal):]
        line = f"- **{title}.** *{journal}*{tail} ({p['year']})."
        links = []
        if p.get("doi"):
            label = "Chapter" if p["doi"].startswith(BOOK_PREFIXES) else "Paper"
            links.append(f"[{label}](https://doi.org/{p['doi']})")
            if p["doi"] in CODE:
                links.append(f"[Code]({CODE[p['doi']]})")
        out.append(line + (" " + " · ".join(links) if links else ""))
    out.append(PUBS[1])
    return "\n".join(out)


def swap(text, marks, block):
    s = text.index(marks[0])
    e = text.index(marks[1], s) + len(marks[1])
    return text[:s] + block + text[e:]


def build(readme, pubs, page, today):
    return swap(swap(readme, STATS, render_stats(pubs, page, today)), PUBS, render_pubs(pubs))


def git(*args):
    return subprocess.run(["git", "-C", ROOT, *args], capture_output=True, text=True)


def selftest():
    pubs = [
        {"title": "Old chapter", "doi": "10.1007/978-1-2-3_4", "authors": ["A B"], "venue": "A Book, 1-2", "year": 2022, "cites": 9},
        {"title": "New paper & more", "doi": "10.1016/j.jhydrol.2026.136599", "authors": ["A B"], "venue": "Journal of Hydrology 681, 136599", "year": 2026, "cites": 0},
        {"title": "Cited paper", "doi": None, "authors": ["A B"], "venue": "Earth Systems and Environment 10(1), 553-575", "year": 2026, "cites": 5},
    ]
    page = '<span data-target="200" data-citations="200">200</span>+ <span data-target="5" data-hindex="5">5</span>'
    readme = f"top\n<td>{STATS[0]}old{STATS[1]}</td>\nmid\n{PUBS[0]}\nold\n{PUBS[1]}\nend\n"
    day = dt.date(2026, 11, 12)
    out = build(readme, pubs, page, day)
    assert build(out, pubs, page, day) == out, "render twice != render once"
    assert "<b>3 publications · 200+ citations</b><br>h-index 5 · Google Scholar, November 2026" in out
    lines = [l for l in out.splitlines() if l.startswith("- **")]
    assert [l.split("**")[1] for l in lines] == ["Cited paper.", "New paper &amp; more.", "Old chapter."], lines
    assert "*Journal of Hydrology* 681, 136599 (2026). [Paper](https://doi.org/10.1016/j.jhydrol.2026.136599) · [Code](" in lines[1]
    assert "*Earth Systems and Environment* 10(1), 553-575 (2026)." in lines[0] and "[" not in lines[0]
    assert "*A Book*, 1-2 (2022). [Chapter](https://doi.org/10.1007/978-1-2-3_4)" in lines[2]
    assert out.startswith("top\n") and out.endswith("end\n") and "\nmid\n" in out, "text outside the markers must not change"
    try:
        build(readme, pubs, "no markers", day)
        raise AssertionError("a site page without markers must raise")
    except ValueError:
        pass
    print("selftest ok: idempotent, ordering, labels, code link, text outside markers untouched, missing markers refused")
    return 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if "--from" not in argv:
        print(__doc__)
        return 2
    site = argv[argv.index("--from") + 1]
    with open(os.path.join(site, "publications.json"), encoding="utf-8") as f:
        pubs = json.load(f)
    with open(os.path.join(site, "index.html"), encoding="utf-8") as f:
        page = f.read()
    push = "--push" in argv
    if push:
        dirty = [l for l in git("status", "--porcelain").stdout.splitlines() if l.strip()]
        if dirty:
            print("skip: profile repo has uncommitted edits, not touching them")
            return 3
        if git("pull", "-q", "--rebase", "origin", "main").returncode:
            git("rebase", "--abort")
            print("skip: pull --rebase failed")
            return 4
    with open(README, encoding="utf-8") as f:
        old = f.read()
    # keep the month label steady unless a number actually changed, so the README is not rewritten monthly for nothing
    new = build(old, pubs, page, dt.date.today())
    strip = lambda t: re.sub(r"Google Scholar, [A-Za-z]+ \d{4}", "Google Scholar", t)
    if strip(new) == strip(old):
        print("profile up to date")
        return 0
    with open(README, "w", encoding="utf-8") as f:
        f.write(new)
    if not push:
        print("profile README rewritten (not pushed)")
        return 0
    git("add", "README.md")
    if git("commit", "-q", "-m", f"Sync publications and Scholar numbers from the portfolio ({dt.date.today():%Y-%m-%d})").returncode:
        print("skip: nothing to commit")
        return 0
    if git("push", "-q", "origin", "main").returncode:
        print("profile README committed locally; push FAILED")
        return 5
    print("profile README updated and pushed")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
