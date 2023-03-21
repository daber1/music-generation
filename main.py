# Import libraries
import math
import random

import mido
import music21


# This section contains functions that represent different chords.

def major_triad(root_key):
    """
    Create a major triad
    :param root_key: The root key of the chord
    :return: A major triad
    """
    return [root_key, root_key + 4, root_key + 7]


def minor_triad(root_key):
    """
    Create a minor triad
    :param root_key: The root key of the chord
    :return: A minor triad
    """
    return [root_key, root_key + 3, root_key + 7]


def first_inversion_major(root_key):
    """
    Create a first inversion major triad
    :param root_key: The root key of the chord
    :return: A first inversion major triad
    """
    return [root_key + 12, root_key + 4, root_key + 7]


def first_inversion_minor(root_key):
    """
    Create a first inversion minor triad
    :param root_key: The root key of the chord
    :return: A first inversion minor triad
    """
    return [root_key + 12, root_key + 3, root_key + 7]


def second_inversion_major(root_key):
    """
    Create a second inversion major triad
    :param root_key: The root key of the chord
    :return: A second inversion major triad
    """
    return [root_key + 12, root_key + 16, root_key + 7]


def second_inversion_minor(root_key):
    """
    Create a second inversion minor triad
    :param root_key: The root key of the chord
    :return: A second inversion minor triad
    """
    return [root_key + 12, root_key + 15, root_key + 7]


def diminished_chord(root_key):
    """
    Create a diminished chord
    :param root_key: The root key of the chord
    :return: A diminished chord
    """
    return [root_key, root_key + 3, root_key + 6]


def sus2(root_key):
    """
    Create a sus2 chord
    :param root_key: The root key of the chord
    :return: A sus2 chord
    """
    return [root_key, root_key + 2, root_key + 7]


def sus4(root_key):
    """
    Create a sus4 chord
    :param root_key: The root key of the chord
    :return: A sus4 chord
    """
    return [root_key, root_key + 5, root_key + 7]


def void(root_key):
    """
    Create a void chord
    :return: None
    """
    return [-(root_key // root_key) for _ in range(3)]


#####################################################################

# Global variables

notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B", "B#"]

chords = [major_triad, minor_triad, first_inversion_major, first_inversion_minor, second_inversion_major,
          second_inversion_minor, diminished_chord, sus2, sus4]
key, octave, melody = list(), 0, list()


# Utility functions

def get_key(midi_file):
    """
    Get the key of the midi file
    :param midi_file:
    :return key: The key of the midi file
    """
    score = music21.converter.parse(midi_file)
    local_key = score.analyze('key')
    return local_key.tonic.name, local_key.mode


def note_to_midi_number(note):
    """
    Convert a note to a midi number
    :param note: The note
    :return: The midi number
    """
    return 12 * octave + notes.index(note)


def get_scale():
    scale = []

    major_keys = [
        ['C', ['C', 'D', 'E', 'F', 'G', 'A', 'B']],
        ['C#', ['C#', 'D#', 'E#', 'F#', 'G#', 'A#', 'B#']],
        ['D', ['D', 'E', 'F#', 'G', 'A', 'B', 'C#']],
        ['D#', ['D#', 'F', 'G', 'G#', 'A#', 'C', 'D']],
        ['E', ['E', 'F#', 'G#', 'A', 'B', 'C#', 'D#']],
        ['F', ['F', 'G', 'A', 'A#', 'C', 'D', 'E']],
        ['F#', ['F#', 'G#', 'A#', 'B', 'C#', 'D#', 'E#']],
        ['G', ['G', 'A', 'B', 'C', 'D', 'E', 'F#']],
        ['G#', ['G#', 'A#', 'B#', 'C#', 'D#', 'E#', 'F#']],
        ['A', ['A', 'B', 'C#', 'D', 'E', 'F#', 'G#']],
        ['A#', ['A#', 'C', 'D', 'D#', 'F', 'G', 'A']],
        ['B', ['B', 'C#', 'D#', 'E', 'F#', 'G#', 'A#']]
    ]
    minor_keys = [
        ['C', ['C', 'D', 'D#', 'F', 'G', 'G#', 'A#']],
        ['C#', ['C#', 'D#', 'E', 'F#', 'G#', 'A', 'B']],
        ['D', ['D', 'E', 'F', 'G', 'A', 'A#', 'C']],
        ['D#', ['D#', 'F', 'F#', 'G#', 'A#', 'B', 'C#']],
        ['E', ['E', 'F#', 'G', 'A', 'B', 'C', 'D']],
        ['F', ['F', 'G', 'G#', 'A#', 'C', 'C#', 'D#']],
        ['F#', ['F#', 'G#', 'A', 'B', 'C#', 'D', 'E']],
        ['G', ['G', 'A', 'A#', 'C', 'D', 'D#', 'F']],
        ['G#', ['G#', 'A#', 'B', 'C#', 'D#', 'E', 'F#']],
        ['A', ['A', 'B', 'C', 'D', 'E', 'F', 'G']],
        ['A#', ['A#', 'C', 'C#', 'D#', 'F', 'F#', 'G#']],
        ['B', ['B', 'C#', 'D', 'E', 'F#', 'G', 'A']]
    ]
    if key[1] == 'major':
        for i in major_keys:
            if i[0] == key[0]:
                scale = i[1]
    else:
        for i in minor_keys:
            if i[0] == key[0]:
                scale = i[1]
    return [note_to_midi_number(note) for note in scale]


def parse_midi_to_list(midi_file):
    """
    Parse a midi file to a list of notes
    :param midi_file: The midi file
    :return: A list of notes
    """
    midi = mido.MidiFile(midi_file)
    return [msg.note for msg in midi if msg.type == 'note_on']


def time_of_the_melody(midi_file):
    """
    Calculate the time of the melody
    :param midi_file: The midi file
    :return: The time of the melody
    """
    midi = mido.MidiFile(midi_file)
    time = 0
    for track in midi.tracks:
        for msg in track:
            if msg.time:
                time += msg.time
    return time


# EA functions

def create_individual(length):
    """
    Create an individual that is a list of chords
    :param length: The length of the individual
    :return: A random individual
    """
    # For better results it was decided to use an octave to generate the chords within the octave
    individual = []
    for i in range(length):
        individual.append(random.choice(chords + [void])(random.randint(octave * 12, octave * 12 + 11)))
    return individual


def create_population(size, length):
    """
    Create a population
    :param size: The size of the population
    :param length: The length of the individual
    :return: A population
    """
    return [create_individual(length) for _ in range(size)]


def mutation(individual):
    """
    Mutate an individual
    :param individual: The individual to mutate
    :return: The mutated individual
    """
    index = random.randint(0, len(individual) - 1)
    ind = individual[index]
    if fitness([ind]) < 0:
        individual[index] = random.choice(chords + [void])(random.randint(octave * 12, octave * 12 + 11))
    return individual


def crossover(individual1, individual2):
    """
    Crossover two individuals
    :param individual1: The first individual
    :param individual2: The second individual
    :return: The crossovered individuals
    """
    child1 = individual1[:len(individual1) // 2] + individual2[len(individual2) // 2:]
    child2 = individual2[:len(individual2) // 2] + individual1[len(individual1) // 2:]
    return child1, child2


def evolution(population):
    """
    Evolve a population
    :param population: The population to evolve
    :return: The evolved population
    """
    new_population = []
    for i in range(len(population)):
        new_population.append(mutation(random.choice(population)))
    for i in range(len(population) // 2):
        child1, child2 = crossover(random.choice(population), random.choice(population))
        new_population.append(child1)
        new_population.append(child2)
    return new_population


def selection(population):
    """
    Select the best individuals
    :param population: The population
    :return: The best individuals
    """
    population = sorted(population, key=lambda x: fitness(x), reverse=True)
    return population[:len(population) // 2]


def fitness(individual):
    """
    Compute the fitness of an individual
    :param individual: The individual
    :return: The fitness
    """
    score = 0
    score += notes_exist(individual)
    score += check_scale(individual)
    score += check_octave(individual)
    score += check_similarity(individual)
    return score


def notes_exist(individual):
    """
    Check if the individual contains existing notes
    :param individual: The individual
    :return: The score
    """
    score = 0
    for chord in individual:
        for note in chord:
            if note in range(128):
                continue
            else:
                score -= 1000000  # We should not have a note that does not exist
    return score


def check_scale(individual):
    """
    Check if the individual contains notes that are in the scale
    :param individual: The individual
    :return: The score
    """
    score = 0
    scale = get_scale()
    for chord in individual:
        for i in range(len(chord)):
            note = chord[i]
            if note in scale:
                continue
            else:
                if i == 0:
                    if note - 12 in scale:
                        continue
                if i == 1:
                    if note - 12 in scale:
                        continue
                score -= 100  # A note that is not in the scale will be penalized
    # Check that the appropriate chord is chosen
    for chord in individual:
        if chord[0] in scale:
            if key[1] == "major":
                if scale.index(chord[0]) in [0, 1, 4, 5]:
                    # it can be major chord and suses(SUS2, SUS4)
                    if chord == major_triad(chord[0]) or chord == sus2(chord[0]) or chord == sus4(chord[0]):
                        continue
                    else:
                        score -= 1000

                elif scale.index(chord[0]) == 2:
                    # it can be minor chord and SUS4
                    if chord == minor_triad(chord[0]) or chord == sus4(chord[0]):
                        continue
                    else:
                        score -= 1000
                elif scale.index(chord[0]) == 3:
                    # it can be major chord and SUS2
                    if chord == major_triad(chord[0]) or chord == sus2(chord[0]):
                        continue
                    else:
                        score -= 1000
                elif scale.index(chord[0]) == 6:
                    # it can be diminished chord
                    if chord == diminished_chord(chord[0]):
                        continue
                    else:
                        score -= 1000
            else:
                if scale.index(chord[0]) in [0, 2, 3, 6]:
                    # it can be minor chord and suses(SUS2, SUS4)
                    if chord == minor_triad(chord[0]) or chord == sus2(chord[0]) or chord == sus4(chord[0]):
                        continue
                    else:
                        score -= 1000
                elif scale.index(chord[0]) == 1:
                    # it can be diminished chord
                    if chord == diminished_chord(chord[0]):
                        continue
                    else:
                        score -= 1000
                elif scale.index(chord[0]) == 4:
                    # it can be minor chord and SUS4
                    if chord == minor_triad(chord[0]) or chord == sus4(chord[0]):
                        continue
                    else:
                        score -= 1000
                elif scale.index(chord[0]) == 5:
                    # it can be major chord and SUS2
                    if chord == major_triad(chord[0]) or chord == sus2(chord[0]):
                        continue
                    else:
                        score -= 1000
        elif chord[0] - 12 in scale:
            if key[1] == "major":
                if scale.index(chord[0] - 12) in [0, 1, 2, 3, 4, 5] or scale.index(chord[0] - 12) in [0, 1, 2, 3, 4, 5]:
                    # it can be inversions of major
                    if chord == first_inversion_major(chord[0] - 12) or chord == second_inversion_major(chord[0] - 12):
                        continue
                    else:
                        score -= 1000
                else:
                    score -= 1000
            else:
                if scale.index(chord[0] - 12) in [0, 2, 3, 4, 5, 6] or scale.index(chord[0] - 12) in [0, 2, 3, 4, 5, 6]:
                    # it can be minor chord, inversions of it and suses(SUS2, SUS4)
                    if chord == first_inversion_minor(chord[0] - 12) or chord == second_inversion_minor(chord[0] - 12):
                        continue
                    else:
                        score -= 1000
                else:
                    score -= 1000
    return score


def check_octave(individual):
    """
    Check if the individual contains notes that are in the same octave
    :param individual: The individual
    :return: The score
    """
    score = 0
    for chord in individual:
        chord_octave = max(chord) // 12
        # If the octave of the generated chord is higher than octave of the original melody, that is not good
        if chord_octave > octave:
            score -= 100 * math.fabs(chord_octave - octave)
    return score


def check_similarity(individual):
    """
    Check if the individual contains notes that are similar to the previous note
    :param individual: The individual
    :return: The score
    """
    score = 0
    for i in range(len(individual)):
        if i == 0:
            continue
        else:
            for note in individual[i]:
                if note in individual[i - 1]:
                    score += 300
    return score


def create_midi_file(best_individual, midi_file_name):
    """
    Create a midi file from an individual
    :param best_individual: The individual
    :param midi_file_name: The name of the midi file
    :return: The midi file
    """
    original = mido.MidiFile(midi_file_name)
    midi = mido.MidiFile()
    track = mido.MidiTrack()
    midi.tracks.append(original.tracks[0])
    midi.tracks.append(original.tracks[1])
    # After several hundreds of generations, it was found that the best individual sounds
    # way better if the octave is lowered down by 1
    track.append(mido.Message('program_change', program=0, time=0))
    rest = 0
    for chord in best_individual:
        if chord == void:
            rest += 1
        else:
            for i in range(len(chord)):
                track.append(mido.Message('note_on', note=chord[i] - 12, velocity=45, time=rest * 384))

            for i in range(len(chord)):
                track.append(mido.Message('note_off', note=chord[i] - 12, velocity=45, time=0 if i > 0 else 384))

    midi.tracks.append(track)
    midi.ticks_per_beat = original.ticks_per_beat
    midi.save(
        f"VladislavLopatovskiiOutput{midi_file_name[midi_file_name.find('input') + 5:].split('.')[0]}-"
        f"{key[0]}{'m' if key[1] == 'minor' else ''}.mid")


def main(midi_file_name):
    # Global variables for the melody
    global key
    global octave
    global melody
    # Get the key of the midi file
    key = get_key(midi_file_name)
    # Get the notes of the midi file
    melody = parse_midi_to_list(midi_file_name)

    octave = min(melody) // 12

    # The length of the individual is the number of the chords (4 for each bar)
    length = math.ceil(time_of_the_melody(midi_file_name) / 1536) * 4
    # Create the population
    population = create_population(size_of_population, length)

    for i in range(number_of_generations):
        population = selection(population)
        population = evolution(population)
        if (i + 1) % (number_of_generations//10) == 0:
            fits = [fitness(individual) for individual in population]
            print(f'Generation {i + 1}/{number_of_generations} : {max(fits)} : {min(fits)} : {sum(fits) / len(fits)}')

    # Get the best individual
    best_individual = sorted(population, key=lambda x: fitness(x), reverse=True)[0]
    # Create the midi file
    create_midi_file(best_individual, midi_file_name)


if __name__ == '__main__':
    input_name = input("Please, enter the name of the input midi file(e.g. 'inputN.mid'): ")
    choice = input("Do you want to use the default hyper-parameters? (y/n): ")
    if choice == 'y':
        # Hyper-parameters
        size_of_population = 100
        number_of_generations = 300
        main(input_name)
    else:
        # Hyper-parameters
        size_of_population = int(input("Please, enter the size of the population: "))
        number_of_generations = int(input("Please, enter the number of generations: "))
        main(input_name)
