import mido
import random
import argparse
from mido import MidiFile, MidiTrack, Message

def generate_chords(key='C', mode='major', num_chords=8, bpm=60):
    scales = {
        'major': [0, 2, 4, 5, 7, 9, 11],
        'minor': [0, 2, 3, 5, 7, 8, 10],
        'lydian': [0, 2, 4, 6, 7, 9, 11],
        'mixolydian': [0, 2, 4, 5, 7, 9, 10]
    }

    key_offsets = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}

    root_offset = key_offsets.get(key, 0)
    scale = [(note + root_offset) % 12 for note in scales.get(mode, scales['major'])]

    chords = []
    for _ in range(num_chords):
        root = random.choice(scale)
        chord_type = random.choice([(0, 4, 7), (0, 3, 7), (0, 4, 9), (0, 5, 9)])  # Major, Minor, 9th, Sus2
        chord = [(root + interval) % 12 + 48 for interval in chord_type]  # Map to MIDI range
        chords.append(chord)

    return chords

def create_midi_file(chords, filename='ambient_chords.mid', bpm=60):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    tick_per_beat = mid.ticks_per_beat
    note_duration = int((60 / bpm) * tick_per_beat * 2)  # Sustain notes for 2 beats

    for chord in chords:
        for note in chord:
            track.append(Message('note_on', note=note, velocity=64, time=0))
        track.append(Message('note_off', note=chord[0], velocity=64, time=note_duration))
        for note in chord[1:]:
            track.append(Message('note_off', note=note, velocity=64, time=0))

    mid.save(filename)
    print(f"MIDI file saved as {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate ambient-style MIDI chord sequences.')
    parser.add_argument('--key', type=str, default='C', help='Key of the sequence (default: C)')
    parser.add_argument('--mode', type=str, default='major', choices=['major', 'minor', 'lydian', 'mixolydian'], help='Scale mode (default: major)')
    parser.add_argument('--num_chords', type=int, default=8, help='Number of chords to generate (default: 8)')
    parser.add_argument('--bpm', type=int, default=60, help='Tempo in BPM (default: 60)')
    parser.add_argument('--output', type=str, default='ambient_chords.mid', help='Output MIDI filename (default: ambient_chords.mid)')

    args = parser.parse_args()
    chords = generate_chords(args.key, args.mode, args.num_chords, args.bpm)
    create_midi_file(chords, args.output, args.bpm)
