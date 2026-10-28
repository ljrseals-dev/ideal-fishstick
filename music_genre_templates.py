"""
music_genre_templates.py

Complete style templates for Japanese pop/city pop, classical, and hip-hop.
Used by theme_builder.py to transform extracted game sequences into new,
original themes that follow the style rules.
"""

from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, Tuple, List


@dataclass
class Section:
    name: str
    bars: int
    purpose: str


@dataclass
class InstrumentRole:
    name: str
    role: str
    range_hint: str
    articulation: str


@dataclass
class DrumPattern:
    name: str
    steps: int
    pattern: Dict[str, str]
    feel: str


@dataclass
class ChordProgression:
    name: str
    roman: Tuple[str, ...]
    example_key: str
    example_chords: Tuple[str, ...]
    use: str


@dataclass
class GenreTemplate:
    genre_id: str
    display_name: str
    family: str
    summary: str
    bpm_range: Tuple[int, int]
    time_signature: str
    swing: str
    common_keys: Tuple[str, ...]
    scales: Tuple[str, ...]
    chord_progressions: Tuple[ChordProgression, ...]
    sections: Tuple[Section, ...]
    instruments: Tuple[InstrumentRole, ...]
    drum_grooves: Tuple[DrumPattern, ...]
    melody_notes: Tuple[str, ...]
    harmony_notes: Tuple[str, ...]
    rhythm_notes: Tuple[str, ...]
    production_notes: Tuple[str, ...]
    lyric_or_flow_notes: Tuple[str, ...] = ()
    substyle_notes: Tuple[str, ...] = ()


def drum(name: str, feel: str, pattern: Dict[str, str]) -> DrumPattern:
    for k, v in pattern.items():
        if len(v) != 16:
            raise ValueError(f"{k} must have 16 steps: {v!r}")
        if set(v) - set("xXo-g"):
            raise ValueError(f"{k} has bad characters: {v!r}")
    return DrumPattern(name=name, steps=16, pattern=pattern, feel=feel)


JAPANESE_STYLE = GenreTemplate(
    genre_id="japanese",
    display_name="Japanese Pop / City Pop with Traditional Color",
    family="Japanese popular music",
    summary="Broad Japanese pop template with optional traditional color.",
    bpm_range=(88, 128),
    time_signature="4/4",
    swing="straight or light 8th-note swing",
    common_keys=("C major", "D major", "F major", "A minor", "D minor"),
    scales=("major", "natural minor", "major pentatonic", "minor pentatonic", "hirajoshi"),
    chord_progressions=(
        ChordProgression("royal_road", ("IVmaj7", "V7", "iii7", "vi7"),
                         "C major", ("Fmaj7", "G7", "Em7", "Am7"), "J-pop chorus"),
        ChordProgression("city_pop", ("IVmaj7", "III7", "vi7", "v7", "I7"),
                         "C major", ("Fmaj7", "E7", "Am7", "Gm7", "C7"), "City pop"),
        ChordProgression("traditional", ("i", "iv", "V7", "i"),
                         "D minor", ("Dm", "Gm", "A7", "Dm"), "Traditional color"),
    ),
    sections=(
        Section("Intro", 4, "Set mood"),
        Section("A-melo", 8, "Verse"),
        Section("B-melo", 8, "Pre-chorus"),
        Section("Chorus", 8, "Hook"),
        Section("Interlude", 4, "Color"),
        Section("Outro", 4, "Fade"),
    ),
    instruments=(
        InstrumentRole("Rhodes", "Chord stabs", "mid", "Soft attack"),
        InstrumentRole("Synth bass", "Root and fifth", "low", "Legato"),
        InstrumentRole("Clean guitar", "Arpeggios", "mid-high", "Chorus"),
        InstrumentRole("Koto", "Traditional color", "high-mid", "Plucked"),
    ),
    drum_grooves=(
        drum("city_pop", "steady", {
            "kick": "x---x---x---x---", "snare": "----x-------x---",
            "closed_hat": "x-x-x-x-x-x-x-x-", "open_hat": "----x-------x---"}),
        drum("jpop", "light", {
            "kick": "x---x---x---x---", "snare": "----x-------x---",
            "closed_hat": "x-x-x-x-x-x-x-x-", "shaker": "x-x-x-x-x-x-x-x-"}),
    ),
    melody_notes=("Pentatonic phrases", "Chorus jumps up", "Repeated motifs"),
    harmony_notes=("Major 7th and 9th", "Royal road for chorus", "Minor iv color"),
    rhythm_notes=("Steady verse", "Open chorus", "Light syncopation"),
    production_notes=("Warm lows", "Chorus guitar", "Short room reverb"),
    lyric_or_flow_notes=("Even syllables", "Clear chorus phrase"),
    substyle_notes=("City pop: smooth chords", "J-pop: strong chorus"),
)

CLASSICAL = GenreTemplate(
    genre_id="classical",
    display_name="Western Classical Music",
    family="Classical",
    summary="Common-practice classical template with motif development.",
    bpm_range=(60, 132),
    time_signature="4/4 or 3/4",
    swing="none",
    common_keys=("C major", "G major", "D major", "F major", "A minor", "D minor"),
    scales=("major", "natural minor", "harmonic minor", "melodic minor", "dorian", "lydian"),
    chord_progressions=(
        ChordProgression("authentic", ("I", "IV", "V7", "I"),
                         "C major", ("C", "F", "G7", "C"), "Basic phrase"),
        ChordProgression("minor_cadence", ("i", "iv", "V7", "i"),
                         "A minor", ("Am", "Dm", "E7", "Am"), "Minor phrase"),
        ChordProgression("circle", ("I", "vi", "ii", "V7", "I"),
                         "C major", ("C", "Am", "Dm", "G7", "C"), "Forward motion"),
    ),
    sections=(
        Section("Introduction", 8, "Set key"),
        Section("Exposition", 16, "Themes"),
        Section("Development", 16, "Develop motif"),
        Section("Recapitulation", 16, "Return themes"),
        Section("Coda", 8, "Close"),
    ),
    instruments=(
        InstrumentRole("Violin I", "Lead melody", "high", "Legato, staccato"),
        InstrumentRole("Cello", "Bass melody", "low-mid", "Legato, pizzicato"),
        InstrumentRole("Horn", "Warm harmony", "mid", "Legato"),
        InstrumentRole("Timpani", "Rhythmic accent", "low", "Rolls, hits"),
    ),
    drum_grooves=(
        drum("timpani", "classical", {
            "timpani": "X-------X-------", "low_strings": "X---X---X---X---"}),
    ),
    melody_notes=("Build motif", "Sequence and inversion", "Clear cadence"),
    harmony_notes=("Diatonic first", "Secondary dominants", "Counterpoint"),
    rhythm_notes=("Rhythmic motifs", "Augmentation", "Rests"),
    production_notes=("Hall reverb", "Natural dynamics", "Balanced sections"),
    substyle_notes=("Sonata form", "Theme and variations", "Waltz 3/4"),
)

HIPHOP = GenreTemplate(
    genre_id="hiphop",
    display_name="Hip-Hop / Rap / Trap",
    family="Hip-hop",
    summary="Boom bap, rap, and trap template with swing or half-time feel.",
    bpm_range=(70, 170),
    time_signature="4/4",
    swing="boom bap: light swing; trap: straight 16ths",
    common_keys=("A minor", "C minor", "D minor", "E minor", "F minor"),
    scales=("natural minor", "harmonic minor", "phrygian", "minor pentatonic", "blues scale"),
    chord_progressions=(
        ChordProgression("dark_minor", ("i", "VI", "III", "VII"),
                         "A minor", ("Am", "F", "C", "G"), "Trap loop"),
        ChordProgression("boom_bap", ("ii7", "V7", "Imaj7", "vi7"),
                         "C major", ("Dm7", "G7", "Cmaj7", "Am7"), "Boom bap"),
        ChordProgression("phrygian", ("i", "bII", "i", "bVII"),
                         "E minor", ("Em", "F", "Em", "D"), "Dark trap"),
    ),
    sections=(
        Section("Intro", 4, "Tag"),
        Section("Verse", 16, "Rap"),
        Section("Hook", 8, "Chant"),
        Section("Bridge", 8, "Change energy"),
        Section("Outro", 4, "Fade"),
    ),
    instruments=(
        InstrumentRole("808 bass", "Sub bass", "low", "Long glide"),
        InstrumentRole("Kick", "Low punch", "low", "Short"),
        InstrumentRole("Snare", "Backbeat", "mid-high", "Crisp"),
        InstrumentRole("Hi-hat", "Timekeeping", "high", "Short or roll"),
    ),
    drum_grooves=(
        drum("boom_bap", "swing", {
            "kick": "x-----x-x-----x-", "snare": "----x-------x---",
            "closed_hat": "x-x-x-x-x-x-x-x-"}),
        drum("trap", "half-time", {
            "kick": "x-----x---x-----", "snare": "----x-------x---",
            "closed_hat": "x-x-x-x-x-x-x-x-", "hi_hat_roll": "x-xx-xx-x-xx-xx-",
            "808": "x-----x---x-----"}),
    ),
    melody_notes=("Short loop", "Minor pentatonic", "Space for vocal"),
    harmony_notes=("Minor loops", "One or two chords", "Jazz for boom bap"),
    rhythm_notes=("Boom bap swing", "Half-time trap", "Triplet flows"),
    production_notes=("Tune 808", "Sidechain 808", "Forward vocal"),
    lyric_or_flow_notes=("Dense boom bap", "Triplet trap", "Short hook"),
    substyle_notes=("Boom bap 85-95", "Trap 130-170"),
)

TEMPLATES: Dict[str, GenreTemplate] = {
    t.genre_id: t for t in (JAPANESE_STYLE, CLASSICAL, HIPHOP)
}


def get_template(genre_id: str) -> GenreTemplate:
    key = genre_id.lower().strip()
    if key not in TEMPLATES:
        raise KeyError(f"Unknown genre {genre_id!r}. Choose: {', '.join(TEMPLATES)}")
    return TEMPLATES[key]


def list_templates() -> List[Tuple[str, str]]:
    return [(gid, t.display_name) for gid, t in TEMPLATES.items()]


def template_to_dict(template: GenreTemplate) -> dict:
    return asdict(template)
