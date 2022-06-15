import math
import sys

import pygame
from hexalattice.hexalattice import *

# TODO: change the values
SOM_SIZE = 61
EPOCHS = 10
LR = 0.0001


# Parsing the input file (csv file)
# Returns a dictionary:
# The keys are the names of the Municipalitys
# The value is a pair of the Economic Cluster value with the rest of the given values
def parse_file(file_path):
    file = open(file_path, 'r')
    lines = file.readlines()

    data = {}
    for i in range(1, len(lines)):
        line = lines[i].split(',')

        # removing '\n'
        line[-1] = line[-1][:-1]

        # line = [int(numeric_string) for numeric_string in line]
        data[line[0]] = [line[1], [int(numeric_string) for numeric_string in line[3:]]]
        others_value = int(line[2]) - sum(data[line[0]][1])
        data[line[0]][1].append(others_value)

    return data


# Returns the values per category
def get_values(data):
    values_per_category = [[] for _ in range(len(data[list(data.keys())[0]][1]))]
    for key in data.keys():
        for j in range(len(data[key][1])):
            values_per_category[j].append(data[key][1][j])

    return values_per_category


# Calculating the standard deviations
def get_standard_deviations(data):
    values_per_category = get_values(data)

    standard_deviations = []
    for i in range(len(values_per_category)):
        standard_deviations.append(np.std(values_per_category[i]))
    return standard_deviations


# Calculating the averages
def get_averages(data):
    values_per_category = get_values(data)

    averages = []
    for i in range(len(values_per_category)):
        averages.append(sum(values_per_category[i]) / len(data))

    return averages


# Calculating the distance between two given vectors
def calculate_distance(first_vec, second_vec, averages, standard_deviations):
    distance = 0
    for i in range(len(first_vec)):
        first_z = (first_vec[i] - averages[i]) / standard_deviations[i]
        second_z = (second_vec[i] - averages[i]) / standard_deviations[i]
        distance += pow((first_z - second_z), 2)

    return pow(distance, 0.5)


# Getting the closest som vector to the input example vector
def get_closest_som_vector(example_vec, som, averages, standard_deviations):
    best = [-1, 0]
    for i in range(len(som)):
        for j in range(len(som[i])):
            current_distance = calculate_distance(example_vec, som[i][j], averages, standard_deviations)
            # initializing the best with the values for the first som vector
            if i == 0 and j == 0:
                best = [[i, j], current_distance]
            else:
                if current_distance < best[1]:
                    best = [[i, j], current_distance]

    return best


def initialing_som():
    som = []

    for i in range(5, 10):
        som.append([[] for _ in range(i)])

    for i in reversed(range(5, 9)):
        som.append([[] for _ in range(i)])

    for i in range(len(averages)):
        for j in range(len(som)):
            for k in range(len(som[j])):
                current_category_value = np.random.normal(averages[i], standard_deviations[i])
                if current_category_value < 0:
                    som[j][k].append(-1 * current_category_value)
                else:
                    som[j][k].append(current_category_value)

    return som


def draw_regular_polygon(surface, color, position, width=0):
    radius = 25
    x, y = position

    pygame.draw.polygon(surface, color, [
        (x + radius * math.sin(2 * math.pi * i / 6),
         y + radius * math.cos(2 * math.pi * i / 6))
        for i in range(6)], width)


if __name__ == '__main__':

    data = parse_file(sys.argv[1])

    # Calculating the averages and standard deviations for every field(every column)
    averages = get_averages(data)
    standard_deviations = get_standard_deviations(data)

    # Initialing the SOM network
    som = initialing_som()

    for epoch in range(EPOCHS):
        # for every input line - getting the closest som vector's index and the distance
        for key in data.keys():
            # pair of the closest som vector's index and distance from the current input line
            closest = get_closest_som_vector(data[key][1], som, averages, standard_deviations)
            # TODO: update the som values

    # Returns the hex_centers
    hex_centers, _ = create_hex_grid(n=100, crop_circ=4, edge_color=(0, 0, 0), do_plot=True)

    # Creat the output window
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    done = False
    screen.fill((255, 255, 255))

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        for hex in hex_centers:
            draw_regular_polygon(screen, (0, 0, 255), hex*50 + 300, width=0)

        pygame.display.flip()
