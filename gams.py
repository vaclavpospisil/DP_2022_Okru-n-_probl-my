import pygame
from dataset_cz import *
# from dataset_50_cities import *

# 13 měst
GAMS_Path = [1, 4, 2, 3, 6, 7, 8, 9, 10, 11, 0, 12, 5, 1]
GAMS_shortest_distance = 1065
# 50 měst
# GAMS_Path = [11, 3, 42, 30, 0, 35, 14, 7, 15, 13, 32, 10, 24, 12, 23, 27, 46, 34, 44, 2, 41, 48, 39, 8, 6, 17, 21, 19, 37, 26, 1, 36, 5, 33, 22, 31, 47, 45, 29, 25, 43, 40, 16, 38, 28, 20, 18, 4, 49, 9, 11]
# GAMS_shortest_distance = 4181

WIDTH, HEIGHT = 1080, 720 # Šířka a výška okna
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT)) # Zobrazení okna
pygame.display.set_caption("Travelling salesman problem - GAMS solution") # Popisek okna
FPS = 60

# Pygame paleta barev
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (127, 127, 127)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Počet měst
CITIES = 13
# CITIES = 50

# Funkce pro vytvoření okna s finálním řešením
def draw_window():
    WINDOW.fill(BLACK) # Vyplnění okna černou barvou

    # Vypsání hodnoty nejkratší vzdálenosti v okně
    pygame.font.init()
    font = pygame.font.Font(pygame.font.get_default_font(), 25)
    text = font.render("The shortest path has the value: %d" %(GAMS_shortest_distance), True, WHITE)
    WINDOW.blit(text, (20,HEIGHT-50))

    # Vzájemné propojení všech měst
    for i in range(CITIES):
        for j in range(CITIES):
            if i != j:
                pygame.draw.line(WINDOW, GRAY, (CITY_INFO_COMPUTE[i][1], CITY_INFO_COMPUTE[i][2]), (CITY_INFO_COMPUTE[j][1], CITY_INFO_COMPUTE[j][2]), 1)
    # Zvýraznění nejkratší cesty
    for i in range((len(GAMS_Path))-1):
        pygame.draw.line(WINDOW, GREEN, (CITY_INFO_COMPUTE[GAMS_Path[i]][1], CITY_INFO_COMPUTE[GAMS_Path[i]][2]), (CITY_INFO_COMPUTE[GAMS_Path[i+1]][1], CITY_INFO_COMPUTE[GAMS_Path[i+1]][2]), 3)
    pygame.draw.line(WINDOW, GREEN, (CITY_INFO_COMPUTE[GAMS_Path[(len(GAMS_Path))-1]][1], CITY_INFO_COMPUTE[GAMS_Path[(len(GAMS_Path))-1]][2]), (CITY_INFO_COMPUTE[GAMS_Path[0]][1], CITY_INFO_COMPUTE[GAMS_Path[0]][2]), 3)
    
    # Zobrazení všech měst
    for i in range(CITIES):
        pygame.draw.circle(WINDOW, RED, (CITY_INFO_COMPUTE[i][1], CITY_INFO_COMPUTE[i][2]), 7)
    pygame.draw.circle(WINDOW, BLUE, (CITY_INFO_COMPUTE[GAMS_Path[0]][1], CITY_INFO_COMPUTE[GAMS_Path[0]][2]), 7) # Počáteční město
    pygame.display.update() # Aktualizace okna

# Pouze při použití se 13 městy
CITY_INFO_COMPUTE = (CITY_INFO_COMPUTE.copy()*2.2)-320 # Upravení matice kvůli lepšímu zobrazení výsledku v Pygame

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