#!/usr/bin/env python3
"""Validiert SEO-Vorgaben des Projekts.

  python3 scripts/validate.py content   # prüft front matter in content/ (ohne Hugo lauffähig)
  python3 scripts/validate.py public    # prüft das gebaute HTML in public/ (nach `hugo --minify`)

Prüfungen: Description 150-155 Zeichen, Titel ohne Seitennamen-Suffix, eindeutige Titel/Descriptions/Slugs,
Slug-Format, Glossar-Antwort <= 50 Wörter, im gebauten HTML: lang, Canonical, genau ein H1, JSON-LD parsebar.
"""
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://arbeitszeit-rechner.github.io/"
SITE_NAME = "Arbeitszeit Rechner"
errors: list[str] = []
warnings: list[str] = []


def err(msg):
    errors.append(msg)


def title_has_suffix(title: str) -> bool:
    return bool(re.search(r"\s[|–—-]\s*" + re.escape(SITE_NAME) + r"\s*$", title, re.I)) or "|" in title


def check_content():
    titles, descs, slugs = {}, {}, {}
    for path in sorted((ROOT / "content").rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
        rel = path.relative_to(ROOT)
        if not m:
            err(f"{rel}: kein front matter")
            continue
        fm, body = yaml.safe_load(m.group(1)) or {}, m.group(2)
        title, desc = fm.get("title", ""), fm.get("description", "")
        if not title:
            err(f"{rel}: title fehlt")
        elif title_has_suffix(title):
            err(f"{rel}: Titel enthält Seitennamen-Suffix: {title!r}")
        if not desc:
            err(f"{rel}: description fehlt")
        elif not 150 <= len(desc) <= 155:
            err(f"{rel}: description hat {len(desc)} Zeichen (Soll 150-155)")
        for key, store, label in ((title, titles, "title"), (desc, descs, "description")):
            if key and key in store:
                err(f"{rel}: {label} doppelt (auch in {store[key]})")
            store[key] = rel
        slug = fm.get("slug")
        if slug:
            if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug):
                err(f"{rel}: slug {slug!r} ist nicht kleingeschrieben/sauber")
            full = f"{path.parent.name}/{slug}" if path.parent.name != "content" else slug
            if full in slugs:
                err(f"{rel}: slug doppelt (auch in {slugs[full]})")
            slugs[full] = rel
        elif path.name != "_index.md":
            err(f"{rel}: slug fehlt")
        # Glossar-Einträge: Antwort <= 50 Wörter, genau ein externer und ein Startseiten-Link
        if path.parent.name == "glossar" and path.name != "_index.md":
            paras = [p.strip() for p in body.strip().split("\n\n") if p.strip()]
            if not paras:
                err(f"{rel}: kein Inhalt")
                continue
            words = len(re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", paras[0]).split())
            if words > 50:
                err(f"{rel}: Antwort hat {words} Wörter (max. 50)")
            ext = re.findall(r"\]\((https?://[^)]+)\)", body)
            if len(ext) != 1:
                err(f"{rel}: erwartet genau 1 externen Link, gefunden {len(ext)}")
            if not re.search(r"\]\(/\)", body):
                err(f"{rel}: Link zur Startseite fehlt")


def check_hub():
    """Hub-Kategorien: Namen eindeutig, Beschreibung vorhanden; Einträge verweisen auf existierende Kategorien."""
    hub = ROOT / "content" / "glossar" / "_index.md"
    m = re.match(r"^---\n(.*?)\n---", hub.read_text(encoding="utf-8"), re.S)
    cats = (yaml.safe_load(m.group(1)) or {}).get("kategorien") or []
    names = [c.get("name") for c in cats]
    if len(names) != len(set(names)):
        err("glossar/_index.md: doppelte Kategorienamen")
    for c in cats:
        if not c.get("name") or not c.get("description"):
            err(f"glossar/_index.md: Kategorie ohne name/description: {c}")
    for path in sorted((ROOT / "content" / "glossar").glob("*.md")):
        if path.name == "_index.md":
            continue
        fm = yaml.safe_load(re.match(r"^---\n(.*?)\n---", path.read_text(encoding="utf-8"), re.S).group(1)) or {}
        if fm.get("kategorie") not in names:
            err(f"{path.relative_to(ROOT)}: kategorie {fm.get('kategorie')!r} nicht im Hub definiert")


def check_public():
    pub = ROOT / "public"
    if not pub.exists():
        err("public/ fehlt: zuerst `hugo --minify` ausführen")
        return
    for path in sorted(pub.rglob("*.html")):
        html = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)
        is404 = path.name == "404.html"
        if not re.search(r'<html[^>]*lang=["\']?de-DE', html):
            err(f"{rel}: lang=de-DE fehlt")
        if len(re.findall(r"<h1[\s>]", html)) != 1:
            err(f"{rel}: genau ein <h1> erwartet")
        if not is404:
            c = re.search(r'<link rel=["\']?canonical["\']? href=["\']?([^"\'>\s]+)', html)
            if not c or not c.group(1).startswith(BASE):
                err(f"{rel}: Canonical fehlt oder falsche Domain")
            d = re.search(r'<meta name=["\']?description["\']? content=["\']([^"\']*)["\']', html)
            if not d or not 150 <= len(d.group(1)) <= 155:
                err(f"{rel}: description fehlt oder nicht 150-155 Zeichen")
            if not re.search(r"<title>[^<]+</title>", html):
                err(f"{rel}: <title> fehlt")
        for block in re.findall(r'<script type=["\']?application/ld\+json["\']?>(.*?)</script>', html, re.S):
            try:
                data = json.loads(block)
                if "@graph" not in data:
                    err(f"{rel}: JSON-LD ohne @graph")
            except json.JSONDecodeError as exc:
                err(f"{rel}: JSON-LD ungültig: {exc}")
        if not is404 and "application/ld+json" not in html:
            err(f"{rel}: kein JSON-LD")
    for name in ("sitemap.xml", "robots.txt"):
        if not (pub / name).exists():
            err(f"public/{name} fehlt")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "content"
    if mode == "content":
        check_content()
        check_hub()
    else:
        check_public()
    for w in warnings:
        print("WARN ", w)
    for e in errors:
        print("FEHLER", e)
    print(f"\n{len(errors)} Fehler, {len(warnings)} Warnungen ({mode})")
    sys.exit(1 if errors else 0)
