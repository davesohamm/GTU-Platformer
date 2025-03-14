import os
import random
import math
import sys
import pygame
from os import listdir
from os.path import isfile, join

pygame.init()

pygame.display.set_caption("Escape GTU")

WIDTH, HEIGHT = 1000, 800
FPS = 120
PLAYER_VEL = 5
offset_x = 0
offset_y = 0
block_size = 96
window = pygame.display.set_mode((WIDTH, HEIGHT))
# Define custom event for apple collisions
APPLE_COLLISION_EVENT = pygame.USEREVENT + 1
TELEPORT_LOCATION = (-1000, -1000)
checkpoint2_distance = 14350
required_score = 100

# Load the icon image
icon_path = os.path.join('assets', 'icon.ico')  # Path to your icon image
icon_image = pygame.image.load(icon_path)

# Set the icon
pygame.display.set_icon(icon_image)

pygame.mixer.init()

# Load music files
pygame.mixer.music.load('assets/music/loop1.mp3')
doublejump_sound = pygame.mixer.Sound('assets/music/doublejump.mp3')
gameover_sound = pygame.mixer.Sound('assets/music/gameover.mp3')
score_sound = pygame.mixer.Sound('assets/music/score.mp3')

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def start_menu(window):
    title_font = pygame.font.Font('escapegtu.ttf', 130)
    start_font = pygame.font.Font('escapegtu.ttf', 36)
    start_pressed = False

    while not start_pressed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_pressed = True

        # Create a background image for the start menu (You should replace this with your actual background)
        background_image = pygame.image.load("gtu1.jpg")
        window.blit(background_image, (0, 0))

        # Draw the game title
        title_text = title_font.render("Escape GTU", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 5))
        window.blit(title_text, title_rect)

        # Draw a "Start" button
        start_text = start_font.render("Press SPACE to Start", True, (0, 0, 0))
        start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 1.25))
        window.blit(start_text, start_rect)

        pygame.display.update()

def game_over_screen(window):
    # Font for game over message
    font = pygame.font.Font('escapegtu.ttf', 60)
    
    # Display "GAME OVER" message with black rectangle background
    game_over_text = font.render("GAME OVER", True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    pygame.draw.rect(window, (0, 0, 0), game_over_rect.inflate(20, 10))  # Black rectangle background
    window.blit(game_over_text, game_over_rect)

    # Load game over death picture
    death_image = pygame.image.load(r"assets\Other\dead.png").convert_alpha()
    death_image = pygame.transform.scale(death_image, (200, 200))

    # Display the game over death picture on top of "GAME OVER"
    death_rect = death_image.get_rect(midbottom=(WIDTH // 2, game_over_rect.top - 20))
    window.blit(death_image, death_rect)
    
    # Display "Press SPACE to restart" message with black rectangle background
    restart_font = pygame.font.Font('escapegtu.ttf', 36)
    restart_text = restart_font.render("Press SPACE to restart", True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 1.5))
    pygame.draw.rect(window, (0, 0, 0), restart_rect.inflate(20, 10))  # Black rectangle background
    window.blit(restart_text, restart_rect)
    
    pygame.display.update()

def load_background(image_path, window):
    # Load the image
    background = pygame.image.load(image_path).convert()
    # Scale to the window size if needed
    background = pygame.transform.scale(background, (window.get_width(), window.get_height()))
    return background


CHARACTERS = ["MaskDude", "NinjaFrog", "PinkMan","VirtualGuy"]
def select_character(window, CHARACTERS):
    
    # Load background image
    char_menu_bg = load_background("assets/Background/menubg.jpeg", window)

    # Drawing the window
    window.blit(char_menu_bg, (0, 0))  # Blit the background

    # Font for character names
    font = pygame.font.Font('kalam.ttf', 40)

    # Colors
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    # List of character names and their corresponding images
    character_names = list(CHARACTERS)
    character_images = {
        "VirtualGuy": pygame.image.load(r"assets/MainCharacters/VirtualGuy/jump.png").convert_alpha(),
        "MaskDude": pygame.image.load(r"assets/MainCharacters/MaskDude/jump.png").convert_alpha(),
        "PinkMan": pygame.image.load(r"assets/MainCharacters/PinkMan/jump.png").convert_alpha(),
        "NinjaFrog": pygame.image.load(r"assets/MainCharacters/NinjaFrog/jump.png").convert_alpha()
    }
    selected_index = 0  # Initially select the first character
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Player has selected a character
                    return character_names[selected_index]
                elif event.key == pygame.K_UP:  # Move selection up
                    selected_index = (selected_index - 1) % len(character_names)
                elif event.key == pygame.K_DOWN:  # Move selection down
                    selected_index = (selected_index + 1) % len(character_names)

        # Drawing title
        title_font = pygame.font.Font('escapegtu.ttf', 50)
        nav_font = pygame.font.Font('escapegtu.ttf', 22)
        title_text = title_font.render("Choose Any Character:", True, WHITE)
        title_rect = title_text.get_rect(center=(window.get_width() // 2, 50))
        window.blit(title_text, title_rect)
        nav_text = nav_font.render("Use UP & DOWN to navigate, and press ENTER to select", False, WHITE)
        nav_rect = nav_text.get_rect(midtop=(window.get_width() // 2, window.get_height() - 50))
        window.blit(nav_text, nav_rect)


        # Drawing character names and images with some styling
        for i, name in enumerate(character_names):
            # Load character image and resize if needed
            image = pygame.transform.scale(character_images[name], (100, 100))
            image_rect = image.get_rect(center=(window.get_width() // 4, 150 + i * 160))

            # Draw character image
            window.blit(image, image_rect)

            # Draw character name with some horizontal spacing
            text = font.render(name, True, WHITE if i != selected_index else RED)
            text_rect = text.get_rect(
                left=image_rect.right + 20,  # Add spacing between image and text
                centery=image_rect.centery
            )
            window.blit(text, text_rect)

        # Add some decorative elements (optional)
        # Example: Drawing a background image or other visual effects

        pygame.display.flip()

    # If the user closes the window without selecting, return None
    return None

def select_terrain(window):

    # Load background image
    terrain_menu_bg = load_background("assets/Background/menubg.jpeg", window)
        # Drawing the window
    window.blit(terrain_menu_bg, (0, 0))  # Blit the background

    # Font for terrain names
    font = pygame.font.Font('kalam.ttf', 40)

    # Colors
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    # List of terrain options
    terrain_options = [
        "Hollow Rock", "Grass", "Wooden", "Hollow Wood",
        "Alien", "Mud", "Ice-Cream", "Steel", "Cheese", "Bricks", "Gold"
    ]

    selected_index = 0  # Initially select the first terrain
    running = True

    # Load terrain images
    terrain_images = {}
    for terrain in terrain_options:
        image_path = f"assets/Terrain/{terrain.lower()}.png"
        original_image = pygame.image.load(image_path).convert_alpha()
        scaled_image = pygame.transform.scale(original_image, (50, 50))  # Scale down the image
        terrain_images[terrain] = scaled_image

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Player has selected a terrain
                    return get_terrain_rect(terrain_options[selected_index])
                elif event.key == pygame.K_UP:  # Move selection up
                    selected_index = (selected_index - 1) % len(terrain_options)
                elif event.key == pygame.K_DOWN:  # Move selection down
                    selected_index = (selected_index + 1) % len(terrain_options)

        # Drawing title
        title_font = pygame.font.Font('escapegtu.ttf', 50)
        nav_font = pygame.font.Font('escapegtu.ttf', 22)
        title_text = title_font.render("Choose Terrain:", True, WHITE)
        title_rect = title_text.get_rect(center=(window.get_width() // 2, 50))
        window.blit(title_text, title_rect)
        nav_text = nav_font.render("Use UP & DOWN to navigate, and press ENTER to select", False, WHITE)
        nav_rect = nav_text.get_rect(midtop=(window.get_width() // 2, window.get_height() - 50))
        window.blit(nav_text, nav_rect)

        # Drawing terrain options with images
        for i, terrain in enumerate(terrain_options):
            text_color = RED if i == selected_index else WHITE
            text = font.render(terrain, True, text_color)
            text_rect = text.get_rect(center=(window.get_width() // 2, 150 + i * 50))
            window.blit(text, text_rect)

            # Draw terrain image
            image = terrain_images[terrain]
            image_rect = image.get_rect(left=100, centery=text_rect.centery)
            window.blit(image, image_rect)

        pygame.display.flip()

    # If the user closes the window without selecting, return None
    return None

def get_terrain_rect(terrain_option):
    # Define terrain rectangles for each terrain option
    terrain_rectangles = {
        "Hollow Rock": pygame.Rect(0, 0, 64, 64), 
        "Grass": pygame.Rect(96, 0, 64, 64),  
        "Wooden": pygame.Rect(192, 0, 64, 64), 
        "Hollow Wood": pygame.Rect(0, 64, 64, 64),
        "Alien": pygame.Rect(0, 128, 64, 64),
        "Mud": pygame.Rect(96, 64, 64, 64),
        "Ice-Cream": pygame.Rect(96, 128, 64, 64),
        "Steel": pygame.Rect(192, 64, 64, 64),
        "Cheese": pygame.Rect(192, 128, 64, 64),
        "Bricks": pygame.Rect(272, 64, 64, 64), 
        "Gold": pygame.Rect(272, 128, 64, 64), 
        # Add more terrain rectangles for other options
    }

    # Return the corresponding terrain rectangle for the selected terrain option
    return terrain_rectangles.get(terrain_option, pygame.Rect(0, 0, WIDTH, HEIGHT))  # Default to full screen if terrain not found

def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites

def get_block(size, terrain_rect):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    surface.blit(image, (0, 0), terrain_rect)
    return pygame.transform.scale2x(surface)

class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height, character_name):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0
        self.character_name = character_name
        self.SPRITES = load_sprite_sheets("MainCharacters", self.character_name, 32, 32, True)
        self.sprite = None
        # Initialize sprite here
        self.update_sprite()

    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        self.hit = True

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 2:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))

    def check_collision_with_fire(self, fire_objects):
        for fire in fire_objects:
            if pygame.sprite.collide_mask(self, fire):
                return True  # Collision detected with at least one fire
        return False  # No collision with any fire

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Block(Object):
    def __init__(self, x, y, size, terrain_rect):
        super().__init__(x, y, size, size)
        block = get_block(size, terrain_rect)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

class Fire(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")
        self.fire = load_sprite_sheets("Traps", "Fire", width, height)
        self.image = self.fire["on"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "on"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0

    def update(self):
        self.loop()  # Update fire animation

class Start(Object):
    ANIMATION_DELAY = 2

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "start")
        self.start = load_sprite_sheets("Items", "Start", width, height)
        self.image = self.start["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.start[self.animation_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0

    def update(self):
        self.loop()  # Update start animation


class Checkpoint(Object):
    ANIMATION_DELAY = 4

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "checkpoint")
        self.start = load_sprite_sheets("Items", "Checkpoints", width, height)
        self.image = self.start["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.start[self.animation_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0

    def update(self):
        self.loop()  # Update start animation

class Apple(Object):
    ANIMATION_DELAY = 2  # Add this line to define the animation delay for the apple

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "apple")
        self.apple = load_sprite_sheets("Items", "Fruits", width, height)
        self.image = self.apple["apple"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "apple"
        self.touched = False  # Attribute to track whether the apple has been touched

    def set_animation_name(self, animation_name):
        self.animation_name = animation_name

    def loop(self):
        sprites = self.apple[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0

    def update(self):
        self.loop()  # Update apple animation

# Load the elevator image
elevator_img = pygame.image.load("assets/Background/elevator.png")
elevator_img = pygame.transform.scale(elevator_img, (683, 514))

class Elevator(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.x = x
        self.y = y
        self.collidable = False  # This makes sure elevator is not checked for collisions
        self.name = "elevator"

    def draw(self, surface, offset_x):
        surface.blit(self.image, (self.x - offset_x, self.y))
        font = pygame.font.Font("escapegtu.ttf", 50)
        text = font.render("C-Block Lift", True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.x + self.image.get_width() // 2 - offset_x, self.y - 20))
        surface.blit(text, text_rect)

    def update(self):
        pass

class Scoreboard(Object):
    def __init__(self):
        self.label_font = pygame.font.Font("escapegtu.ttf", 28)
        self.score_font = pygame.font.Font("escapegtusolid.ttf", 28)
        self.score = 0

    def update_score(self, score):
        self.score = score

    def draw(self, window):
        label_text = self.label_font.render("Score: ", True, (0,0,0))
        score_text = self.score_font.render(str(self.score), True, (0,0,0))
        label_width = label_text.get_width()
        window.blit(label_text, (10, 10))
        window.blit(score_text, (10 + label_width, 10))

def handle_events(player, objects, score):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == APPLE_COLLISION_EVENT:
            apple = event.apple
            if apple in objects:
                objects.remove(apple)
                score += 1
    return score

def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image

def draw(window, background, bg_image, player, objects, offset_x, stop_message, show_stop_message):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        if isinstance(obj, Scoreboard):  # Check if obj is a Scoreboard instance
            obj.draw(window)
        else:
            obj.draw(window, offset_x)

    # Draw stop message if player is at checkpoint 2 but doesn't have enough score
    if show_stop_message:
        window.blit(stop_message, (WIDTH // 2 - stop_message.get_width() // 2, HEIGHT // 2 - stop_message.get_height() // 2))
        show_stop_message = False
    player.draw(window, offset_x)

    pygame.display.update()

def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if hasattr(obj, 'collidable') and not obj.collidable:
            continue
        if not isinstance(obj, Scoreboard) and pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects

def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if hasattr(obj, 'collidable') and not obj.collidable:
            continue
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()
    return collided_object

def handle_move(player, objects):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    collide_left = collide(player, [obj for obj in objects if not isinstance(obj, Scoreboard)], -PLAYER_VEL * 2)
    collide_right = collide(player, [obj for obj in objects if not isinstance(obj, Scoreboard)], PLAYER_VEL * 2)

    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]

    for obj in to_check:
        if isinstance(obj, Scoreboard):
            continue
        if obj and obj.name == "fire":
            player.make_hit()

def generate_blocks(block_size, num_blocks, terrain_rect):
    # Create a list to store the blocks
    blocks = []
     
    # Loop through the desired number of blocks
    for _ in range(num_blocks):
        # Generate random x and y positions for the block
        x = random.randint(3400, WIDTH * 15)
        y = random.randint(0, HEIGHT)
        temp_block = Block(x, y, block_size, terrain_rect)

        # Check for collisions with existing blocks
        collision = False
        for existing_block in blocks:
            # Check if the rectangles of temp_block and existing_block collide
            if temp_block.rect.colliderect(existing_block.rect):
                collision = True
                break

        # If no collision, add the block to the list
        if not collision:
            blocks.append(temp_block)

    return blocks


def generate_plane(x_offset, y_offset, width, height, terrain_rect):

    blocks = []
    block_size = 64
    x = x_offset
    y = y_offset
    
    for row in range(height // block_size):
        for col in range(width // block_size):
            block = Block(x + col * block_size, y + row * block_size, block_size, terrain_rect)
            blocks.append(block)
    
    return blocks

def restart(window, player, offset_x, offset_y, camera_speed_x, camera_speed_y, scroll_area_width, scroll_area_height):
    # Reset player's position
    player.rect.x = 100
    player.rect.y = 400
    player.x_vel = 0
    player.y_vel = 0
    # Reset camera offsets
    offset_x = 0
    offset_y = 0
    return offset_x, offset_y

def main(window, fire_objects):
    start_menu(window)
    clock = pygame.time.Clock()
    background, bg_image = get_background("gtu1.jpg")

    character_name = select_character(window, CHARACTERS)
    if character_name is None:
        return
    
    terrain_rect = select_terrain(window)  # Get the selected terrain rect
    if terrain_rect is None:
        return
    
    offset_x = 0
    offset_y = 0
    scroll_area_width = 400
    scroll_area_height = 400
    camera_speed_x = 6
    camera_speed_y = 6
    run = True
    is_jumping = False
    score = 0
    game_over = False 
    restart_condition_met = False
    stopfont = pygame.font.Font("escapegtu.ttf", 36)
    stop_message = stopfont.render("Score 100 needed to go further!", True, (0, 0, 0))
    show_stop_message = False

    objects = []
    
    pygame.mixer.music.load("assets/music/loop1.mp3")
     # Load and play the background music
    pygame.mixer.music.play(-1)  # -1 makes it play in a loop

    player = Player(100, 100, 50, 50, character_name)

    num_blocks = 200  # Adjust this number to change the number of blocks
    blocks = generate_blocks(block_size, num_blocks, terrain_rect)     
    scoreboard = Scoreboard()
    # Create the elevator object at the specified position
    elevator = Elevator(14000, HEIGHT - 600, elevator_img)

    start1 = Start(-20, HEIGHT - block_size * 2.6 - 64, 64, 64)
    checkpoint1 = Checkpoint(14120, HEIGHT - 590 - 64, 64, 64)
    checkpoint2 = Checkpoint(14504, HEIGHT - 160 - 64, 64, 64)
    apple1 = Apple(300, HEIGHT - block_size * 5 - 64, 32, 32)
    apple2 = Apple(450, HEIGHT - block_size * 5 - 64, 32, 32)
    apple3 = Apple(600, HEIGHT - block_size * 5 - 64, 32, 32)
    apple4 = Apple(750, HEIGHT - block_size * 5 - 64, 32, 32)
    apple5 = Apple(900, HEIGHT - block_size * 5 - 64, 32, 32)
    apple6 = Apple(1050, HEIGHT - block_size * 5 - 64, 32, 32)
    apple7 = Apple(1200, HEIGHT - block_size * 5 - 64, 32, 32)
    apple8 = Apple(1320, HEIGHT - block_size * 7 - 64, 32, 32)
    apple9 = Apple(1450, HEIGHT - block_size * 5 - 64, 32, 32)
    apple10 = Apple(1750, HEIGHT - block_size * 5 - 64, 32, 32)
    apple11= Apple(1925, HEIGHT - block_size * 3 - 64, 32, 32)
    apple12= Apple(2030, HEIGHT - block_size * 2.2 - 64, 32, 32)
    apple13= Apple(2350, HEIGHT - block_size * 2 - 64, 32, 32)
    apple14= Apple(2600, HEIGHT - block_size * 2 - 64, 32, 32)
    apple15= Apple(2600, HEIGHT - block_size * 4 - 64, 32, 32)
    apple16= Apple(2800, HEIGHT - block_size * 2 - 64, 32, 32)
    apple17= Apple(3000, HEIGHT - block_size * 2 - 64, 32, 32)
    apple18= Apple(2800, HEIGHT - block_size * 4 - 64, 32, 32)
    apple19= Apple(2700, HEIGHT - block_size * 6 - 64, 32, 32)
    apple20= Apple(3750, HEIGHT - block_size  - 64, 32, 32)
    apple21= Apple(4050, HEIGHT - block_size  - 64, 32, 32)
    apple22= Apple(4350, HEIGHT - block_size  - 64, 32, 32)
    apple23= Apple(3750, HEIGHT - block_size * 4 - 64, 32, 32)
    apple24= Apple(4050, HEIGHT - block_size * 3 - 64, 32, 32)
    apple25= Apple(4350, HEIGHT - block_size * 4 - 64, 32, 32)
    apple26= Apple(3650, HEIGHT - block_size * 4 - 64, 32, 32)
    apple27= Apple(4450, HEIGHT - block_size * 4 - 64, 32, 32)
    apple28= Apple(3600, HEIGHT - block_size * 2 - 64, 32, 32)
    apple29= Apple(3850, HEIGHT - block_size * 6 - 64, 32, 32)
    apple30= Apple(4250, HEIGHT - block_size * 6 - 64, 32, 32)
    apple31 = Apple(675, HEIGHT - block_size * 6.5 - 64, 32, 32)
    apple32 = Apple(5100, HEIGHT - block_size * 5 - 64, 32, 32)
    apple33 = Apple(4900, HEIGHT - block_size * 4 - 64, 32, 32)
    apple34 = Apple(5100, HEIGHT - block_size * 3 - 64, 32, 32)
    apple35 = Apple(5200, HEIGHT - block_size * 3 - 64, 32, 32)
    apple36 = Apple(5300, HEIGHT - block_size * 5 - 64, 32, 32)
    apple37 = Apple(5300, HEIGHT - block_size * 2 - 64, 32, 32)
    apple38 = Apple(5300, HEIGHT - block_size * 3 - 64, 32, 32)
    apple39 = Apple(5400, HEIGHT - block_size * 5 - 64, 32, 32)
    apple40 = Apple(5000, HEIGHT - block_size * 5 - 64, 32, 32)
    apple41 = Apple(5500, HEIGHT - block_size * 2 - 64, 32, 32)
    apple42 = Apple(5680, HEIGHT - block_size * 2 - 64, 32, 32)
    apple43 = Apple(5685, HEIGHT - block_size * 3 - 64, 32, 32)
    apple44 = Apple(5850, HEIGHT - block_size * 5 - 64, 32, 32)
    apple45 = Apple(5785, HEIGHT - block_size * 4 - 64, 32, 32)
    apple46 = Apple(5785, HEIGHT - block_size * 3 - 64, 32, 32) 
    apple47 = Apple(5885, HEIGHT - block_size * 3 - 64, 32, 32)
    apple48 = Apple(5950, HEIGHT - block_size * 5 - 64, 32, 32)
    apple49 = Apple(5200, HEIGHT - block_size * 4 - 64, 32, 32)
    apple50 = Apple(5570, HEIGHT - block_size * 5 - 64, 32, 32)
    apple51 = Apple(5685, HEIGHT - block_size * 5 - 64, 32, 32)
    apple52 = Apple(5585, HEIGHT - block_size * 7 - 64, 32, 32)
    apple53 = Apple(5400, HEIGHT - block_size * 7 - 64, 32, 32)
    apple54 = Apple(6535, HEIGHT - block_size * 3 - 64, 32, 32)
    apple55 = Apple(6735, HEIGHT - block_size * 4 - 64, 32, 32)
    apple56 = Apple(6930, HEIGHT - block_size * 3 - 64, 32, 32)
    apple57 = Apple(7130, HEIGHT - block_size * 4 - 64, 32, 32)
    apple58 = Apple(7325, HEIGHT - block_size * 3 - 64, 32, 32)
    apple59 = Apple(7700, HEIGHT - block_size * 3 - 64, 32, 32)
    apple60 = Apple(7800, HEIGHT - block_size * 3 - 64, 32, 32)
    apple61 = Apple(7900, HEIGHT - block_size * 3 - 64, 32, 32)
    apple62 = Apple(8000, HEIGHT - block_size * 3 - 64, 32, 32)
    apple63 = Apple(8100, HEIGHT - block_size * 3 - 64, 32, 32)
    apple64 = Apple(7800, HEIGHT - block_size * 5 - 64, 32, 32)
    apple65 = Apple(8000, HEIGHT - block_size * 5 - 64, 32, 32)
    apple66 = Apple(7700, HEIGHT - block_size * 7 - 64, 32, 32)
    apple67 = Apple(7800, HEIGHT - block_size * 7 - 64, 32, 32)
    apple68 = Apple(8000, HEIGHT - block_size * 7 - 64, 32, 32)
    apple69 = Apple(8100, HEIGHT - block_size * 7 - 64, 32, 32)
    apple70 = Apple(8450, HEIGHT - block_size * 2 - 64, 32, 32)
    apple71 = Apple(8550, HEIGHT - block_size * 4.2 - 64, 32, 32)
    apple72 = Apple(8850, HEIGHT - block_size * 5 - 64, 32, 32)
    apple73 = Apple(9200, HEIGHT - block_size - 64, 32, 32)
    apple74 = Apple(9340, HEIGHT - block_size * 3 - 64, 32, 32)
    apple75 = Apple(9436, HEIGHT - block_size * 4 - 64, 32, 32)
    apple76 = Apple(9628, HEIGHT - block_size * 4 - 64, 32, 32)
    apple77 = Apple(9724, HEIGHT - block_size * 3 - 64, 32, 32)
    apple78 = Apple(9916, HEIGHT - block_size * 4 - 64, 32, 32)
    apple79 = Apple(10012, HEIGHT - block_size * 5 - 64, 32, 32)
    apple80 = Apple(10204, HEIGHT - block_size * 5 - 64, 32, 32)
    apple81 = Apple(10300, HEIGHT - block_size * 4 - 64, 32, 32)
    apple82 = Apple(10492, HEIGHT - block_size * 3 - 64, 32, 32)
    apple83 = Apple(10588, HEIGHT - block_size * 4 - 64, 32, 32)
    apple84 = Apple(10780, HEIGHT - block_size * 4 - 64, 32, 32)
    apple85 = Apple(10876, HEIGHT - block_size * 3 - 64, 32, 32)
    apple86 = Apple(11068, HEIGHT - block_size * 4 - 64, 32, 32)
    apple87 = Apple(11164, HEIGHT - block_size * 5 - 64, 32, 32)
    apple88 = Apple(11356, HEIGHT - block_size * 5 - 64, 32, 32)
    apple89 = Apple(11452, HEIGHT - block_size * 4 - 64, 32, 32)
    apple90 = Apple(11644, HEIGHT - block_size * 3 - 64, 32, 32)
    apple91 = Apple(11740, HEIGHT - block_size * 4 - 64, 32, 32)
    apple92 = Apple(11932, HEIGHT - block_size * 4 - 64, 32, 32)
    apple93 = Apple(12028, HEIGHT - block_size * 3 - 64, 32, 32)
    apple94 = Apple(9340, HEIGHT - block_size * 5 - 64, 32, 32)
    apple95 = Apple(9724, HEIGHT - block_size * 5 - 64, 32, 32)
    apple96 = Apple(9916, HEIGHT - block_size * 6 - 64, 32, 32)
    apple97 = Apple(10300, HEIGHT - block_size * 6 - 64, 32, 32)
    apple98 = Apple(10492, HEIGHT - block_size * 5 - 64, 32, 32)
    apple99 = Apple(10876, HEIGHT - block_size * 5 - 64, 32, 32)
    apple100 = Apple(11068, HEIGHT - block_size * 6 - 64, 32, 32)
    apple101 = Apple(11452, HEIGHT - block_size * 6 - 64, 32, 32)
    apple102 = Apple(11644, HEIGHT - block_size * 5 - 64, 32, 32)
    apple103 = Apple(12028, HEIGHT - block_size * 5 - 64, 32, 32)
    apple104 = Apple(12422, HEIGHT - block_size * 3 - 64, 32, 32)
    apple105 = Apple(12518, HEIGHT - block_size * 4 - 64, 32, 32)
    apple106 = Apple(12614, HEIGHT - block_size * 3 - 64, 32, 32)
    apple107 = Apple(12806, HEIGHT - block_size * 3 - 64, 32, 32)
    apple108 = Apple(12902, HEIGHT - block_size * 4 - 64, 32, 32)
    apple109 = Apple(12998, HEIGHT - block_size * 3 - 64, 32, 32)
    apple110 = Apple(13190, HEIGHT - block_size * 3 - 64, 32, 32)
    apple111 = Apple(13286, HEIGHT - block_size * 4 - 64, 32, 32)
    apple112 = Apple(13382, HEIGHT - block_size * 3 - 64, 32, 32)
    apple113 = Apple(13574, HEIGHT - block_size * 3 - 64, 32, 32)
    apple114 = Apple(13670, HEIGHT - block_size * 4 - 64, 32, 32)
    apple115 = Apple(13766, HEIGHT - block_size * 3 - 64, 32, 32)

    apple_objects = [apple1, apple2, apple3, apple4, apple5, apple6, apple7, apple8, apple9, apple10, apple11 ,apple12, apple13, apple14, apple15, apple16, apple17, apple18, apple19, apple20, apple21, apple22, apple23, apple24, apple25, 
                     apple26, apple27, apple28, apple29, apple30, apple31, apple32, apple33, apple34, apple35, apple36, apple37, apple38, apple39, apple40, apple41, apple42, apple43, apple44, apple45, apple46, apple47, apple48, apple49, apple50,
                     apple51, apple52, apple53, apple54, apple55, apple56, apple57, apple58, apple59, apple60, apple61, apple62, apple63, apple64, apple65, apple66, apple67, apple68, apple69, apple70, apple71, apple72, apple73, apple74, apple75, 
                     apple76, apple77, apple78, apple79, apple80, apple81, apple82, apple83, apple84, apple85, apple86, apple87, apple88, apple89, apple90, apple91, apple92, apple93, apple94, apple95, apple96, apple97, apple98, apple99, apple100, 
                     apple101, apple102, apple103, apple104, apple105, apple106, apple107, apple108, apple109, apple110, apple111, apple112, apple113, apple114, apple115
                     ]

    font = pygame.font.Font('freesansbold.ttf', 25)
    fire1.on()
    fire2.on()
    fire3.on()
    fire4.on()
    fire5.on()
    fire6.on()
    fire7.on()
    fire8.on()
    fire9.on()
    fire10.on()
    fire11.on()
    fire12.on()
    fire13.on()
    fire14.on()
    fire15.on()
    fire16.on()
    fire17.on()
    fire18.on()
    fire19.on()
    fire20.on()
    fire21.on()
    fire22.on()
    fire23.on()
    fire24.on()
    fire25.on()
    fire26.on()
    fire27.on()
    fire28.on()
    fire29.on()
    fire30.on()
    fire31.on()
    fire32.on()
    fire33.on()
    fire34.on()
    fire35.on()
    fire36.on()
    fire37.on()
    fire38.on()
    fire39.on()
    fire40.on()
    fire41.on()
    fire42.on()
    fire43.on()
    fire44.on()
    fire45.on()
    fire46.on()
    fire47.on()
    fire48.on()
    fire49.on()
    fire50.on()
    fire51.on()
    fire52.on()
    fire53.on()
    fire54.on()
    fire55.on()
    fire56.on()
    fire57.on()
    fire58.on()
    fire59.on()
    fire60.on()
    fire61.on()
    fire62.on()
    fire63.on()
    fire64.on()
    fire65.on()
    fire66.on()
    fire67.on()
    fire68.on()
    fire69.on()
    fire70.on()
    fire71.on()

    start1.on()
    checkpoint1.on()
    
    floor = [Block(i * block_size, HEIGHT - block_size, block_size, terrain_rect)
         for i in range((-WIDTH * 2) // block_size, (WIDTH * 30) // block_size)]

    objects = [*floor, elevator, scoreboard, Block(0, HEIGHT - block_size * 2, block_size, terrain_rect), Block(block_size, HEIGHT - block_size * 3, block_size, terrain_rect),
           Block(block_size * 3, HEIGHT - block_size * 5, block_size, terrain_rect), Block(block_size * 3, HEIGHT - block_size * 5, block_size, terrain_rect), Block(block_size * 3, HEIGHT - block_size * 4, block_size, terrain_rect),
           Block(block_size * 3, HEIGHT - block_size * 3, block_size, terrain_rect), Block(block_size * 3, HEIGHT - block_size * 2, block_size, terrain_rect),
           Block(block_size * 4, HEIGHT - block_size * 5, block_size, terrain_rect), Block(block_size * 5, HEIGHT - block_size * 3, block_size, terrain_rect),
           Block(block_size * 5, HEIGHT - block_size * 5, block_size, terrain_rect), Block(block_size * 6, HEIGHT - block_size * 5, block_size, terrain_rect),
           Block(block_size * 6, HEIGHT - block_size * 2, block_size, terrain_rect), Block(block_size * 6, HEIGHT - block_size * 3, block_size, terrain_rect),

           Block(block_size * 10, HEIGHT - block_size * 2, block_size, terrain_rect), Block(block_size * 10, HEIGHT - block_size * 3, block_size, terrain_rect), Block(block_size * 10, HEIGHT - block_size * 4, block_size, terrain_rect),
           Block(block_size * 10, HEIGHT - block_size * 5, block_size, terrain_rect),
           Block(block_size * 9, HEIGHT - block_size * 5, block_size, terrain_rect), Block(block_size * 8, HEIGHT - block_size * 5, block_size, terrain_rect),
           Block(block_size * 11, HEIGHT - block_size * 5, block_size, terrain_rect), Block(block_size * 12, HEIGHT - block_size * 5, block_size, terrain_rect),

           Block(block_size * 15, HEIGHT - block_size * 2, block_size, terrain_rect), Block(block_size * 15, HEIGHT - block_size * 3, block_size, terrain_rect), Block(block_size * 15, HEIGHT - block_size * 4, block_size, terrain_rect),
           Block(block_size * 15, HEIGHT - block_size * 5, block_size, terrain_rect), Block(block_size * 16, HEIGHT - block_size * 2, block_size, terrain_rect), Block(block_size * 17, HEIGHT - block_size * 2, block_size, terrain_rect),
           Block(block_size * 18, HEIGHT - block_size * 2, block_size, terrain_rect), Block(block_size * 18, HEIGHT - block_size * 3, block_size, terrain_rect),
           Block(block_size * 18, HEIGHT - block_size * 4, block_size, terrain_rect), Block(block_size * 18, HEIGHT - block_size * 5, block_size, terrain_rect),

           Block(block_size * 20, HEIGHT - block_size * 3, block_size, terrain_rect), Block(block_size * 21, HEIGHT - block_size * 2, block_size, terrain_rect),

           Block(block_size * 24, HEIGHT - block_size * 2, block_size, terrain_rect), Block(block_size * 25, HEIGHT - block_size * 2, block_size, terrain_rect), Block(block_size * 26, HEIGHT - block_size * 2, block_size, terrain_rect), Block(block_size * 27, HEIGHT - block_size * 2, block_size, terrain_rect),
           Block(block_size * 29, HEIGHT - block_size * 2, block_size, terrain_rect),  Block(block_size * 30, HEIGHT - block_size * 2, block_size, terrain_rect), Block(block_size * 31, HEIGHT - block_size * 2, block_size, terrain_rect),
           Block(block_size * 32, HEIGHT - block_size * 2, block_size, terrain_rect), Block(block_size * 25, HEIGHT - block_size * 4, block_size, terrain_rect), Block(block_size * 26, HEIGHT - block_size * 4, block_size, terrain_rect),
           Block(block_size * 30, HEIGHT - block_size * 4, block_size, terrain_rect), Block(block_size * 31, HEIGHT - block_size * 4, block_size, terrain_rect), Block(block_size * 29, HEIGHT - block_size * 8, block_size, terrain_rect),
           Block(block_size * 26, HEIGHT - block_size * 6, block_size, terrain_rect), Block(block_size * 27, HEIGHT - block_size * 6, block_size, terrain_rect), Block(block_size * 27, HEIGHT - block_size * 8, block_size, terrain_rect),
           Block(block_size * 28, HEIGHT - block_size * 6, block_size, terrain_rect), Block(block_size * 29, HEIGHT - block_size * 6, block_size, terrain_rect),  Block(block_size * 30, HEIGHT - block_size * 6, block_size, terrain_rect),

           Block(block_size * 35, HEIGHT - block_size * 2, block_size, terrain_rect), Block(block_size * 36, HEIGHT - block_size * 2, block_size, terrain_rect), Block(block_size * 37, HEIGHT - block_size * 2, block_size, terrain_rect), 
           Block(block_size * 37, HEIGHT - block_size * 4, block_size, terrain_rect), Block(block_size * 38, HEIGHT - block_size * 4, block_size, terrain_rect), Block(block_size * 39, HEIGHT - block_size * 4, block_size, terrain_rect),
           Block(block_size * 39, HEIGHT - block_size * 6, block_size, terrain_rect), Block(block_size * 40, HEIGHT - block_size * 6, block_size, terrain_rect), Block(block_size * 41, HEIGHT - block_size * 6, block_size, terrain_rect),
           
           Block(block_size * 43, HEIGHT - block_size * 6, block_size, terrain_rect), Block(block_size * 44, HEIGHT - block_size * 6, block_size, terrain_rect), Block(block_size * 45, HEIGHT - block_size * 6, block_size, terrain_rect), 
           Block(block_size * 45, HEIGHT - block_size * 4, block_size, terrain_rect), Block(block_size * 46, HEIGHT - block_size * 4, block_size, terrain_rect), Block(block_size * 47, HEIGHT - block_size * 4, block_size, terrain_rect),
           Block(block_size * 47, HEIGHT - block_size * 2, block_size, terrain_rect), Block(block_size * 48, HEIGHT - block_size * 2, block_size, terrain_rect), Block(block_size * 49, HEIGHT - block_size * 2, block_size, terrain_rect),
           Block(block_size * 41, HEIGHT - block_size * 3, block_size, terrain_rect), Block(block_size * 42, HEIGHT - block_size * 3, block_size, terrain_rect), Block(block_size * 43, HEIGHT - block_size * 3, block_size, terrain_rect),
          
           Block(block_size * 56, HEIGHT - block_size * 4, block_size, terrain_rect), Block(block_size * 58, HEIGHT - block_size * 4, block_size, terrain_rect), 
           Block(block_size * 56, HEIGHT - block_size * 5, block_size, terrain_rect), Block(block_size * 58, HEIGHT - block_size * 5, block_size, terrain_rect), Block(block_size * 59, HEIGHT - block_size * 5, block_size, terrain_rect),
           Block(block_size * 53, HEIGHT - block_size * 5, block_size, terrain_rect), Block(block_size * 52, HEIGHT - block_size * 5, block_size, terrain_rect), Block(block_size * 52, HEIGHT - block_size * 4, block_size, terrain_rect),
           Block(block_size * 52, HEIGHT - block_size * 3, block_size, terrain_rect), Block(block_size * 53, HEIGHT - block_size * 3, block_size, terrain_rect), Block(block_size * 54, HEIGHT - block_size *3, block_size, terrain_rect), 
           Block(block_size * 61, HEIGHT - block_size * 5, block_size, terrain_rect), Block(block_size * 62, HEIGHT - block_size * 5, block_size, terrain_rect), Block(block_size * 62, HEIGHT - block_size * 4, block_size, terrain_rect),
           Block(block_size * 62, HEIGHT - block_size * 3, block_size, terrain_rect), Block(block_size * 61, HEIGHT - block_size * 3, block_size, terrain_rect), Block(block_size * 60, HEIGHT - block_size * 3, block_size, terrain_rect),
           Block(block_size * 56, HEIGHT - block_size * 7, block_size, terrain_rect), Block(block_size * 57, HEIGHT - block_size * 7, block_size, terrain_rect), Block(block_size * 58, HEIGHT - block_size * 7, block_size, terrain_rect), 
           Block(block_size * 51, HEIGHT - block_size * 4, block_size, terrain_rect), Block(block_size * 63, HEIGHT - block_size * 4, block_size, terrain_rect), Block(block_size * 55, HEIGHT - block_size * 5, block_size, terrain_rect),

           Block(block_size * 68, HEIGHT - block_size * 2, block_size, terrain_rect), Block(block_size * 68, HEIGHT - block_size * 3, block_size, terrain_rect), Block(block_size * 68, HEIGHT - block_size *8, block_size, terrain_rect),
           Block(block_size * 68, HEIGHT - block_size * 5, block_size, terrain_rect), Block(block_size * 68, HEIGHT - block_size * 6, block_size, terrain_rect), Block(block_size * 68, HEIGHT - block_size *7, block_size, terrain_rect),
           Block(block_size * 70, HEIGHT - block_size * 2, block_size, terrain_rect), Block(block_size * 70, HEIGHT - block_size * 3, block_size, terrain_rect), Block(block_size * 70, HEIGHT - block_size * 4, block_size, terrain_rect),
           Block(block_size * 70, HEIGHT - block_size * 6, block_size, terrain_rect), Block(block_size * 70, HEIGHT - block_size * 7, block_size, terrain_rect), Block(block_size * 70, HEIGHT - block_size *8, block_size, terrain_rect), 
           Block(block_size * 72, HEIGHT - block_size * 2, block_size, terrain_rect), Block(block_size * 72, HEIGHT - block_size * 3, block_size, terrain_rect), Block(block_size * 72, HEIGHT - block_size * 5, block_size, terrain_rect),
           Block(block_size * 72, HEIGHT - block_size * 6, block_size, terrain_rect), Block(block_size * 72, HEIGHT - block_size * 7, block_size, terrain_rect), Block(block_size * 72, HEIGHT - block_size * 8, block_size, terrain_rect),
           Block(block_size * 74, HEIGHT - block_size * 2, block_size, terrain_rect), Block(block_size * 74, HEIGHT - block_size * 3, block_size, terrain_rect), Block(block_size * 74, HEIGHT - block_size * 4, block_size, terrain_rect), 
           Block(block_size * 74, HEIGHT - block_size * 6, block_size, terrain_rect), Block(block_size * 74, HEIGHT - block_size * 7, block_size, terrain_rect), Block(block_size * 74, HEIGHT - block_size * 8, block_size, terrain_rect),
           Block(block_size * 76, HEIGHT - block_size * 2, block_size, terrain_rect), Block(block_size * 76, HEIGHT - block_size * 3, block_size, terrain_rect), Block(block_size * 76, HEIGHT - block_size * 5, block_size, terrain_rect),
           Block(block_size * 76, HEIGHT - block_size * 6, block_size, terrain_rect), Block(block_size * 76, HEIGHT - block_size * 7, block_size, terrain_rect), Block(block_size * 76, HEIGHT - block_size * 8, block_size, terrain_rect),
           
           Block(block_size * 79, HEIGHT - block_size * 3, block_size, terrain_rect), Block(block_size * 79, HEIGHT - block_size * 4, block_size, terrain_rect), Block(block_size * 79, HEIGHT - block_size * 5, block_size, terrain_rect),
           Block(block_size * 79, HEIGHT - block_size * 6, block_size, terrain_rect), Block(block_size * 79, HEIGHT - block_size * 7, block_size, terrain_rect), Block(block_size * 79, HEIGHT - block_size * 8, block_size, terrain_rect),
           Block(block_size * 79, HEIGHT - block_size * 9, block_size, terrain_rect), Block(block_size * 80, HEIGHT - block_size * 9, block_size, terrain_rect), Block(block_size * 81, HEIGHT - block_size * 9, block_size, terrain_rect),
           Block(block_size * 82, HEIGHT - block_size * 9, block_size, terrain_rect), Block(block_size * 83, HEIGHT - block_size * 9, block_size, terrain_rect), Block(block_size * 84, HEIGHT - block_size * 9, block_size, terrain_rect), 
           Block(block_size * 85, HEIGHT - block_size * 9, block_size, terrain_rect), Block(block_size * 85, HEIGHT - block_size * 8, block_size, terrain_rect), Block(block_size * 85, HEIGHT - block_size * 7, block_size, terrain_rect),
           Block(block_size * 85, HEIGHT - block_size * 6, block_size, terrain_rect), Block(block_size * 85, HEIGHT - block_size * 5, block_size, terrain_rect), Block(block_size * 85, HEIGHT - block_size * 4, block_size, terrain_rect),
           Block(block_size * 85, HEIGHT - block_size * 3, block_size, terrain_rect), Block(block_size * 80, HEIGHT - block_size * 3, block_size, terrain_rect), Block(block_size * 81, HEIGHT - block_size * 3, block_size, terrain_rect), 
           Block(block_size * 82, HEIGHT - block_size * 3, block_size, terrain_rect), Block(block_size * 83, HEIGHT - block_size * 3, block_size, terrain_rect), 
           Block(block_size * 81, HEIGHT - block_size * 7, block_size, terrain_rect), Block(block_size * 82, HEIGHT - block_size * 7, block_size, terrain_rect), Block(block_size * 83, HEIGHT - block_size * 7, block_size, terrain_rect),
           Block(block_size * 81, HEIGHT - block_size * 5, block_size, terrain_rect), Block(block_size * 82, HEIGHT - block_size * 5, block_size, terrain_rect), Block(block_size * 83, HEIGHT - block_size * 5, block_size, terrain_rect),
           
           Block(block_size * 88, HEIGHT - block_size * 2, block_size, terrain_rect), Block(block_size * 89, HEIGHT - block_size * 4.2, block_size, terrain_rect), 
           Block(block_size * 90, HEIGHT - block_size * 3, block_size, terrain_rect), Block(block_size * 92, HEIGHT - block_size * 5, block_size, terrain_rect), Block(block_size * 93, HEIGHT - block_size * 3, block_size, terrain_rect),
        
           Block(block_size * 97, HEIGHT - block_size * 3, block_size, terrain_rect), Block(block_size * 97, HEIGHT - block_size * 5, block_size, terrain_rect), Block(block_size * 98, HEIGHT - block_size * 4, block_size, terrain_rect),
           Block(block_size * 99, HEIGHT - block_size * 5, block_size, terrain_rect), Block(block_size * 100, HEIGHT - block_size * 4, block_size, terrain_rect), Block(block_size * 101, HEIGHT - block_size * 3, block_size, terrain_rect),
           Block(block_size * 101, HEIGHT - block_size * 5, block_size, terrain_rect), Block(block_size * 103, HEIGHT - block_size * 6, block_size, terrain_rect), Block(block_size * 103, HEIGHT - block_size * 4, block_size, terrain_rect),
           Block(block_size * 104, HEIGHT - block_size * 5, block_size, terrain_rect), Block(block_size * 105, HEIGHT - block_size * 4, block_size, terrain_rect), Block(block_size * 106, HEIGHT - block_size * 5, block_size, terrain_rect), 
           Block(block_size * 107, HEIGHT - block_size * 6, block_size, terrain_rect), Block(block_size * 107, HEIGHT - block_size * 4, block_size, terrain_rect), 
           
           Block(block_size * 109, HEIGHT - block_size * 3, block_size, terrain_rect), Block(block_size * 109, HEIGHT - block_size * 5, block_size, terrain_rect), Block(block_size * 110, HEIGHT - block_size * 4, block_size, terrain_rect),
           Block(block_size * 111, HEIGHT - block_size * 5, block_size, terrain_rect), Block(block_size * 112, HEIGHT - block_size * 4, block_size, terrain_rect), Block(block_size * 113, HEIGHT - block_size * 3, block_size, terrain_rect),
           Block(block_size * 113, HEIGHT - block_size * 5, block_size, terrain_rect), Block(block_size * 115, HEIGHT - block_size * 6, block_size, terrain_rect), Block(block_size * 115, HEIGHT - block_size * 4, block_size, terrain_rect),
           Block(block_size * 116, HEIGHT - block_size * 5, block_size, terrain_rect), Block(block_size * 117, HEIGHT - block_size * 4, block_size, terrain_rect), Block(block_size * 118, HEIGHT - block_size * 5, block_size, terrain_rect), 
           Block(block_size * 119, HEIGHT - block_size * 6, block_size, terrain_rect), Block(block_size * 119, HEIGHT - block_size * 4, block_size, terrain_rect), 
           
           Block(block_size * 121, HEIGHT - block_size * 3, block_size, terrain_rect), Block(block_size * 121, HEIGHT - block_size * 5, block_size, terrain_rect), Block(block_size * 122, HEIGHT - block_size * 4, block_size, terrain_rect),
           Block(block_size * 123, HEIGHT - block_size * 5, block_size, terrain_rect), Block(block_size * 124, HEIGHT - block_size * 4, block_size, terrain_rect), Block(block_size * 125, HEIGHT - block_size * 3, block_size, terrain_rect),
           Block(block_size * 125, HEIGHT - block_size * 5, block_size, terrain_rect),

           Block(block_size * 128, HEIGHT - block_size * 2, block_size, terrain_rect), Block(block_size * 132, HEIGHT - block_size * 2, block_size, terrain_rect),
           Block(block_size * 136, HEIGHT - block_size * 2, block_size, terrain_rect), Block(block_size * 140, HEIGHT - block_size * 2, block_size, terrain_rect),
           Block(block_size * 144, HEIGHT - block_size * 2, block_size, terrain_rect), 

           fire1, fire2, fire3, fire4, fire5, fire6, fire7, fire8, fire9, fire10, fire11, fire12, fire13, fire14, fire15, fire16, fire17, fire18, fire19, fire20, fire21, fire22, fire23, fire24, fire25, fire26, fire27, fire28, fire29, fire30, 
           fire31, fire32, fire33, fire34, fire35, fire36, fire37, fire38, fire39, fire40, fire41, fire42, fire43, fire44, fire45, fire46, fire47, fire48, fire49, fire50, fire51, fire52, fire53, fire54, fire55, fire56, fire57, fire58, fire59,fire60, 
           fire61, fire62, fire63, fire64, fire65, fire66, fire67, fire68, fire69, fire70, fire71, start1, checkpoint1, checkpoint2, *apple_objects ]

    while run:
        clock.tick(FPS)
        # Update and draw player
        player.loop(FPS)
        player.draw(window, offset_x) 

        # Update the scoreboard with the current score
        scoreboard.update_score(score)
        # Draw the scoreboard
        scoreboard.draw(window)

        # Update and draw fires
        for fire in fire_objects:
          fire.update()
          fire.draw(window, offset_x)
        # Update and draw start arrow
       # for start1 in objects:
        #    start1.update()
         #   start1.draw(window, offset_x)

        for apple in apple_objects:
            apple.update()
            apple.draw(window, offset_x)
        #Apples getting removed and score increments
        for apple in apple_objects:
            if pygame.sprite.collide_rect(player, apple):
                # Teleport the apple to the chosen location
                apple.rect.x, apple.rect.y = TELEPORT_LOCATION
                # Increment the score
                score += 1
                score_sound.play()  # Play score sound

        # Check for collision between player and fire objects
        for fire in fire_objects:
            if pygame.sprite.collide_mask(player, fire):
                # If collision detected, set game over state to True
                game_over = True
                gameover_sound.play()  # Play game over sound
                break

       # Draw the elevator (without any collision logic)
       # elevator.draw(window, player.rect.x - WIDTH // 2 + player.rect.width // 2)
        
        if game_over:
            # Display game over screen
            game_over_screen(window)
            pygame.mixer.music.stop()  # Stop the background music
            gameover_sound.play()  # Play game over sound
            pygame.display.update()

            # Wait for player to press space to restart
            wait_for_restart()
            offset_x, offset_y = restart(window, player, offset_x, offset_y, camera_speed_x, camera_speed_y, scroll_area_width, scroll_area_height)

            # Reset game state
            pygame.mixer.music.play(-1)  # Restart the background music
            game_over = False


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()
                    if player.jump_count == 2:  # Assuming double jump is the second jump
                        doublejump_sound.play()

                # Check for game restart
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    
                    offset_x, offset_y = restart(window, player, offset_x, offset_y, camera_speed_x, camera_speed_y, scroll_area_width, scroll_area_height)

        pygame.display.update()
        clock.tick(60)

        player.loop(FPS)
        fire1.loop()
        fire2.loop()
        fire3.loop()
        fire4.loop()
        fire5.loop()
        fire6.loop()
        fire7.loop()
        fire8.loop()
        fire9.loop()
        fire10.loop()
        fire11.loop()
        fire12.loop()
        fire13.loop()
        fire14.loop()
        fire15.loop()
        fire16.loop()
        fire17.loop()
        fire18.loop()
        fire19.loop()
        fire20.loop()
        fire21.loop()
        fire22.loop()
        fire23.loop()
        fire24.loop()
        fire25.loop()
        fire26.loop()
        fire27.loop()
        fire28.loop()
        fire29.loop()
        fire30.loop()
        fire31.loop()
        fire32.loop()
        fire33.loop()
        fire34.loop()
        fire35.loop()
        fire36.loop()
        fire37.loop()
        fire38.loop()
        fire39.loop()
        fire40.loop()
        fire41.loop()
        fire42.loop()
        fire43.loop()
        fire44.loop()
        fire45.loop()
        fire46.loop()
        fire47.loop()
        fire48.loop()
        fire49.loop()
        fire50.loop()
        fire51.loop()
        fire52.loop()
        fire53.loop()
        fire54.loop()
        fire55.loop()
        fire56.loop()
        fire57.loop()
        fire58.loop()
        fire59.loop()
        fire60.loop()
        fire61.loop()
        fire62.loop()
        fire63.loop()
        fire64.loop()
        fire65.loop()
        fire66.loop()
        fire67.loop()
        fire68.loop()
        fire69.loop()
        fire70.loop()
        fire71.loop()

        start1.loop()
        checkpoint1.loop()
        checkpoint2.loop()

        handle_move(player, objects)
        draw(window, background, bg_image, player, objects, offset_x, stop_message, show_stop_message)

        # Update the camera position based on player's movement
        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            if player.x_vel > 0:
                offset_x += player.x_vel + camera_speed_x
            elif player.x_vel < 0 and player.rect.left - offset_x <= scroll_area_width:
                offset_x += player.x_vel - camera_speed_x

        # Similarly, update the camera position for vertical movement
        if ((player.rect.bottom - offset_y >= HEIGHT - scroll_area_height) and player.y_vel > 0) or (
                (player.rect.top - offset_y <= scroll_area_height) and player.y_vel < 0):
            offset_y += player.y_vel + camera_speed_y


        # Check for checkpoint 2
        if offset_x >= checkpoint2_distance:
            if score < required_score:
                # Player cannot pass checkpoint 2 without required score
                if player.x_vel > 0:
                    player.rect.x -= player.x_vel  # Move player back
                elif player.x_vel < 0:
                    player.rect.x -= player.x_vel  # Move player back
                player.x_vel = 0  # Stop player's horizontal movement
                show_stop_message = True
            else:
                show_stop_message = False

        # Check for game restart
        if restart_condition_met:
            offset_x, offset_y = restart(window, player, offset_x, offset_y, camera_speed_x, camera_speed_y, scroll_area_width, scroll_area_height)
            restart_condition_met = False  # Reset the restart condition after restart


    pygame.quit()
    quit()

def wait_for_restart():
       waiting = True
       while waiting:
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False


if __name__ == "__main__":
    # Create a list of fire objects
    fire1 = Fire(225, HEIGHT - block_size - 64, 16, 32)
    fire2 = Fire(425, HEIGHT - block_size - 64, 16, 32) 
    fire3 = Fire(725, HEIGHT - block_size - 64, 16, 32) 
    fire4 = Fire(1325, HEIGHT - block_size - 64, 16, 32) 
    fire5 = Fire(1625, HEIGHT - block_size * 2 - 64, 16, 32) 
    fire6 = Fire(1855, HEIGHT - block_size - 64, 16, 32) 
    fire7 = Fire(2150, HEIGHT - block_size - 64, 16, 32) 
    fire8 = Fire(2725, HEIGHT - block_size - 64, 16, 32) 
    fire9 = Fire(3675, HEIGHT - block_size - 64, 16, 32) 
    fire10 = Fire(4450, HEIGHT - block_size - 64, 16, 32) 
    fire11 = Fire(4150, HEIGHT - block_size * 6 - 64, 16, 32) 
    fire12 = Fire(3975, HEIGHT - block_size * 6 - 64, 16, 32)  
    fire13 = Fire(4825, HEIGHT - block_size - 64, 16, 32) 
    fire14 = Fire(5500, HEIGHT - block_size - 64, 16, 32) 
    fire15 = Fire(5500, HEIGHT - block_size * 7 - 64, 16, 32) 
    fire16 = Fire(6075, HEIGHT - block_size * 4 - 64, 16, 32) 
    fire17 = Fire(6650, HEIGHT - block_size - 64, 16, 32) 
    fire18 = Fire(6850, HEIGHT - block_size - 64, 16, 32) 
    fire19 = Fire(7030, HEIGHT - block_size - 64, 16, 32) 
    fire20 = Fire(7220, HEIGHT - block_size - 64, 16, 32) 
    fire21 = Fire(7410, HEIGHT - block_size - 64, 16, 32) 
    fire22 = Fire(7900, HEIGHT - block_size * 7 - 64, 16, 32) 
    fire23 = Fire(7900, HEIGHT - block_size * 5 - 64, 16, 32) 
    fire24 = Fire(8675, HEIGHT - block_size * 3 - 64, 16, 32) 
    fire25 = Fire(8965, HEIGHT - block_size * 3 - 64, 16, 32) 
    fire26 = Fire(9350, HEIGHT - block_size - 64, 16, 32)
    fire27 = Fire(9446, HEIGHT - block_size - 64, 16, 32) 
    fire28 = Fire(9542, HEIGHT - block_size - 64, 16, 32) 
    fire29 = Fire(9638, HEIGHT - block_size - 64, 16, 32) 
    fire30 = Fire(9734, HEIGHT - block_size - 64, 16, 32) 
    fire31 = Fire(9830, HEIGHT - block_size - 64, 16, 32) 
    fire32 = Fire(9926, HEIGHT - block_size - 64, 16, 32) 
    fire33 = Fire(10022, HEIGHT - block_size - 64, 16, 32) 
    fire34 = Fire(10118, HEIGHT - block_size - 64, 16, 32) 
    fire35 = Fire(10214, HEIGHT - block_size - 64, 16, 32) 
    fire36 = Fire(10310, HEIGHT - block_size - 64, 16, 32) 
    fire37 = Fire(10406, HEIGHT - block_size - 64, 16, 32) 
    fire38 = Fire(10502, HEIGHT - block_size - 64, 16, 32) 
    fire39 = Fire(10598, HEIGHT - block_size - 64, 16, 32) 
    fire40 = Fire(10694, HEIGHT - block_size - 64, 16, 32) 
    fire41 = Fire(10790, HEIGHT - block_size - 64, 16, 32) 
    fire42 = Fire(10886, HEIGHT - block_size - 64, 16, 32) 
    fire43 = Fire(10982, HEIGHT - block_size - 64, 16, 32) 
    fire44 = Fire(11078, HEIGHT - block_size - 64, 16, 32) 
    fire45 = Fire(11174, HEIGHT - block_size - 64, 16, 32) 
    fire46 = Fire(11270, HEIGHT - block_size - 64, 16, 32)  
    fire47 = Fire(11366, HEIGHT - block_size - 64, 16, 32) 
    fire48 = Fire(11462, HEIGHT - block_size - 64, 16, 32) 
    fire49 = Fire(11558, HEIGHT - block_size - 64, 16, 32) 
    fire50 = Fire(11654, HEIGHT - block_size - 64, 16, 32) 
    fire51 = Fire(11750, HEIGHT - block_size - 64, 16, 32) 
    fire52 = Fire(11846, HEIGHT - block_size - 64, 16, 32) 
    fire53 = Fire(11942, HEIGHT - block_size - 64, 16, 32) 
    fire54 = Fire(12038, HEIGHT - block_size - 64, 16, 32)
    fire55 = Fire(9542, HEIGHT - block_size * 5 - 64, 16, 32) 
    fire56 = Fire(10118, HEIGHT - block_size * 4 - 64, 16, 32) 
    fire57 = Fire(10694, HEIGHT - block_size * 5 - 64, 16, 32) 
    fire58 = Fire(11270, HEIGHT - block_size * 4 - 64, 16, 32) 
    fire59 = Fire(11846, HEIGHT - block_size * 5 - 64, 16, 32)
    fire60 = Fire(12422, HEIGHT - block_size - 64, 16, 32) 
    fire61 = Fire(12518, HEIGHT - block_size - 64, 16, 32)
    fire62 = Fire(12614, HEIGHT - block_size - 64, 16, 32)
    fire63 = Fire(12806, HEIGHT - block_size - 64, 16, 32) 
    fire64 = Fire(12902, HEIGHT - block_size - 64, 16, 32) 
    fire65 = Fire(12998, HEIGHT - block_size - 64, 16, 32)
    fire66 = Fire(13190, HEIGHT - block_size - 64, 16, 32) 
    fire67 = Fire(13286, HEIGHT - block_size - 64, 16, 32) 
    fire68 = Fire(13382, HEIGHT - block_size - 64, 16, 32) 
    fire69 = Fire(13574, HEIGHT - block_size - 64, 16, 32) 
    fire70 = Fire(13670, HEIGHT - block_size - 64, 16, 32)
    fire71 = Fire(13766, HEIGHT - block_size - 64, 16, 32) 

    fire_objects = [fire1, fire2, fire3, fire4, fire5, fire6, fire7, fire8, fire9, fire10, 
                    fire11, fire12, fire13, fire14, fire15, fire16, fire17, fire18, fire19, fire20,
                    fire21, fire22, fire23, fire24, fire25, fire26, fire27, fire28, fire29, fire30,
                    fire31, fire32, fire33, fire34, fire35, fire36, fire37, fire38, fire39, fire40,
                    fire41, fire42, fire43, fire44, fire45, fire46, fire47, fire48, fire49, fire50,
                    fire51, fire52, fire53, fire54, fire55, fire56, fire57, fire58, fire59, fire60, 
                    fire61, fire62, fire63, fire64, fire65, fire66, fire67, fire68, fire69, fire70,
                    fire71]
    main(window, fire_objects)
