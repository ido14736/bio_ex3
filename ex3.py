import sys
import numpy as np
import math
import random
import pygame
from hexalattice.hexalattice import *

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

        values_sum = 0
        current_values = []
        for numeric_string in splitted_line[3:]:
            values_sum += int(numeric_string)
            current_values.append((int(numeric_string)/int(splitted_line[2])))
        # splitted_line = [int(numeric_string) for numeric_string in splitted_line]
        input_examples[splitted_line[0]] = [splitted_line[1], current_values]
        others_value = ((int(splitted_line[2]) - values_sum)/int(splitted_line[2]))
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
        first_z = first_vec[i]
        second_z = second_vec[i]
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

#def update_som_first_circle(som, lr, neighborhood, differ, i, j):
#    update = [k * (lr * neighborhood) for k in differ]
#
#    if i < 4:
#        if (i-1) >= 0:
#            if (j-1) >= 0:
#                som[i-1][j-1] = [sum(x) for x in zip(*[som[i-1][j-1], update])]
# #               print(i-1,j-1)
#            if j <= (len(som[i-1]) - 1):
#                som[i-1][j] = [sum(x) for x in zip(*[som[i-1][j], update])]
#    #            print(i-1,j)
#
#        if (j-1) >= 0:
#            som[i][j-1] = [sum(x) for x in zip(*[som[i][j-1], update])]
#            #        print(i,j-1)
#        if (j+1) <= (len(som[i]) - 1):
#            som[i][j+1] = [sum(x) for x in zip(*[som[i][j+1], update])]
#            #        print(i,j+1)
#
#        if (i+1) <= 8:
#            if j <= (len(som[i+1]) - 1):
#                #             print(i+1,j)
#                som[i+1][j] = [sum(x) for x in zip(*[som[i+1][j], update])]
#            if (j+1) <= (len(som[i+1]) - 1):
#                som[i+1][j+1] = [sum(x) for x in zip(*[som[i+1][j+1], update])]
#                #             print(i+1,j+1)
#
#    elif i == 4:
#        if (i-1) >= 0:
#            if j <= (len(som[i-1]) - 1):
#                som[i-1][j] = [sum(x) for x in zip(*[som[i-1][j], update])]
#                #            print(i-1,j)
#            if (j-1) >= 0:
#                som[i-1][j-1] = [sum(x) for x in zip(*[som[i-1][j-1], update])]
#                #           print(i-1,j-1)
#
#        if (j-1) >= 0:
#            som[i][j-1] = [sum(x) for x in zip(*[som[i][j-1], update])]
#            #          print(i,j-1)
#        if (j+1) <= (len(som[i]) - 1):
#            som[i][j+1] = [sum(x) for x in zip(*[som[i][j+1], update])]
#            #          print(i,j+1)
#
#        if (i+1) <= 8:
#            if j <= (len(som[i+1]) - 1):
#                som[i+1][j] = [sum(x) for x in zip(*[som[i+1][j], update])]
#                #           print(i+1,j)
#            if (j-1) >= 0:
#                som[i+1][j-1] = [sum(x) for x in zip(*[som[i+1][j-1], update])]
#                #           print(i+1,j-1)
#
#    elif i > 4:
#        if (i - 1) >= 0:
#            if j <= (len(som[i-1]) - 1):
#                som[i - 1][j] = [sum(x) for x in zip(*[som[i-1][j], update])]
#                #             print(i - 1, j)
#            if (j + 1) <= (len(som[i - 1]) - 1):
#                som[i - 1][j+1] = [sum(x) for x in zip(*[som[i-1][j+1], update])]
#                #              print(i - 1, j+1)
#
#        if (j - 1) >= 0:
#            som[i][j - 1] = [sum(x) for x in zip(*[som[i][j-1], update])]
#            #          print(i, j - 1)
#        if (j + 1) <= (len(som[i]) - 1):
#            som[i][j + 1] = [sum(x) for x in zip(*[som[i][j+1], update])]
#            #          print(i, j + 1)
#
#        if (i + 1) <= 8:
#            if (j-1) >= 0:
#                #                print(i + 1, j-1)
#                som[i + 1][j-1] = [sum(x) for x in zip(*[som[i+1][j-1], update])]
#            if j <= (len(som[i + 1]) - 1):
#                som[i + 1][j] = [sum(x) for x in zip(*[som[i+1][j], update])]
#                #               print(i + 1, j)


def update_som(som, neighborhood, second_neighborhood, differ, i, j):
    update = [k * (neighborhood) for k in differ]
    second_update = [k * (second_neighborhood) for k in differ]

    if i < 4:
        if (i-1) >= 0:
            if (j-1) >= 0:
                som[i-1][j-1] = [sum(x) for x in zip(*[[k * (1-neighborhood) for k in som[i-1][j-1]], update])]

                # second circle
                if (j-2) >= 0:
                   #print(i-1, j-2)
                    som[i - 1][j - 2] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i - 1][j - 2]], second_update])]

                    if (i-2) >= 0:
                        #print(i - 2, j - 2)
                        som[i - 2][j - 2] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i - 2][j - 2]], second_update])]


 #               print(i-1,j-1)
            if j <= (len(som[i-1]) - 1):
                som[i-1][j] = [sum(x) for x in zip(*[[k * (1-neighborhood) for k in som[i-1][j]], update])]

                # second circle
                if (j+1) <= (len(som[i-1]) - 1):
                    #print(i-1, j+1)
                    som[i - 1][j + 1] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i - 1][j + 1]], second_update])]

                    if (i-2) >= 0:
                        if j <= (len(som[i - 2]) - 1):
                            #print(i - 2, j)
                            som[i - 2][j] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i - 2][j]], second_update])]
    #            print(i-1,j)

            if (i-2) >= 0:
                if (j-1) >= 0 and (j-1) <= (len(som[i - 2]) - 1):
                    #print(i - 2, j - 1)
                    som[i - 2][j - 1] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i - 2][j - 1]], second_update])]


        if (j-1) >= 0:
            som[i][j-1] = [sum(x) for x in zip(*[[k * (1-neighborhood) for k in som[i][j-1]], update])]
            if (j-2) >= 0:
                #print(i, j - 2)
                som[i][j - 2] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i][j - 2]], second_update])]
            #        print(i,j-1)
        if (j+1) <= (len(som[i]) - 1):
            som[i][j+1] = [sum(x) for x in zip(*[[k * (1-neighborhood) for k in som[i][j+1]], update])]
            if (j+2) <= (len(som[i]) - 1):
                #print(i, j + 2)
                som[i][j + 2] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i][j + 2]], second_update])]
            #        print(i,j+1)

        if (i+1) <= 8:
            if j <= (len(som[i+1]) - 1):
                #             print(i+1,j)
                som[i+1][j] = [sum(x) for x in zip(*[[k * (1-neighborhood) for k in som[i+1][j]], update])]
                if j - 1 >= 0:
                    #print(i+1, j - 1)
                    som[i + 1][j - 1] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i + 1][j - 1]], second_update])]

                if (i+2) <= 8:
                    if (i+2) > 4:
                        if j - 1 >= 0:
                            #print(i + 2, j - 1)
                            som[i + 2][j - 1] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i + 2][j - 1]], second_update])]
                    else:
                        #print(i + 2, j)
                        som[i + 2][j] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i + 2][j]], second_update])]

            if (j+1) <= (len(som[i+1]) - 1):
                som[i+1][j+1] = [sum(x) for x in zip(*[[k * (1-neighborhood) for k in som[i+1][j+1]], update])]

                if j + 2 <= (len(som[i + 1]) - 1):
                    #print(i + 1, j + 2)
                    som[i + 1][j + 2] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i + 1][j + 2]], second_update])]

                if (i+2) <= 8:
                    if (i+2) > 4:
                        if j+1 <= (len(som[i + 2]) - 1):
                            #print(i + 2, j + 1)
                            som[i + 2][j + 1] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i + 2][j + 1]], second_update])]
                    else:
                        if j + 2 <= (len(som[i + 2]) - 1):
                            #print(i + 2, j + 2)
                            som[i + 2][j + 2] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i + 2][j + 2]], second_update])]

            if (i+2) <= 8:
                if (i + 2) > 4:
                    #print(i + 2, j)
                    som[i + 2][j] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i + 2][j]], second_update])]
                else:
                    if j + 1 <= (len(som[i + 2]) - 1):
                        #print(i + 2, j + 1)
                        som[i + 2][j + 1] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i + 2][j + 1]], second_update])]

                #             print(i+1,j+1)

    elif i == 4:
        if (i-1) >= 0:
            if j <= (len(som[i-1]) - 1):
                som[i-1][j] = [sum(x) for x in zip(*[[k * (1-neighborhood) for k in som[i-1][j]], update])]

                if j+1 <= (len(som[i-1]) - 1):
                    #print(i-1, j+1)
                    som[i - 1][j + 1] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i - 1][j + 1]], second_update])]
                #            print(i-1,j)
            if (j-1) >= 0:
                som[i-1][j-1] = [sum(x) for x in zip(*[[k * (1-neighborhood) for k in som[i-1][j-1]], update])]

                if j-2 >= 0:
                    #print(i-1, j-2)
                    som[i - 1][j - 2] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i - 1][j - 2]], second_update])]
                #           print(i-1,j-1)

            if i-2 >= 0:
                if j-2 >= 0 and j-2 <= (len(som[i-2]) - 1):
                    #print(i - 2, j - 2)
                    som[i - 2][j - 2] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i - 2][j - 2]], second_update])]

                if j-1 >= 0 and j-1 <= (len(som[i-2]) - 1):
                    #print(i - 2, j - 1)
                    som[i - 2][j - 1] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i - 2][j - 1]], second_update])]

                if j >= 0 and j <= (len(som[i-2]) - 1):
                    #print(i - 2, j)
                    som[i - 2][j] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i - 2][j]], second_update])]

        if (j-1) >= 0:
            som[i][j-1] = [sum(x) for x in zip(*[[k * (1-neighborhood) for k in som[i][j-1]], update])]
            if (j-2) >= 0:
                som[i][j - 2] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i][j - 2]], second_update])]
                #print(i, j - 2)
            #          print(i,j-1)
        if (j+1) <= (len(som[i]) - 1):
            som[i][j+1] = [sum(x) for x in zip(*[[k * (1-neighborhood) for k in som[i][j+1]], update])]
            if (j+2) <= (len(som[i]) - 1):
                #print(i, j + 2)
                som[i][j + 2] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i][j + 2]], second_update])]
            #          print(i,j+1)

        if (i+1) <= 8:
            if j <= (len(som[i+1]) - 1):
                som[i+1][j] = [sum(x) for x in zip(*[[k * (1-neighborhood) for k in som[i+1][j]], update])]
                if j+1 <= (len(som[i+1]) - 1):
                    #print(i+1, j + 1)
                    som[i + 1][j + 1] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i + 1][j + 1]], second_update])]
                #           print(i+1,j)
            if (j-1) >= 0:
                som[i+1][j-1] = [sum(x) for x in zip(*[[k * (1-neighborhood) for k in som[i+1][j-1]], update])]
                if j-2 >= 0:
                    #print(i+1, j - 2)
                    som[i + 1][j - 2] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i + 1][j - 2]], second_update])]
                #           print(i+1,j-1)

            if (i+2) <= 8:
                if j - 2 >= 0 and j - 2 <= (len(som[i + 2]) - 1):
                    #print(i + 2, j - 2)
                    som[i + 2][j - 2] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i + 2][j - 2]], second_update])]

                if j - 1 >= 0 and j - 1 <= (len(som[i + 2]) - 1):
                    #print(i + 2, j - 1)
                    som[i + 2][j - 1] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i + 2][j - 1]], second_update])]

                if j >= 0 and j <= (len(som[i + 2]) - 1):
                    #print(i + 2, j)
                    som[i + 2][j] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i + 2][j]], second_update])]

    elif i > 4:
        if (i - 1) >= 0:
            if j <= (len(som[i-1]) - 1):
                som[i - 1][j] = [sum(x) for x in zip(*[[k * (1-neighborhood) for k in som[i-1][j]], update])]
                if j-1 >= 0:
                    #print(i-1, j-1)
                    som[i - 1][j - 1] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i - 1][j - 1]], second_update])]
                #             print(i - 1, j)
            if (j + 1) <= (len(som[i - 1]) - 1):
                som[i - 1][j+1] = [sum(x) for x in zip(*[[k * (1-neighborhood) for k in som[i-1][j+1]], update])]
                if j+2 <= (len(som[i - 1]) - 1):
                    #print(i-1, j+2)
                    som[i - 1][j + 2] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i - 1][j + 2]], second_update])]

            if i-2 >=0:
                if i-2 < 4:
                    if j-1 >= 0 and j-1 <= (len(som[i - 2]) - 1):
                        #print(i - 2, j-1)
                        som[i - 2][j - 1] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i - 2][j - 1]], second_update])]
                else:
                    if j + 2 >= 0 and j + 2 <= (len(som[i - 2]) - 1):
                        #print(i - 2, j + 2)
                        som[i - 2][j + 2] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i - 2][j + 2]], second_update])]

                if j + 1 >= 0 and j + 1 <= (len(som[i - 2]) - 1):
                    #print(i - 2, j + 1)
                    som[i - 2][j + 1] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i - 2][j + 1]], second_update])]

                if j >= 0 and j <= (len(som[i - 2]) - 1):
                    #print(i - 2, j)
                    som[i - 2][j] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i - 2][j]], second_update])]
                #              print(i - 1, j+1)

        if (j - 1) >= 0:
            som[i][j - 1] = [sum(x) for x in zip(*[[k * (1-neighborhood) for k in som[i][j-1]], update])]
            if (j - 2) >= 0:
                #print(i, j-2)
                som[i][j - 2] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i][j - 2]], second_update])]
            #          print(i, j - 1)
        if (j + 1) <= (len(som[i]) - 1):
            som[i][j + 1] = [sum(x) for x in zip(*[[k * (1-neighborhood) for k in som[i][j+1]], update])]
            if (j + 2) <= (len(som[i]) - 1):
                #print(i, j+2)
                som[i][j + 2] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i][j + 2]], second_update])]
            #          print(i, j + 1)

        if (i + 1) <= 8:
            if (j-1) >= 0:
                #                print(i + 1, j-1)
                som[i + 1][j-1] = [sum(x) for x in zip(*[[k * (1-neighborhood) for k in som[i+1][j-1]], update])]

                if (j-2) >= 0:
                    #print(i+1, j-2)
                    som[i + 1][j - 2] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i + 1][j - 2]], second_update])]
            if j <= (len(som[i + 1]) - 1):
                som[i + 1][j] = [sum(x) for x in zip(*[[k * (1-neighborhood) for k in som[i+1][j]], update])]

                if (j+1) <= (len(som[i + 1]) - 1):
                    #print(i+1, j+1)
                    som[i + 1][j + 1] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i + 1][j + 1]], second_update])]

            if (i + 2) <= 8:
                if j-2 >= 0 and j-2 <= (len(som[i+2]) - 1):
                    #print(i + 2, j - 2)
                    som[i + 2][j - 2] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i + 2][j - 2]], second_update])]

                if j-1 >= 0 and j-1 <= (len(som[i+2]) - 1):
                    #print(i + 2, j - 1)
                    som[i + 2][j - 1] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i + 2][j - 1]], second_update])]

                if j >= 0 and j <= (len(som[i+2]) - 1):
                    #print(i + 2, j)
                    som[i + 2][j] = [sum(x) for x in zip(*[[k * (1-second_neighborhood) for k in som[i + 2][j]], second_update])]
                #               print(i + 1, j)

def draw_regular_polygon(surface, color, position, width=0):
    radius = 25
    x, y = position

    pygame.draw.polygon(surface, color, [
        (x + radius * math.sin(2 * math.pi * i / 6),
         y + radius * math.cos(2 * math.pi * i / 6))
        for i in range(6)], width)


def get_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    return r, g, b

def average(lst):
    if lst == []:
        return 0
    return sum(lst) / len(lst)

if __name__ == '__main__':
    # parsing the file - a dict that the keys are the names of the Municipalitys
    # and the value is a pair of the Economic Cluster paid with the rest of the values
    input_examples = parse_file(sys.argv[1])
    num_of_values = len(input_examples[list(input_examples.keys())[0]][1])
    #print(input_examples["Abu Gosh"][1])
    # calculating the averages and standard deviations for every field(every column)
    averages, standard_deviations = get_averages_and_standard_deviations(input_examples)

    # initialzing the som
    som = []
    for i in range(5,10):
        som.append([ [] for _ in range(i) ])
    for i in reversed(range(5,9)):
        som.append([ [] for _ in range(i) ])

    for i in range(num_of_values):
        for j in range(len(som)):
            for k in range(len(som[j])):
                som[j][k] = np.random.dirichlet(np.ones(num_of_values), size=1).tolist()[0]
                #print(sum(som[j][k]))
            #print("next")

    # TODO: change the values
    epochs = 10
    #print(som[0])
    #update_som(som, lr, 0.2, [], 8, 4)

    for ep in range(epochs):
        # for every input line - getting the closest som vector's index and the distance
        for key in input_examples.keys():
            # pair of the closest som vector's index and distance from the current input line
            closest = get_closest_som_vector(input_examples[key][1], som, averages, standard_deviations)
            #print("init:")
            #print("best:", closest, "ecocomy level:", input_examples[key][0])
            #print((input_examples[key][1]))
            #print(som[closest[0][0]][closest[0][1]])
            #for t in som:
            #    print(t)
            differ = np.subtract(input_examples[key][1], som[closest[0][0]][closest[0][1]])
            #for i in range(5):
            #    print("chosen point:", (0, i))
            #    update_som(som, lr, 0.2, 0.1, differ, 0, i)
            #for i in range(6):
            #    print("chosen point:", (1, i))
            #    update_som(som, lr, 0.2, 0.1, differ, 1, i)
            #for i in range(7):
            #    print("chosen point:", (2, i))
            #    update_som(som, lr, 0.2, 0.1, differ, 2, i)
            #for i in range(8):
            #    print("chosen point:", (3, i))
            #    update_som(som, lr, 0.2, 0.1, differ, 3, i)
            #for i in range(9):
            #    print("chosen point:", (4, i))
            #    update_som(som, lr, 0.2, 0.1, differ, 4, i)
            #for i in range(8):
            #    print("chosen point:", (5, i))
            #    update_som(som, lr, 0.2, 0.1, differ, 5, i)
            #for i in range(7):
            #    print("chosen point:", (6, i))
            #    update_som(som, lr, 0.2, 0.1, differ, 6, i)
            #for i in range(6):
            #    print("chosen point:", (7, i))
            #    update_som(som, lr, 0.2, 0.1, differ, 7, i)
            #for i in range(5):
            #    print("chosen point:", (8, i))
            #    update_som(som, lr, 0.2, 0.1, differ, 8, i)
            #print("ok")
            first_update = [i * (0.3) for i in differ]
            first = [i * (0.7) for i in som[closest[0][0]][closest[0][1]]]
            #print(som[closest[0][0]][closest[0][1]])
            #print((input_examples[key][1]))
            #print(first_update)
            som[closest[0][0]][closest[0][1]] = [sum(x) for x in zip(*[first, first_update])]
            #print("after first:")
            #for t in som:
            #    print(t)
            update_som(som, 0.2, 0.1, differ, closest[0][0], closest[0][1])
            #print("after second:")
            #for t in som:
            #    print(t)
            #print(som[closest[0][0]][closest[0][1]])
    #print(som[0])

    final_predictions_per_som_cell = {}

    #init
    for i in range(9):
        if i==0 or i==8:
            for j in range(5):
                final_predictions_per_som_cell[i,j] = []

        elif i==1 or i==7:
            for j in range(6):
                final_predictions_per_som_cell[i,j] = []

        elif i==2 or i==6:
            for j in range(7):
                final_predictions_per_som_cell[i,j] = []

        elif i==3 or i==5:
            for j in range(8):
                final_predictions_per_som_cell[i,j] = []

        elif i==4:
            for j in range(9):
                final_predictions_per_som_cell[i,j] = []


    #print(final_predictions_per_som_cell)
    for t in som:
        print(t)
    # final predictions
    for key in input_examples.keys():
        # pair of the closest som vector's index and distance from the current input line
        closest = get_closest_som_vector(input_examples[key][1], som, averages, standard_deviations)
        final_predictions_per_som_cell[closest[0][0], closest[0][1]].append(int(input_examples[key][0]))
        print("best:", closest, "ecocomy level:", input_examples[key][0])
    #print(final_predictions_per_som_cell)
    # Returns the hex_centers
    hex_centers, _ = create_hex_grid(n=100, crop_circ=4, edge_color=(0, 0, 0), do_plot=True)

    # Creat the output window
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    done = False
    screen.fill((255, 255, 255))
    #print(final_predictions_per_som_cell)
    for i in range(len(hex_centers)):
        #print(i, average(final_predictions_per_som_cell[list(final_predictions_per_som_cell.keys())[i][0], list(final_predictions_per_som_cell.keys())[i][1]]))
        current_avg = average(final_predictions_per_som_cell[list(final_predictions_per_som_cell.keys())[i][0], list(final_predictions_per_som_cell.keys())[i][1]])
        if current_avg == 0:
            r, g, b = 200, 0, 0
        else:
            #print(current_avg, (1-(current_avg/10)))
            r, g, b = 0, 0, (1-(current_avg/10))*255

        #r, g, b = 0,0, 20
        draw_regular_polygon(screen, (r, g, b), hex_centers[i] * 50 + 300, width=0)

        pygame.display.flip()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True


            # first circle updates


            #if closest[0][0] - 1 >= 0:
            #som[closest[0][0]][closest[0][1]] = [sum(x) for x in
                                             #    zip(*[som[closest[0][0]][closest[0][1]], first_update])]

            # TODO: update the som values

    # TODO: final predictions



