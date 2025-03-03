import random
from midiutil.MidiFile import MIDIFile

def generate_funk_bassline():
    # Create a MIDI file with 1 track
    midi = MIDIFile(1)
    
    # Track parameters
    track = 0
    channel = 0
    tempo = 110  # BPM - typical funk tempo
    volume = 100  # 0-127
    time = 0  # Start at the beginning
    
    midi.addTrackName(track, time, "Funk Bassline")
    midi.addTempo(track, time, tempo)
    
    # E Dorian scale (common for funk)
    e_dorian_scale = [40, 42, 43, 45, 47, 49, 50, 52]  # E F# G A B C# D E
    
    # Common funk chord progression (2 bars each)
    # Em7-A7-Dmaj7-Bm7 progression (common in funk)
    chord_progression = [
        'Em7', 'Em7', 'A7', 'A7', 
        'Dmaj7', 'Dmaj7', 'Bm7', 'Bm7'
    ]
    
    # Root notes for each chord
    chord_roots = {
        'Em7': 40,   # E
        'A7': 45,    # A
        'Dmaj7': 38, # D
        'Bm7': 47    # B
    }
    
    # Chord tones
    chord_tones = {
        'Em7': [40, 43, 47, 50],    # E G B D
        'A7': [45, 49, 52, 43],     # A C# E G
        'Dmaj7': [38, 42, 45, 49],  # D F# A C#
        'Bm7': [47, 50, 54, 57]     # B D F# A
    }
    
    # 16th note duration
    sixteenth_note = 0.25
    
    # Common funk rhythmic patterns (represented as 16th note positions in a bar)
    # 1 = play note, 0 = rest
    funk_patterns = [
        [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0],  # Classic funk rhythm
        [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],  # Syncopated pattern
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],  # Another common pattern
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0],  # With 16th notes
        [1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0]   # Heavily syncopated
    ]
    
    # Generate our bassline through the chord progression
    current_time = 0
    
    for bar, chord in enumerate(chord_progression):
        root = chord_roots[chord]
        chord_tone_set = chord_tones[chord]
        
        # Choose a rhythmic pattern for this bar
        pattern = random.choice(funk_patterns)
        
        # Sometimes introduce variation in the pattern
        if random.random() < 0.3:
            # Modify the pattern slightly
            mod_index = random.randint(0, 15)
            pattern[mod_index] = 1 - pattern[mod_index]  # Toggle between 0 and 1
        
        # Generate notes based on the pattern
        for i, hit in enumerate(pattern):
            if hit:
                # Determine note choice strategy
                note_choice = random.random()
                
                if i == 0 or (i % 4 == 0 and random.random() < 0.8):
                    # Emphasize root notes on strong beats (especially the 1)
                    note = root
                elif note_choice < 0.6:
                    # Chord tones are common
                    note = random.choice(chord_tone_set)
                elif note_choice < 0.9:
                    # Scale tones for passing notes
                    note = random.choice(e_dorian_scale)
                else:
                    # Occasional chromatic approach notes
                    approach_options = [n + 1 for n in chord_tone_set] + [n - 1 for n in chord_tone_set]
                    note = random.choice(approach_options)
                
                # Determine note duration and articulation
                if random.random() < 0.7:
                    # Regular note
                    duration = sixteenth_note * 0.8  # Slightly detached for funk feel
                    volume_adj = 0
                elif random.random() < 0.85:
                    # Emphasized note (like a "slap")
                    duration = sixteenth_note * 0.6  # Shorter, punchier
                    volume_adj = 15  # Louder
                else:
                    # Ghost note
                    duration = sixteenth_note * 0.5
                    volume_adj = -30  # Quieter
                
                # Add the note to the MIDI file
                midi.addNote(track, channel, note, current_time, duration, 
                             min(127, max(1, volume + volume_adj)))
            
            # Move time forward by a 16th note
            current_time += sixteenth_note
    
    # Add a final tonic note
    midi.addNote(track, channel, 40, current_time, 1, volume)
    
    return midi

def create_funk_bassline(filename="funk_bassline.mid", bars=4):
    # Generate a random funk bassline
    midi = generate_funk_bassline()
    
    # Save the MIDI file
    with open(filename, "wb") as output_file:
        midi.writeFile(output_file)
    
    print(f"Funk bassline saved as {filename}")

# Usage
if __name__ == "__main__":
    # Generate a single bassline
    create_funk_bassline()
    
    # Or generate multiple basslines with different filenames
    for i in range(3):
        create_funk_bassline(f"funk_bassline_{i+1}.mid")
