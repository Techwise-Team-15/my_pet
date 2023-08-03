import pygame
from game_util.scene_items import PetStats

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Save Health Bars Percentages")

    def display_pet_stats_screen(pet_stats):
        # Create a surface to display pet stats
        stats_surface = pygame.Surface((200, 100))
        stats_surface.fill((255, 255, 255))  # White background

        # Get pet stats
        health = pet_stats.get_pet_health()
        thirst = pet_stats.get_pet_thirst()
        hunger = pet_stats.get_pet_hunger()
        happiness = pet_stats.get_pet_happiness()  

        font = pygame.freetype.SysFont(None, 24)
        font.render_to(stats_surface, (10, 10), f"Health: {health}%", (0, 0, 0))
        font.render_to(stats_surface, (10, 30), f"Thirst: {thirst}%", (0, 0, 0))
        font.render_to(stats_surface, (10, 50), f"Hunger: {hunger}%", (0, 0, 0))
        font.render_to(stats_surface, (10, 70), f"Happiness: {happiness}%", (0, 0, 0))

        return stats_surface

   
    running = True
    pet_stats = PetStats()

    while running:
     
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Save health bars when the "S" key is pressed
                if event.key == pygame.K_s:
                    pet_stats.save_health_bars("health_bars.txt")
                # Load health bars when the "L" key is pressed
                elif event.key == pygame.K_l:
                    pet_stats.load_health_bars("health_bars.txt")

        pet_stats.update()
        pet_stats.draw(screen)

      
        stats_surface = display_pet_stats_screen(pet_stats)
        screen.blit(stats_surface, (10, 10))  

        
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
