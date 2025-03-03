import random
from midiutil.MidiFile import MIDIFile

def generate_blues_riff():
    # Create a MIDI file with 1 track
    midi = MIDIFile(1)
    
    # Track parameters
    track = 0
    channel = 0
    tempo = 120  # BPM
    volume = 100  # 0-127
    time = 0  # Start at the beginning
    
    midi.addTrackName(track, time, "12-Bar Blues")
    midi.addTempo(track, time, tempo)
    
    # Blues scales (in C)
    c_blues_scale = [36, 39, 40, 41, 43, 46, 48]  # C, Eb, E, F, G, Bb, C (octave up)
    
    # Common 12-bar blues progression in C: C7-F7-C7-G7-F7-C7
    chord_progression = [
        'C7', 'C7', 'C7', 'C7',  # 4 bars of C7
        'F7', 'F7', 'C7', 'C7',  # 2 bars of F7, 2 bars of C7
        'G7', 'F7', 'C7', 'C7'   # 1 bar of G7, 1 bar of F7, 2 bars of C7
    ]
    
    # Root notes for each chord
    chord_roots = {
        'C7': 36,  # C
        'F7': 41,  # F
        'G7': 43   # G
    }
    
    # Generate a note pattern for each bar
    beat_duration = 0.5  # 8th notes
    
    for bar, chord in enumerate(chord_progression):
        root = chord_roots[chord]
        
        # 8 eighth notes per bar (4/4 time)
        for beat in range(8):
            # Different note patterns based on current beat and chord
            if beat == 0:
                # Start with root note on the 1
                note = root
            elif random.random() < 0.6:
                # Use notes from the blues scale with tendency toward chord tones
                note = random.choice(c_blues_scale)
            else:
                # Occasionally use chord tones
                if chord == 'C7':
                    note = random.choice([36, 40, 43, 46])  # C E G Bb
                elif chord == 'F7':
                    note = random.choice([41, 45, 48, 51])  # F A C Eb
                elif chord == 'G7':
                    note = random.choice([43, 47, 50, 53])  # G B D F
            
            # Add the note to the track
            duration = beat_duration
            # Sometimes hold a note longer
            if random.random() < 0.2:
                duration *= 2
                
            # Add note to MIDI file
            midi.addNote(track, channel, note, time + (bar * 4) + (beat * beat_duration), 
                         duration, volume)
    
    # Add a final tonic note
    midi.addNote(track, channel, 36, time + 48, 2, volume)
    
    return midi

def create_random_blues(filename="random_blues_riff.mid"):
    # Generate a random blues riff
    midi = generate_blues_riff()
    
    # Save the MIDI file
    with open(filename, "wb") as output_file:
        midi.writeFile(output_file)
    
    print(f"Blues riff saved as {filename}")

# Usage
if __name__ == "__main__":
    # Generate a single riff
    create_random_blues()
    
    # Or generate multiple riffs with different filenames
    for i in range(3):
        create_random_blues(f"blues_riff_{i+1}.mid")
