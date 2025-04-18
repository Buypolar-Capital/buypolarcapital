import itertools

# Define standard tuning
standard_tuning = ["E", "A", "D", "G", "B", "E"]

# Define chromatic scale with enharmonic equivalents
chromatic_scale = {
    "C": "C", "C#": "C#", "Db": "C#", "D": "D", "D#": "D#", "Eb": "D#", "E": "E", "E#": "F", "Fb": "E", "F": "F", "F#": "F#", "Gb": "F#", "G": "G", "G#": "G#", "Ab": "G#", "A": "A", "A#": "A#", "Bb": "A#", "B": "B", "B#": "C", "Cb": "B"
}

# Generate fretboard matrix
fretboard = []
for string in standard_tuning:
    start_index = list(chromatic_scale.keys()).index(string)
    fretboard.append([list(chromatic_scale.keys())[(start_index + fret) % 12] for fret in range(12)])

def print_fretboard():
    print("\nStandard Tuning Fretboard (0-11 frets):")
    for i, row in enumerate(fretboard):
        print(f"String {6-i} ({standard_tuning[i]}):", row)

# Predefined standard chord shapes (CAGED system + extensions)
predefined_chords = {
    "C": [-1, 3, 2, 0, 1, 0],  # Open C
    "A": [0, 0, 2, 2, 2, 0],    # Open A
    "G": [3, 2, 0, 0, 0, 3],    # Open G
    "E": [0, 2, 2, 1, 0, 0],    # Open E
    "D": [-1, -1, 0, 2, 3, 2],  # Open D
    "C7": [-1, 3, 2, 3, 1, 0],  # C dominant 7
    "A7": [0, 0, 2, 0, 2, 0],   # A dominant 7
    "G7": [3, 2, 0, 0, 0, 1],   # G dominant 7
    "E7": [0, 2, 0, 1, 0, 0],   # E dominant 7
    "D7": [-1, -1, 0, 2, 1, 2]  # D dominant 7
}

def shift_chord(chord_vector, shift_frets):
    """Shifts a chord up the neck by a number of frets (for barre/movable shapes)."""
    return [f + shift_frets if f >= 0 else -1 for f in chord_vector]

def get_predefined_chord(chord_name):
    """Returns a predefined chord shape if it exists, handling sharps and flats."""
    if chord_name in chromatic_scale:
        root_note = chromatic_scale[chord_name]
    else:
        print("Invalid chord input.")
        return None
    
    shift_frets = list(chromatic_scale.keys()).index(root_note) - list(chromatic_scale.keys()).index(root_note[0])
    
    if root_note in predefined_chords:
        return shift_chord(predefined_chords[root_note], shift_frets)
    return None

def find_chord_positions(chord_name):
    """Finds all fret positions that contain chord notes, ensuring repetition."""
    chord_notes = ["C", "E", "G"] if chord_name == "C" else []  # Extend for other chords
    positions = []
    
    for string_index in range(6):
        string_positions = []
        for fret in range(12):
            note = fretboard[string_index][fret]
            if note in chord_notes:
                string_positions.append((6 - string_index, fret, note))
        
        if string_positions:
            positions.append(string_positions)  # Keep multiple options per string
    
    return positions

def generate_chord_vectors(chord_positions):
    """Generates all possible chord vectors while ensuring repetition."""
    possible_vectors = []
    
    for combination in itertools.product(*chord_positions):
        vector = [-1] * 6  # Default to muted strings
        
        for string, fret, note in combination:
            vector[6 - string] = fret  # Assign frets to string positions
        
        possible_vectors.append(vector)
    
    return possible_vectors

def filter_playable_chords(chord_vectors):
    """Filters out unplayable chords based on fret span and physical feasibility."""
    playable = []
    
    for vector in chord_vectors:
        active_frets = [f for f in vector if f >= 0]
        if len(active_frets) > 0:
            min_fret, max_fret = min(active_frets), max(active_frets)
            if max_fret - min_fret <= 4:  # Limit stretch to max 4 frets
                playable.append(vector)
    
    return playable

# Get user input for chord
chord_name = input("Enter a chord (C, D, E, F, G, A, B, with # or b for sharps/flats): ").strip().capitalize()

# Try predefined chord first
predefined_chord = get_predefined_chord(chord_name)
if predefined_chord:
    print(f"\nPredefined {chord_name} chord:")
    print(predefined_chord)
else:
    # Process chord dynamically
    print_fretboard()
    chord_positions = find_chord_positions(chord_name)
    print(f"\nAll chord note positions for {chord_name}:")
    print(chord_positions)

    chord_vectors = generate_chord_vectors(chord_positions)
    print("\nGenerated chord vectors:")
    for v in chord_vectors[:5]:  # Print first 5 options for readability
        print(v)

    playable_chords = filter_playable_chords(chord_vectors)
    print("\nPlayable chord options:")
    for v in playable_chords[:5]:  # Print first 5 playable versions
        print(v)