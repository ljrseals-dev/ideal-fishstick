# Legacy Theme Builder

**Authors:** Lewis Seals & Crystal Cheairs (`Crystal-Codec-Newton`)

A production-grade toolkit for safely reverse-engineering legacy game music structures, analyzing rhythmic patterns, and transforming them into brand-new, original full-length musical themes across Japanese Pop / City Pop, Western Classical, and Hip-Hop / Trap styles.

---

## Repository Structure

| File | Description |
|------|-------------|
| `music_genre_templates.py` | Style engine defining BPM ranges, scales, chord progressions, sections, and drum grooves |
| `game_extract.json` | Neutral mock extraction data (11-note motif seed, 2.25 bars) |
| `theme_builder.py` | Expands the motif across full template section lengths and maps to target scales |
| `midi_exporter.py` | Zero-dependency multi-track MIDI compiler (full-length melody + looped drums) |
| `sequence_parser.pas` | Free Pascal parser for sequence JSON |
| `ghidra_music_helper.py` | Ghidra helper to locate music symbols and Pascal strings |
| `new_theme_*.json` | Pre-generated full-length theme datasets |
| `new_theme_*.mid` | Pre-compiled full-length playable MIDI files |

---

## Full-Track Specs

| Style | Bars | Ticks | BPM | Duration |
|-------|------|-------|-----|----------|
| Japanese Pop / City Pop | 36 | 69,120 | 113 | ~1:16 |
| Western Classical | 64 | 122,880 | 110 | ~2:20 |
| Hip-Hop / Trap | 40 | 76,800 | 95 | ~1:41 |

The 11-note / 4,320-tick extract is treated as a motif seed. `theme_builder.py` loops it to fill `total_bars × 4 × 480` ticks. Drums (16-step / 1-bar pattern) repeat once per bar across the full length.

---

## Quick Start

```bash
python theme_builder.py
python midi_exporter.py
```

Outputs:

- `new_theme_japanese.json` / `.mid` (36 bars)
- `new_theme_classical.json` / `.mid` (64 bars)
- `new_theme_hiphop.json` / `.mid` (40 bars)

### Pascal reader (optional)

```bash
fpc sequence_parser.pas
./sequence_parser
```

---

## Legal & Ethical Guidelines

- Only analyze binaries and game files that you legally own.
- Do not redistribute copyrighted audio assets, ROMs, or raw extracted code.
- Output themes are original algorithmic transformations; do not misrepresent them as the original game tracks.
- Do not bypass DRM.
- Offline-first, no telemetry.

---

## Requirements

- Python 3.10+
- Free Pascal (`fpc`) – optional
- Ghidra – optional

No external Python packages required.
