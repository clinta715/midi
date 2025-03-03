import random
from midiutil.MidiFile import MIDIFile

def generate_jazz_bassline():
    # Create a MIDI file with 1 track
    midi = MIDIFile(1)
    
    # Track parameters
    track = 0
    channel = 0
    tempo = 130  # BPM - medium swing tempo
    volume = 95  # 0-127
    time = 0  # Start at the beginning
    
    midi.addTrackName(track, time, "Jazz Walking Bass")
    midi.addTempo(track, time, tempo)
    
    # Common jazz ii-V-I progression in C, Bb, and F with some extensions
    progressions = [
        # ii-V-I in C
        [('Dm7', 1), ('G7', 1), ('Cmaj7', 2)],
        # ii-V-I in Bb with turnaround
        [('Cm7', 1), ('F7', 1), ('Bbmaj7', 1), ('Bdim7', 1)],
        # I-VI-ii-V in F
        [('Fmaj7', 1), ('D7', 1), ('Gm7', 1), ('C7', 1)],
        # Jazz blues in F
        [('F7', 2), ('Bb7', 2), ('F7', 2), ('Cm7', 1), ('F7', 1), ('Bbmaj7', 1), ('Bdim7', 1)]
    ]
    
    # Randomly choose a progression
    progression = random.choice(progressions)
    
    # Define chord tones for each chord type
    chord_types = {
        'maj7': [0, 4, 7, 11],      # 1, 3, 5, 7
        '7': [0, 4, 7, 10],         # 1, 3, 5, b7
        'm7': [0, 3, 7, 10],        # 1, b3, 5, b7
        'dim7': [0, 3, 6, 9],       # 1, b3, b5, bb7
        '7b9': [0, 4, 7, 10, 13],   # 1, 3, 5, b7, b9
        'm7b5': [0, 3, 6, 10]       # 1, b3, b5, b7
    }
    
    # Map chord symbols to root notes and chord types
    chord_map = {
        'Cmaj7': (48, 'maj7'),      # C
        'Dm7': (50, 'm7'),          # D
        'D7': (50, '7'),            # D7
        'Ebmaj7': (51, 'maj7'),     # Eb
        'Em7': (52, 'm7'),          # E
        'Fmaj7': (53, 'maj7'),      # F
        'F7': (53, '7'),            # F7
        'Gm7': (55, 'm7'),          # G
        'G7': (55, '7'),            # G7
        'Abmaj7': (56, 'maj7'),     # Ab
        'Am7': (57, 'm7'),          # A
        'Bbmaj7': (58, 'maj7'),     # Bb
        'Bb7': (58, '7'),           # Bb7
        'Bm7b5': (59, 'm7b5'),      # B
        'Bdim7': (59, 'dim7'),      # B
        'Cm7': (48, 'm7')           # C minor
    }
    
    # Quarter note duration
    quarter_note = 1.0
    
    current_time = 0
    last_note = None
    
    # Generate our walking bass line through the chord progression
    for chord_info in progression:
        chord, bars = chord_info
        root, chord_type = chord_map[chord]
        
        # Get chord tones relative to root
        relative_chord_tones = chord_types[chord_type]
        
        # Create absolute chord tones
        chord_tones = [root + note for note in relative_chord_tones]
        
        # For each bar of this chord
        for bar in range(bars):
            # For each beat in the bar (4/4 time)
            for beat in range(4):
                # Determine note selection strategy based on beat position
                if beat == 0:
                    # Root on beat 1 (most of the time)
                    if random.random() < 0.8:
                        note = root
                    else:
                        # Occasionally use 5th or 3rd on beat 1
                        note = chord_tones[random.choice([1, 2])]
                elif beat == 3:
                    # Last beat often leads to the next chord
                    if bar == bars - 1 and progression.index(chord_info) < len(progression) - 1:
                        # Get the root of the next chord
                        next_chord, _ = progression[progression.index(chord_info) + 1]
                        next_root, _ = chord_map[next_chord]
                        
                        # Leading options
                        options = []
                        
                        # Approach from below (half step)
                        options.append(next_root - 1)
                        
                        # Approach from above (half step)
                        options.append(next_root + 1)
                        
                        # Approach from below (whole step)
                        options.append(next_root - 2)
                        
                        # Fifth of current chord
                        options.append(root + 7)
                        
                        note = random.choice(options)
                    else:
                        # Choose from chord tones or approach tones
                        note_choice = random.random()
                        if note_choice < 0.6:
                            note = random.choice(chord_tones)
                        elif note_choice < 0.8:
                            # Chromatic approach from below
                            next_note_options = [n for n in chord_tones if n > last_note]
                            if next_note_options:
                                note = random.choice(next_note_options) - 1
                            else:
                                note = last_note + 1  # Move up chromatically
                        else:
                            # Scalar or arpeggiated movement
                            note = last_note + random.choice([2, 3, 4])
                            # Keep in reasonable range
                            while note > root + 12:
                                note -= 12
                else:
                    # Beats 2 and 3 - standard walking bass choices
                    note_choice = random.random()
                    
                    if note_choice < 0.5:
                        # Use chord tones
                        note = random.choice(chord_tones)
                    elif note_choice < 0.75:
                        # Use approach tone
                        approach_dir = random.choice([-1, 1])
                        note = last_note + approach_dir
                    elif note_choice < 0.9:
                        # Use scale tone (diatonic)
                        scale_steps = [0, 2, 4, 5, 7, 9, 11]
                        scale_tone = random.choice(scale_steps)
                        note = (root % 12) + scale_tone
                        # Adjust octave to be near the last note
                        while note < last_note - 6:
                            note += 12
                        while note > last_note + 6:
                            note -= 12
                    else:
                        # Occasional larger interval for interest
                        interval = random.choice([5, 7, -4, -5])
                        note = last_note + interval
                
                # Keep notes in a reasonable bass range (E1 to G3)
                while note < 28:  # E1
                    note += 12
                while note > 55:  # G3
                    note -= 12
                
                # Add some subtle swing feel for jazz
                duration = quarter_note * 0.95  # Slightly detached articulation
                
                # Add the note to the MIDI file
                midi.addNote(track, channel, note, current_time, duration, volume)
                
                # Update time and last note
                current_time += quarter_note
                last_note = note
    
    # Add a final tonic note (use the first chord's root)
    first_chord = progression[0][0]
    first_root, _ = chord_map[first_chord]
    midi.addNote(track, channel, first_root, current_time, quarter_note * 2, volume)
    
    return midi

def create_jazz_bassline(filename="jazz_bassline.mid"):
    # Generate a random jazz bassline
    midi = generate_jazz_bassline()
    
    # Save the MIDI file
    with open(filename, "wb") as output_file:
        midi.writeFile(output_file)
    
    print(f"Jazz bassline saved as {filename}")

# Usage
if __name__ == "__main__":
    # Generate a single bassline
    create_jazz_bassline()
    
    # Or generate multiple basslines with different filenames
    for i in range(3):
        create_jazz_bassline(f"jazz_bassline_{i+1}.mid")
