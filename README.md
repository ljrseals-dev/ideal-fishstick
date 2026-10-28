# Legacy Theme Builder

**Authors:** Lewis Seals & Crystal Cheairs (`Crystal-Codec-Newton`)

A production-grade toolkit for safely reverse-engineering legacy game music structures, analyzing rhythmic patterns, and transforming them into brand-new, original musical themes across Japanese Pop / City Pop, Western Classical, and Hip-Hop / Trap styles.

---

## Repository Structure

| File | Description |
|------|-------------|
| `music_genre_templates.py` | Style engine defining BPM ranges, scales, chord progressions, and drum grooves |
| `game_extract.json` | Neutral mock extraction data simulating game sequence analysis (Ghidra output) |
| `theme_builder.py` | Core transformation script mapping extracted rhythm durations onto target style scales |
| `midi_exporter.py` | Zero-dependency compiler generating standard multi-track MIDI files (`.mid`) |
| `sequence_parser.pas` | Free Pascal parser to load and analyze sequence JSON natively |
| `ghidra_music_helper.py` | Ghidra helper script to locate music symbols and Pascal string drivers in binaries |
| `new_theme_*.json` | Pre-generated original theme JSON datasets |
| `new_theme_*.mid` | Pre-compiled playable MIDI audio files |

---

## Quick Start

### 1. Generate Original Themes from Extract

```bash
python theme_builder.py
```

This reads `game_extract.json` and outputs:

- `new_theme_japanese.json`
- `new_theme_classical.json`
- `new_theme_hiphop.json`

### 2. Export Playable MIDI Files

```bash
python midi_exporter.py
```

This compiles the JSON themes into standard multi-track MIDI files:

- `new_theme_japanese.mid`
- `new_theme_classical.mid`
- `new_theme_hiphop.mid`

### 3. Build & Run the Pascal Parser

```bash
fpc sequence_parser.pas
./sequence_parser
```

---

## Legal & Ethical Guidelines

- Only analyze binaries and game files that you legally own.
- Do not redistribute copyrighted audio assets, ROMs, or raw extracted code.
- Output themes are original algorithmic transformations; do not misrepresent them as verbatim original game tracks.
- Do not bypass DRM.
- Zero telemetry, offline-first architecture.

---

## Workflow

1. **Ghidra** → analyze binary → find music driver functions.
2. Identify the sequence format (header, tempo, opcodes, note events).
3. Write your own parser (Python or Pascal) to convert the sequence into the shape of `game_extract.json`.
4. Run `theme_builder.py` to create new original themes.
5. Run `midi_exporter.py` to listen to the results in any MIDI player or DAW.

---

## Requirements

- Python 3.10+
- Free Pascal (`fpc`) – optional, for the Pascal reader
- Ghidra – optional, for binary analysis

No external Python packages required.
