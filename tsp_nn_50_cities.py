from cmath import inf, sqrt
import pygame
import numpy as np
import math
from dataset_50_cities import *

WIDTH, HEIGHT = 1080, 720 # Šířka a výška okna
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT)) # Zobrazení okna
pygame.display.set_caption("Travelling salesman problem - Nearest Neigbour algorithm") # Popisek okna
FPS = 60

# Pygame paleta barev
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (127, 127, 127)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

CITIES = 50 # Počet měst

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
    for i in range((len(Path))-1):
        pygame.draw.line(WINDOW, GREEN, (CITY_INFO[final_Path[i]][1], CITY_INFO[final_Path[i]][2]), (CITY_INFO[final_Path[i+1]][1], CITY_INFO[final_Path[i+1]][2]), 3)
    pygame.draw.line(WINDOW, GREEN, (CITY_INFO[final_Path[(len(Path))-1]][1], CITY_INFO[final_Path[(len(Path))-1]][2]), (CITY_INFO[final_Path[0]][1], CITY_INFO[final_Path[0]][2]), 3)
    
    # Zobrazení všech měst
    for i in range(CITIES):
        pygame.draw.circle(WINDOW, RED, (CITY_INFO[i][1], CITY_INFO[i][2]), 7)
    pygame.draw.circle(WINDOW, BLUE, (CITY_INFO[final_Path[0]][1], CITY_INFO[final_Path[0]][2]), 7) # Počáteční město
    pygame.display.update() # Aktualizace okna

# Algorithmus pro hledání cesty pomocí metody nejbližšího souseda
final_Path = []
shortest_distance = 9999999
runs = []
dist = []
for j in range(CITIES):
    CITY_INFO_COMPUTE = CITY_INFO.copy()
    starting_city = j
    actual_city = starting_city
    Path = []
    Path.append(actual_city)
    Total_distance = 0

    n = 0
    while n < CITIES-1:
        Distances = []

        for i in range(CITIES):
            D = math.sqrt((int(CITY_INFO_COMPUTE[actual_city][1]) - int(CITY_INFO_COMPUTE[i][1]))**2 + int((CITY_INFO_COMPUTE[actual_city][2]) - int(CITY_INFO_COMPUTE[i][2]))**2)
            
            if D == 0:
                D = np.inf
        
            Distances.append(D)

        min = np.min(Distances)
        Total_distance += min
        min_index = Distances.index(min)
        CITY_INFO_COMPUTE[actual_city][1] = 9999999
        CITY_INFO_COMPUTE[actual_city][2] = 9999999
        actual_city = min_index
        Path.append(actual_city)
        n += 1

    Path.append(starting_city)
    LAST_PATH = math.sqrt((int(CITY_INFO[actual_city][1]) - int(CITY_INFO[starting_city][1]))**2 + int((CITY_INFO[actual_city][2]) - int(CITY_INFO[starting_city][2]))**2)
    Total_distance += LAST_PATH
    
    if Total_distance < shortest_distance:
        shortest_distance = Total_distance
        final_Path = Path

    runs.append(j)
    dist.append(Total_distance)

# Zobrazení nejkratší cesty
print(final_Path)

# Hlavní smyčka
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