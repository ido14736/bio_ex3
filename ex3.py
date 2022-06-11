import sys
import numpy as np


som_size = 61


# parsing the input csv file
def parse_file(filepath):
    file1 = open(filepath, 'r')
    lines = file1.readlines()

    input_examples = {}
    for i in range(1, len(lines)):
        splitted_line = lines[i].split(',')

        # removing '\n'
        splitted_line[-1] = splitted_line[-1][:-1]

        # splitted_line = [int(numeric_string) for numeric_string in splitted_line]
        input_examples[splitted_line[0]] = [splitted_line[1], [int(numeric_string) for numeric_string in splitted_line[3:]]]
        others_value = int(splitted_line[2]) - sum(input_examples[splitted_line[0]][1])
        input_examples[splitted_line[0]][1].append(others_value)

    return input_examples


# calculating the averages and standard deviations
def get_averages_and_standard_deviations(input_examples):
    values_per_category = [ [] for _ in range(len(input_examples[list(input_examples.keys())[0]][1])) ]

    for key in input_examples.keys():
        for j in range(len(input_examples[key][1])):
            values_per_category[j].append(input_examples[key][1][j])

    averages = []
    for i in range(len(values_per_category)):
        averages.append(sum(values_per_category[i]) / len(input_examples))

    standard_deviations = []
    for i in range(len(values_per_category)):
        standard_deviations.append(np.std(values_per_category[i]))
    return averages, standard_deviations


# calculating the distance between two vectors
def calculate_distance(first_vec, second_vec, averages, standard_deviations):
    distance = 0
    for i in range(len(first_vec)):
        first_z = (first_vec[i] - averages[i]) / standard_deviations[i]
        second_z = (second_vec[i] - averages[i]) / standard_deviations[i]
        distance += pow((first_z - second_z), 2)
    return pow(distance, 0.5)


# getting the closest som vector to the input example vector
def get_closest_som_vector(example_vec, som, averages, standard_deviations):
    best = [-1, 0]
    for i in range(len(som)):
        for j in range(len(som[i])):
            #print("som",som[i][j])
            current_distance = calculate_distance(example_vec, som[i][j], averages, standard_deviations)
            #print([i,j], current_distance)
            # initializing the best with the values for the first som vector
            if i == 0 and j == 0:
                best = [[i,j], current_distance]
            else:
                if current_distance < best[1]:
                    best = [[i,j], current_distance]

    return best


if __name__ == '__main__':
    # parsing the file - a dict that the keys are the names of the Municipalitys
    # and the value is a pair of the Economic Cluster paid with the rest of the values
    input_examples = parse_file(sys.argv[1])

    # calculating the averages and standard deviations for every field(every column)
    averages, standard_deviations = get_averages_and_standard_deviations(input_examples)

    # initialzing the som
    som = []
    for i in range(5,10):
        som.append([ [] for _ in range(i) ])
    for i in reversed(range(5,9)):
        som.append([ [] for _ in range(i) ])

    for i in range(len(averages)):
        for j in range(len(som)):
            for k in range(len(som[j])):
                current_category_value = np.random.normal(averages[i], standard_deviations[i])
                if current_category_value < 0:
                    som[j][k].append(-1 * current_category_value)
                else:
                    som[j][k].append(current_category_value)

    # TODO: change the values
    epochs = 10
    lr = 0.0001

    for ep in range(epochs):
        # for every input line - getting the closest som vector's index and the distance
        for key in input_examples.keys():
            # pair of the closest som vector's index and distance from the current input line
            closest = get_closest_som_vector(input_examples[key][1], som, averages, standard_deviations)
            # TODO: update the som values

    # TODO: final predictions



