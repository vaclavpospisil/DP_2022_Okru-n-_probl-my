from dataset_cz import *
import numpy as np
import random
from numpy.random import randint
import math
import pygame
import matplotlib.pyplot as plt

WIDTH, HEIGHT = 1080, 720 # Šířka a výška okna
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT)) # Zobrazení okna
pygame.display.set_caption("Travelling salesman problem - Genetic algorithm") # Popisek okna
FPS = 60 

# Pygame paleta barev
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (127, 127, 127)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

CITIES = 13     # Počet měst
N_POP = 100     # Velikost populace
R_MUT = 0.03    # Pravděpodobnost mutace
R_CROSS = 0.9   # Pravděpodobnost křížení
TS_VEL = 20     # Velikost turnaje
N_GEN = 50      # Počet generací
RUNS = 0
SP = 99999
generations = []
dist = []

CITY_INFO = CITY_INFO_COMPUTE.copy()

# Funkce pro vytvoření okna s finálním řešením
def draw_window():
    WINDOW.fill(BLACK) # Vyplnění okna černou barvou

    # Vypsání hodnoty nejkratší vzdálenosti v okně
    pygame.font.init()
    font = pygame.font.Font(pygame.font.get_default_font(), 25)
    text = font.render("The shortest path has the value: %f" %(shortest_distance), True, WHITE)
    WINDOW.blit(text, (20,HEIGHT-50))

    # Vzájemné propojení všech měst
    for i in range(CITIES):
        for j in range(CITIES):
            if i != j:
                pygame.draw.line(WINDOW, GRAY, (CITY_INFO[i][1], CITY_INFO[i][2]), (CITY_INFO[j][1], CITY_INFO[j][2]), 1)
    # Zvýraznění nejkratší cesty
    for i in range((len(PATH))-1):
        pygame.draw.line(WINDOW, GREEN, (CITY_INFO[PATH[i]][1], CITY_INFO[PATH[i]][2]), (CITY_INFO[PATH[i+1]][1], CITY_INFO[PATH[i+1]][2]), 3)
    pygame.draw.line(WINDOW, GREEN, (CITY_INFO[PATH[(len(PATH))-1]][1], CITY_INFO[PATH[(len(PATH))-1]][2]), (CITY_INFO[PATH[0]][1], CITY_INFO[PATH[0]][2]), 3)
    
    # Zobrazení všech měst
    for i in range(CITIES):
        pygame.draw.circle(WINDOW, RED, (CITY_INFO[i][1], CITY_INFO[i][2]), 7)
    pygame.draw.circle(WINDOW, BLUE, (CITY_INFO[PATH[0]][1], CITY_INFO[PATH[0]][2]), 7) # Počáteční město
    pygame.display.update() # Aktualizace okna

# Výpočet vzdálenosti mezi dvěmi městy
def compute_distance(first, second):
    return math.sqrt((int(CITY_INFO[int(first)][1]) - int(CITY_INFO[int(second)][1]))**2 + int((CITY_INFO[int(first)][2]) - int(CITY_INFO[int(second)][2]))**2)

# Výpočet hodnoty fitness funkce (minimální délka trasy)
def fitness(POP_SET):
    total = 0
    for j in range(CITIES-1):

        first = int(POP_SET[j])
        second = int(POP_SET[j+1])
        total += compute_distance(first, second)

    total += compute_distance(POP_SET[0], second)

    return total

# Vytvoření počáteční populace, která se skládá z N_POP různých cest
def initial_population(CITY_INFO_COMPUTE,N_POP):
    POP_SET = []

    for i in range(N_POP):
        np.random.shuffle(CITY_INFO_COMPUTE)
        SET = []

        for j in range(CITIES):
            SET.append(int(CITY_INFO_COMPUTE[j][0]))

        POP_SET.append(SET)

    return np.array(POP_SET)

# Použití selekce pomocí turnajové selekce
def selection(POP_SET):

    selection_index = random.randint(0, N_POP-1)

    for i in range(TS_VEL):
        index = random.randint(0, N_POP-1)

        if fitness(POP_SET[index]) < fitness(POP_SET[selection_index]):
            selection_index = index

    return POP_SET[selection_index]

# Provedení jednobodového křížení
def crossover(parent_1, parent_2):

    if np.random.rand() < R_CROSS:
        crossover_point = random.randint(0, CITIES)
        cross_1 = parent_1[:crossover_point]
        cross_2 = parent_2[:crossover_point]

        cross_3 = [city for city in parent_2 if city not in cross_1]
        cross_4 = [city for city in parent_1 if city not in cross_2]

        child_1 = np.concatenate((cross_1, cross_3))
        child_2 = np.concatenate((cross_2, cross_4))

    else:
        child_1, child_2 = parent_1.copy(), parent_2.copy()

    return child_1, child_2

# Provedení dvoubodového křížení
def two_point_crossover(parent_1, parent_2):
    if np.random.rand() < R_CROSS:
        crossover_point1 = random.randint(0, CITIES)
        crossover_point2 = random.randint(crossover_point1, CITIES)

        cross_1_start = parent_1[:crossover_point1]
        cross_2_start = parent_2[:crossover_point1]

        cross_1_end = parent_1[crossover_point2:]
        cross_2_end = parent_2[crossover_point2:]

        cross_1_mid = [item for item in parent_2 if item not in cross_1_start and item not in cross_1_end]
        cross_2_mid = [item for item in parent_1 if item not in cross_2_start and item not in cross_2_end]

        child_1 = np.concatenate((cross_1_start,cross_1_mid,cross_1_end))
        child_2 = np.concatenate((cross_2_start,cross_2_mid,cross_2_end))
    else:
        child_1, child_2 = parent_1.copy(), parent_2.copy()

    return child_1, child_2    

# Provedení mutace pomocí vzájemné výměny dvou měst
def mutation(child):
    if np.random.rand() < R_MUT:
        mut_1 = random.randint(0, CITIES-1)
        mut_2 = random.randint(0, CITIES-1)
        mut_city_1 = child[mut_1]
        mut_city_2 = child[mut_2]
        child[mut_1] = mut_city_2
        child[mut_2] = mut_city_1

    return child

# Hlavní cyklus genetického algoritmu
def genetic_algorithm(SP = 99999):
    POP_SET = initial_population(CITY_INFO_COMPUTE, N_POP)
    pop_fitness = np.zeros(N_POP)
    generation = 0
    
    while generation <= N_GEN:

        for i in range(N_POP):
            distance = fitness(POP_SET[i])
            pop_fitness[i] = distance
        min = np.min(pop_fitness)
        min_idx = np.argmin(pop_fitness)

        if min < SP:
            SP = min
            shortest_path = []

            for i in range(CITIES):
                shortest_path.append(int(POP_SET[min_idx][i]))

            shortest_path.append(int(POP_SET[min_idx][0]))

        selected = [selection(POP_SET) for _ in range(N_POP)]
        new_population = []

        for i in range(0, N_POP, 2):
            parent_1, parent_2 = selected[i], selected[i+1]
            child_1, child_2 = two_point_crossover(parent_1, parent_2)
            child_1 = mutation(child_1)
            child_2 = mutation(child_2)
            new_population.append(child_1)
            new_population.append(child_2)
        POP_SET = new_population
        print("Generation: %d, The shortest path has the distance: %f" % (generation, SP))
        generations.append(generation)
        dist.append(SP)
        generation += 1
    
    return shortest_path, SP

# Hlavní Pygame smyčka
def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT: # Při kliknutí na tlačítko X dojde k zavření okna
                run = False

            if event.type == pygame.KEYDOWN: # Při stisknutí klávesy ESC dojde k zavření okna

                if event.key == pygame.K_ESCAPE:
                    run = False

        draw_window()

if __name__ == "__main__":

    # Hlavní smyčka algoritmu
    while RUNS < 1:

        PATH, shortest_distance = genetic_algorithm()

        RUNS += 1

    # Zobrazení výsledků
    print("The shortest path has the distance: %f" % (shortest_distance))
    print("The shortest path is: %s" %(PATH))

    # Vytvoření grafu závislosti hodnoty nejkratší vzdálenosti na počtu generací
    plt.plot(generations, dist, label="Průběh genetického algoritmu")
    plt.xlabel('počet generací')
    plt.ylabel('hodnota nejkratší vzdálenosti')
    plt.legend()
    plt.show()

    CITY_INFO = (CITY_INFO.copy()*2.2)-320 # Upravení matice kvůli lepšímu zobrazení výsledku v Pygame
    main() # Vykreslit výsledek v pygame okně