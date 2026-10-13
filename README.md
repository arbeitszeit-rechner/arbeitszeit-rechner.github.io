# Arbeitszeit Rechner (Hugo)

Deutschsprachige Website zum Thema „Arbeitszeit Rechner“. Stand: Phase 1 (Projektstruktur). Offene Aufgaben: siehe `KURANG.md`.

## Befehle

```bash
hugo server            # lokale Vorschau (robots.txt sperrt im Entwicklungsmodus alles)
hugo --minify          # Produktionsbuild nach public/ (Hugo >= 0.128)
python3 scripts/validate.py content   # Front matter prüfen (benötigt PyYAML)
python3 scripts/validate.py public    # gebautes HTML prüfen
```

## Struktur

| Pfad | Zweck |
|---|---|
| `hugo.toml` | Konfiguration: Base-URL, Sprache, Menüs, Sitemap, Werbe-Modus |
| `content/` | Inhalte (Startseite, Glossar, Pflichtseiten) |
| `layouts/_default/` | `baseof` (Grundgerüst), `single`, `list` |
| `layouts/index.html` | Startseite: Überschrift, Rechner, Artikel, Glossar-Links |
| `layouts/glossar/` | Glossar-Hub (gruppiert nach Kategorien) und Eintrags-Template |
| `layouts/partials/` | `head`, `seo`, `schema` (JSON-LD), `breadcrumbs`, `navbar`, `footer`, `calculator`, `ads/slot`, … |
| `layouts/shortcodes/` | `ad` (Werbeplatz im Artikel), `kontaktdaten` |
| `layouts/robots.txt` | robots.txt-Template; die Sitemap erzeugt Hugo |
| `assets/css`, `assets/js` | Design-System (inline eingebunden) und minimales JavaScript |
| `static/fonts/` | Inter (SIL OFL), selbst gehostet |
| `data/author.yaml` | Wiederverwendbares Autorenprofil (nur verifizierte Angaben) |
| `archetypes/` | Vorlagen für neue Seiten, `hugo new glossar/begriff.md` |
| `scripts/validate.py` | SEO-Prüfungen (Description-Länge, Titel, Slugs, JSON-LD) |

## Front-matter-Felder

`title` (ohne Seitennamen-Suffix), `description` (150–155 Zeichen), `slug`, `linkTitle`, `h1`, `lead`, `date`, `lastmod`, `show_author`, `noindex`, `ads` (false = keine Werbung), `webpage_type` (AboutPage, ContactPage, …), `main_entity` (Article).
Glossar-Einträge zusätzlich: `term`, `question`, `kategorie`, `featured`.
