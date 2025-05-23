import pygame
import random
import sys

pygame.init()

# Fixed window size
W, H = 1280, 720
TITLEBAR_HEIGHT = 60

screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
pygame.display.set_caption("Tarot Card Reading")

# Load Resources
bg_img = pygame.image.load("background.jpg")
back_img = pygame.image.load("back.jpg")
card_faces = [pygame.image.load(f"{i+1}.jpg") for i in range(22)]
butter_img = pygame.image.load("butter.jpg")
explian_img = pygame.image.load("butter2.jpg")

# Load Text
with open("explain.txt", "r", encoding="utf-8") as f:
    explanations = [line.strip() for line in f.readlines()]

font = pygame.font.SysFont("simhei", 24)

# Record Status
STATE_START = "start"
STATE_CHOOSE = "choose"
STATE_REVEAL = "reveal"
STATE_EXPLAIN = "explain"
state = STATE_START

# Setting button
butter_rect = butter_img.get_rect(center=(W//2, H//2))
explian_rect = explian_img.get_rect(center=(W//2, H - 100))
refresh_btn = pygame.Rect(W - 200, 10, 80, 40)
close_btn = pygame.Rect(W - 100, 10, 80, 40)

# Make the card face into 3 rows, with the numbers in each row being 7, 8, and 7 respectively
cards_per_row = [7, 8, 7]
rows = len(cards_per_row)
visible_left = 50
vertical_spacing = 20

#Function: Make 22 cards fit the window size
def get_card_size_and_positions_auto(back_img, screen_width, screen_height, cards_per_row, rows, visible_left=50, vertical_spacing=20):
    orig_w, orig_h = back_img.get_size()
    max_card_width = float('inf')
    for num_cards in cards_per_row:
        max_width_for_row = (screen_width - (num_cards - 1) * visible_left) / num_cards
        if max_width_for_row < max_card_width:
            max_card_width = max_width_for_row

    scale_ratio = max_card_width / orig_w
    card_w = int(orig_w * scale_ratio)
    card_h = int(orig_h * scale_ratio)

    total_height = rows * card_h + (rows - 1) * vertical_spacing
    start_y = max(TITLEBAR_HEIGHT + 20, (screen_height - total_height) // 2)

    positions = []
    current_y = start_y
    for num_cards in cards_per_row:
        total_row_width = visible_left * (num_cards - 1) + card_w
        start_x = (screen_width - total_row_width) // 2
        for i in range(num_cards):
            x = start_x + i * visible_left
            positions.append((x, current_y))
        current_y += card_h + vertical_spacing

    return (card_w, card_h), positions

(card_w, card_h), positions = get_card_size_and_positions_auto(back_img, W, H, cards_per_row, rows)

# Shuffle the order of the cards
card_indices = list(range(22))
random.shuffle(card_indices)
#Create a variable to obtain the selection card
selected_index = None

# main
running = True
while running:
    screen.blit(pygame.transform.scale(bg_img, (W, H)), (0, 0))

    # Draw the window
    pygame.draw.rect(screen, (30, 30, 30), (0, 0, W, TITLEBAR_HEIGHT))
    title_text = font.render("Tarot Card Reading", True, (255, 255, 255))
    screen.blit(title_text, (20, 15))

    pygame.draw.rect(screen, (180, 180, 180), refresh_btn)
    pygame.draw.rect(screen, (180, 180, 180), close_btn)
    screen.blit(font.render("Return", True, (255, 255, 255)), (refresh_btn.x + 5, refresh_btn.y + 8))
    screen.blit(font.render("Close", True, (255, 255, 255)), (close_btn.x + 10, close_btn.y + 8))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos

            # Close button
            if close_btn.collidepoint(mouse_pos):
                running = False

            # Refresh button
            elif refresh_btn.collidepoint(mouse_pos):
                state = STATE_START
                card_indices = list(range(22))
                random.shuffle(card_indices)
                selected_index = None

            elif state == STATE_START:
                if butter_rect.collidepoint(mouse_pos):
                    state = STATE_CHOOSE

            elif state == STATE_CHOOSE:
                for i, pos in enumerate(positions):
                    rect = pygame.Rect(pos, (card_w, card_h))
                    if rect.collidepoint(mouse_pos):
                        selected_index = i
                        state = STATE_REVEAL
                        break

            elif state == STATE_REVEAL:
                if explian_rect.collidepoint(mouse_pos):
                    state = STATE_EXPLAIN

    #Draw the start window
    if state == STATE_START:
        screen.blit(butter_img, butter_rect)
    # Draw the choose card window
    elif state == STATE_CHOOSE:
        tip_text = font.render("Click on the card you like", True, (255, 255, 255))
        screen.blit(tip_text, (500, TITLEBAR_HEIGHT + 10))
        scaled_back = pygame.transform.scale(back_img, (card_w, card_h))
        for pos in positions:
            screen.blit(scaled_back, pos)

    elif state == STATE_REVEAL:
        scaled_back = pygame.transform.scale(back_img, (card_w, card_h))
        for pos in positions:
            screen.blit(scaled_back, pos)

        if selected_index is not None:
            card_id = card_indices[selected_index]
            face_img = pygame.transform.scale(card_faces[card_id], (card_w, card_h))
            face_rect = face_img.get_rect(center=(W//2, H//2 - 100))
            screen.blit(face_img, face_rect)

        screen.blit(explian_img, explian_rect)
    #Draw the explain window
    elif state == STATE_EXPLAIN:
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (30, 30, 30), (0, 0, W, TITLEBAR_HEIGHT))  # The title bar is still displayed


        screen.blit(title_text, (20, 15))
        pygame.draw.rect(screen, (180, 180, 180), refresh_btn)
        pygame.draw.rect(screen, (180, 180, 180), close_btn)
        screen.blit(font.render("Return", True, (255, 255, 255)), (refresh_btn.x + 8, refresh_btn.y + 8))
        screen.blit(font.render("close", True, (255, 255, 255)), (close_btn.x + 10, close_btn.y + 8))

        if selected_index is not None:
            card_id = card_indices[selected_index]
            face_img = pygame.transform.scale(card_faces[card_id], (card_w, card_h))
            face_rect = face_img.get_rect(center=(W//2, H//2 - 150))
            screen.blit(face_img, face_rect)

            explanation = explanations[card_id]
            # Automatic line break processing
            max_line_width = 600  # You can adjust it according to the window size
            words = explanation.split()
            lines = []
            line = ""
            for word in words:
                test_line = line + word + " "
                test_surf = font.render(test_line, True, (0, 0, 0))
                if test_surf.get_width() <= max_line_width:
                    line = test_line
                else:
                    lines.append(line)
                    line = word + " "
            if line:
                lines.append(line)

            # Render the newline text
            for i, line in enumerate(lines):
                line_surf = font.render(line.strip(), True, (0, 0, 0))
                screen.blit(line_surf, (W // 2 - line_surf.get_width() // 2, H // 2 + 30 + i * 30))
    pygame.display.flip()

pygame.quit()
sys.exit()
