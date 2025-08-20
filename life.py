# Example file showing a basic pygame "game loop"
import pygame
from state_table import StateTable

# pygame setup
GRAY = (126, 126, 126)
YELLOW = (255, 252, 79)
WHITE = (255, 255, 255)
CELL_SIZE = 22
COLS = 70
ROWS = 40
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE + 50
BUTTON_HEIGHT = 50
BUTTON_COLOR = (31, 82, 147)
BUTTON_HOVER_COLOR = (150, 150, 150)
TEXT_COLOR = (255, 255, 255)
LIGHT_GRAY = (179, 179, 179)
UPDATE_INTERVAL = 500
last_update_time = 0
print(f"Number of columns: {COLS}, Number of rows: {ROWS}")
pygame.init()
state_table = StateTable(ROWS, COLS)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()
running = True
updating = False
font = pygame.font.SysFont(None, 36)
buttons = [
    {"text": "Reset", "rect": pygame.Rect(500, HEIGHT - BUTTON_HEIGHT, 100, BUTTON_HEIGHT)},
    {"text": "Start", "rect": pygame.Rect(700, HEIGHT - BUTTON_HEIGHT, 100, BUTTON_HEIGHT)},
    {"text": "Exit", "rect": pygame.Rect(900, HEIGHT - BUTTON_HEIGHT, 100, BUTTON_HEIGHT)},
]

def draw_grid(stable, buttons):
    screen.fill(GRAY)
    pygame.draw.rect(screen, LIGHT_GRAY, (0, HEIGHT - 50, WIDTH, 50))
    mouse_pos = pygame.mouse.get_pos()
    for row in range(ROWS + 1):
        y = row * CELL_SIZE
        pygame.draw.line(screen, WHITE, (0, y), (WIDTH, y), 1)

    for col in range(COLS + 1):
        x = col * CELL_SIZE
        pygame.draw.line(screen, WHITE, (x, 0), (x, HEIGHT-50), 1)
    for button in buttons:
        rect = button["rect"]
        text = button["text"]
        # 判断鼠标是否悬停
        if rect.collidepoint(mouse_pos):
            color = BUTTON_HOVER_COLOR
        else:
            color = BUTTON_COLOR
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (179, 179, 179), rect, 2)  # 边框

        # 渲染文字
        text_surf = font.render(text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)
    pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, HEIGHT), 1)
    num_rows, num_cols = stable.get_row_column()
    for row in range(num_rows):
        for col in range(num_cols):
            if stable.table[row][col] == 1:
                pygame.draw.rect(screen, YELLOW, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

while running:
    current_time = pygame.time.get_ticks()
    if updating:
        if current_time - last_update_time >= UPDATE_INTERVAL:
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
                row, col = pos[1] // CELL_SIZE, pos[0] // CELL_SIZE
                if row >= ROWS or col >= COLS:
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
                print(f"鼠标点击了: {pos}")
    # fill the screen with a color to wipe away anything from last frame
    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()