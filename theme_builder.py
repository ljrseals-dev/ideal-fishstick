"""
theme_builder.py

Reads a game sequence extract, applies style rules, and writes a new,
original theme. The new theme follows the style traits (BPM, scale, chords,
drums, melody notes) but uses a completely different note choice.
"""

import json
import random
from typing import Dict, List, Tuple

from music_genre_templates import get_template, list_templates

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

SCALE_INTERVALS = {
    "major": [0, 2, 4, 5, 7, 9, 11],
    "natural minor": [0, 2, 3, 5, 7, 8, 10],
    "harmonic minor": [0, 2, 3, 5, 7, 8, 11],
    "melodic minor": [0, 2, 3, 5, 7, 9, 11],
    "major pentatonic": [0, 2, 4, 7, 9],
    "minor pentatonic": [0, 3, 5, 7, 10],
    "blues scale": [0, 3, 5, 6, 7, 10],
    "dorian": [0, 2, 3, 5, 7, 9, 10],
    "lydian": [0, 2, 4, 6, 7, 9, 11],
    "mixolydian": [0, 2, 4, 5, 7, 9, 10],
    "phrygian": [0, 1, 3, 5, 7, 8, 10],
    "hirajoshi": [0, 2, 3, 7, 8],
}


def note_to_pitch(note: str) -> int:
    name = note[:-1]
    octave = int(note[-1])
    return NOTE_NAMES.index(name) + (octave + 1) * 12


def pitch_to_note(pitch: int) -> str:
    octave = pitch // 12 - 1
    name = NOTE_NAMES[pitch % 12]
    return f"{name}{octave}"


def key_to_root(key: str) -> int:
    root = key.split()[0]
    return NOTE_NAMES.index(root)


def make_scale_pitches(root: int, scale_name: str) -> List[int]:
    intervals = SCALE_INTERVALS[scale_name]
    pitches = []
    for octave in range(2, 7):
        for interval in intervals:
            pitch = (octave + 1) * 12 + root + interval
            if 36 <= pitch <= 96:
                pitches.append(pitch)
    return sorted(set(pitches))


def load_extract(filepath: str) -> dict:
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def build_theme(extract: dict, genre_id: str, seed: int = 42) -> dict:
    template = get_template(genre_id)
    rng = random.Random(seed)

    new_key = rng.choice(template.common_keys)
    new_scale = rng.choice(template.scales)
    root = key_to_root(new_key)
    scale_pitches = make_scale_pitches(root, new_scale)

    progression = rng.choice(template.chord_progressions)
    groove = rng.choice(template.drum_grooves) if template.drum_grooves else None

    original = extract["extracted_rhythm"]
    new_melody = []
    for i, step in enumerate(original):
        orig_pitch = note_to_pitch(step["note"])
        degree = orig_pitch % 7
        target_octave = orig_pitch // 12
        candidates = [p for p in scale_pitches if p // 12 == target_octave]
        if not candidates:
            candidates = scale_pitches
        chosen = candidates[degree % len(candidates)]
        new_melody.append({
            "note": pitch_to_note(chosen),
            "duration_ticks": step["duration_ticks"],
        })

    # Resolve to root
    new_melody[-1]["note"] = pitch_to_note(root + 60)

    new_bpm = rng.randint(template.bpm_range[0], template.bpm_range[1])
    if "boom bap" in template.swing:
        new_bpm = max(85, min(95, new_bpm))
    elif "trap" in template.swing.lower():
        new_bpm = max(130, min(170, new_bpm))

    return {
        "title": f"Original Theme in {new_key}",
        "style": template.display_name,
        "style_id": genre_id,
        "bpm": new_bpm,
        "time_signature": template.time_signature,
        "key": new_key,
        "scale": new_scale,
        "chord_progression": list(progression.example_chords),
        "drum_groove": groove.pattern if groove else None,
        "drum_name": groove.name if groove else None,
        "melody": new_melody,
        "production_notes": list(template.production_notes),
        "harmony_notes": list(template.harmony_notes),
        "rhythm_notes": list(template.rhythm_notes),
    }


def save_theme(theme: dict, filepath: str) -> None:
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(theme, f, indent=2, ensure_ascii=False)


def main():
    print("Reading game extract...")
    extract = load_extract("game_extract.json")
    print(f"  Source: {extract['source_game']}")
    print(f"  Notes: {len(extract['extracted_rhythm'])}")

    print("\nBuilding new themes:")
    for gid, name in list_templates():
        print(f"  - {name}")
        theme = build_theme(extract, gid, seed=100)
        filename = f"new_theme_{gid}.json"
        save_theme(theme, filename)
        print(f"    Saved: {filename}")
        print(f"    Key: {theme['key']}  Scale: {theme['scale']}  BPM: {theme['bpm']}")

    print("\nDone.")


if __name__ == "__main__":
    main()
