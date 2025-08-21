# Example file showing a basic pygame "game loop"
import pygame
import config
from state_table import StateTable

print(f"Number of columns: {config.COLS}, Number of rows: {config.ROWS}")
last_update_time = 0
pygame.init()
state_table = StateTable(config.ROWS, config.COLS)
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()
running = True
updating = False
font = pygame.font.SysFont(None, 36)
buttons = [
    {"text": "Reset", "rect": pygame.Rect(500, config.HEIGHT - config.BUTTON_HEIGHT, 100, config.BUTTON_HEIGHT)},
    {"text": "Start", "rect": pygame.Rect(700, config.HEIGHT - config.BUTTON_HEIGHT, 100, config.BUTTON_HEIGHT)},
    {"text": "Exit", "rect": pygame.Rect(900, config.HEIGHT - config.BUTTON_HEIGHT, 100, config.BUTTON_HEIGHT)},
]

def draw_grid(stable, buttons):
    screen.fill(config.GRAY)
    pygame.draw.rect(screen, config.LIGHT_GRAY, (0, config.HEIGHT - 50, config.WIDTH, 50))
    mouse_pos = pygame.mouse.get_pos()
    for row in range(config.ROWS + 1):
        y = row * config.CELL_SIZE
        pygame.draw.line(screen, config.WHITE, (0, y), (config.WIDTH, y), 1)

    for col in range(config.COLS + 1):
        x = col * config.CELL_SIZE
        pygame.draw.line(screen, config.WHITE, (x, 0), (x, config.HEIGHT-50), 1)
    for button in buttons:
        rect = button["rect"]
        text = button["text"]
        # mouse hover
        if rect.collidepoint(mouse_pos):
            color = config.BUTTON_HOVER_COLOR
        else:
            color = config.BUTTON_COLOR
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (179, 179, 179), rect, 2)  # 边框

        text_surf = font.render(text, True, config.TEXT_COLOR)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)
    pygame.draw.rect(screen, config.WHITE, (0, 0, config.WIDTH, config.HEIGHT), 1)
    num_rows, num_cols = stable.get_row_column()
    for row in range(num_rows):
        for col in range(num_cols):
            if stable.table[row][col] == 1:
                pygame.draw.rect(screen, config.YELLOW, (col * config.CELL_SIZE, row * config.CELL_SIZE, config.CELL_SIZE, config.CELL_SIZE))

while running:
    current_time = pygame.time.get_ticks()
    if updating:
        if current_time - last_update_time >= config.UPDATE_INTERVAL:
            state_table.update()
            last_update_time = current_time
    draw_grid(state_table, buttons=buttons)
    mouse_pos = pygame.mouse.get_pos()
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // config.CELL_SIZE, pos[0] // config.CELL_SIZE
                if row >= config.ROWS or col >= config.COLS:
                    for button in buttons:
                        if button["rect"].collidepoint(pos):
                            if button["text"] == "Reset":
                                state_table.reset()
                            elif button["text"] == "Start":
                                button["text"] = "Pause"
                                updating = True
                            elif button["text"] == "Pause":
                                button["text"] = "Start"
                                updating = False
                            elif button["text"] == "Exit":
                                running = False
                    continue
                if state_table.get_cell_state(row, col) == 0:
                    state_table.activate(row, col)
                else:
                    state_table.deactivate(row, col)
                print(f"Mouse click position: {pos}")
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()