"""
midi_exporter.py

Converts a new theme JSON into a standard MIDI file with no external
dependencies. Writes the melody track plus a simple drum track.
"""

import json
import struct

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def note_to_midi(note: str) -> int:
    name = note[:-1]
    octave = int(note[-1])
    return NOTE_NAMES.index(name) + (octave + 1) * 12


def variable_length(value: int) -> bytes:
    if value < 0:
        value = 0
    buf = [value & 0x7F]
    value >>= 7
    while value:
        buf.append((value & 0x7F) | 0x80)
        value >>= 7
    return bytes(reversed(buf))


def build_header(ntrks: int, division: int = 480) -> bytes:
    return b"MThd" + struct.pack(">IHHH", 6, 0, ntrks, division)


def build_melody_track(theme: dict, channel: int = 0) -> bytes:
    tempo_bpm = theme["bpm"]
    us_per_quarter = int(60_000_000 / tempo_bpm)

    events = bytearray()

    # Tempo meta event
    events += variable_length(0)
    events += bytes([0xFF, 0x51, 0x03])
    events += struct.pack(">I", us_per_quarter)[1:]

    # Program change (Electric Piano = 4)
    events += variable_length(0)
    events += bytes([0xC0 | channel, 4])

    for step in theme["melody"]:
        pitch = note_to_midi(step["note"])
        dur = int(step["duration_ticks"])

        # Note on
        events += variable_length(0)
        events += bytes([0x90 | channel, pitch, 90])

        # Note off
        events += variable_length(dur)
        events += bytes([0x80 | channel, pitch, 64])

    # End of track
    events += variable_length(0)
    events += bytes([0xFF, 0x2F, 0x00])

    return b"MTrk" + struct.pack(">I", len(events)) + bytes(events)


def build_drum_track(theme: dict, channel: int = 9) -> bytes:
    pattern = theme.get("drum_groove") or {}
    ticks_per_step = 120  # 16 steps * 120 = 1920 ticks = 4 bars at 480 PPQ

    gm = {
        "kick": 36, "snare": 38, "closed_hat": 42, "open_hat": 46,
        "shaker": 70, "rim": 37, "taiko": 47, "hi_hat_roll": 42,
        "808": 35, "low_strings": 36, "timpani": 47,
    }

    events = bytearray()
    total_steps = 16

    for step in range(total_steps):
        hits = []
        for name, steps in pattern.items():
            if step < len(steps) and steps[step] in "xXo":
                if name in gm:
                    velocity = 110 if steps[step] == "X" else 90
                    hits.append((gm[name], velocity))

        if hits:
            for note, vel in hits:
                events += variable_length(0)
                events += bytes([0x90 | channel, note, vel])
            events += variable_length(ticks_per_step - 1)
            for note, _ in hits:
                events += variable_length(0)
                events += bytes([0x80 | channel, note, 64])
            events += variable_length(1)
        else:
            events += variable_length(ticks_per_step)

    events += variable_length(0)
    events += bytes([0xFF, 0x2F, 0x00])

    return b"MTrk" + struct.pack(">I", len(events)) + bytes(events)


def export_midi(theme: dict, filename: str) -> None:
    melody_track = build_melody_track(theme)
    drum_track = build_drum_track(theme)
    header = build_header(ntrks=2, division=480)

    with open(filename, "wb") as f:
        f.write(header)
        f.write(melody_track)
        f.write(drum_track)


if __name__ == "__main__":
    for gid in ("japanese", "classical", "hiphop"):
        with open(f"new_theme_{gid}.json", encoding="utf-8") as f:
            theme = json.load(f)
        out = f"new_theme_{gid}.mid"
        export_midi(theme, out)
        print(f"Exported {out}")
