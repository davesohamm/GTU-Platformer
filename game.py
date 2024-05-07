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
FPS = 60
PLAYER_VEL = 4
offset_x = 0
offset_y = 0
scroll_area_width = 200
scroll_area_height = 200
camera_speed_x = 5
camera_speed_y = 5
block_size = 96
window = pygame.display.set_mode((WIDTH, HEIGHT))
# Define custom event for apple collisions
APPLE_COLLISION_EVENT = pygame.USEREVENT + 1
TELEPORT_LOCATION = (-1000, -1000)


def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def start_menu(window):
    title_font = pygame.font.Font('kalam.ttf', 80)
    start_font = pygame.font.Font('kalam.ttf', 36)
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
        title_text = title_font.render("GTU Escape", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 5))
        window.blit(title_text, title_rect)

        # Draw a "Start" button
        start_text = start_font.render("Press SPACE to Start", True, (0, 0, 0))
        start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 3.5))
        window.blit(start_text, start_rect)

        pygame.display.update()

def game_over_screen(window):
    # Font for game over message
    font = pygame.font.Font('kalam.ttf', 60)
    
    # Display "GAME OVER" message with black rectangle background
    game_over_text = font.render("GAME OVER", True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    pygame.draw.rect(window, (0, 0, 0), game_over_rect.inflate(20, 10))  # Black rectangle background
    window.blit(game_over_text, game_over_rect)

    # Load game over death picture
    death_image = pygame.image.load(r"Y:\GTU-Platformer\assets\Other\dead.png").convert_alpha()
    death_image = pygame.transform.scale(death_image, (200, 200))

    # Display the game over death picture on top of "GAME OVER"
    death_rect = death_image.get_rect(midbottom=(WIDTH // 2, game_over_rect.top - 20))
    window.blit(death_image, death_rect)
    
    # Display "Press SPACE to restart" message with black rectangle background
    restart_font = pygame.font.Font('kalam.ttf', 36)
    restart_text = restart_font.render("Press SPACE to restart", True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 1.5))
    pygame.draw.rect(window, (0, 0, 0), restart_rect.inflate(20, 10))  # Black rectangle background
    window.blit(restart_text, restart_rect)
    
    pygame.display.update()

CHARACTERS = ["MaskDude", "NinjaFrog", "PinkMan","VirtualGuy"]
def select_character(window, CHARACTERS):
    # Font for character names
    font = pygame.font.Font('kalam.ttf', 40)

    # Colors
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    # List of character names and their corresponding images
    character_names = list(CHARACTERS)
    character_images = {
        "VirtualGuy": pygame.image.load(r"Y:/GTU-Platformer/assets/MainCharacters/VirtualGuy/jump.png").convert_alpha(),
        "MaskDude": pygame.image.load(r"Y:/GTU-Platformer/assets/MainCharacters/MaskDude/jump.png").convert_alpha(),
        "PinkMan": pygame.image.load(r"Y:/GTU-Platformer/assets/MainCharacters/PinkMan/jump.png").convert_alpha(),
        "NinjaFrog": pygame.image.load(r"Y:/GTU-Platformer/assets/MainCharacters/NinjaFrog/jump.png").convert_alpha()
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

        # Drawing the window
        window.fill((30, 30, 30))  # Fill background with a dark color

        # Drawing title
        title_font = pygame.font.Font('freesansbold.ttf', 50)
        nav_font = pygame.font.Font('freesansbold.ttf', 15)
        title_text = title_font.render("Choose Any Character:", True, WHITE)
        title_rect = title_text.get_rect(center=(window.get_width() // 2, 50))
        window.blit(title_text, title_rect)
        nav_text = nav_font.render("Use UP & DOWN to navigate, and press ENTER to select", True, WHITE)
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

            # Add a highlight effect for the selected character
            if i == selected_index:
                pygame.draw.rect(window, WHITE, text_rect, 3)  # White border

        # Add some decorative elements (optional)
        # Example: Drawing a background image or other visual effects

        pygame.display.flip()

    # If the user closes the window without selecting, return None
    return None

def select_terrain(window):
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

        # Drawing the window
        window.fill((30, 30, 30))  # Fill background with a dark color

        # Drawing title
        title_font = pygame.font.Font('freesansbold.ttf', 50)
        nav_font = pygame.font.Font('freesansbold.ttf', 15)
        title_text = title_font.render("Choose Terrain:", True, WHITE)
        title_rect = title_text.get_rect(center=(window.get_width() // 2, 50))
        window.blit(title_text, title_rect)
        nav_text = nav_font.render("Use UP & DOWN to navigate, and press ENTER to select", True, WHITE)
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
        self.y_vel = -self.GRAVITY * 9
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
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

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
    ANIMATION_DELAY = 5

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


def draw(window, background, bg_image, player, objects, offset_x):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x)

    pygame.display.update()

def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
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
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()
    return collided_object


def handle_move(player, objects):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)

    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]

    for obj in to_check:
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
    
    objects = []
    
    pygame.mixer.music.load("gtusong.mp3")
     # Load and play the background music
    pygame.mixer.music.play(-1)  # -1 makes it play in a loop

    player = Player(100, 100, 50, 50, character_name)

    num_blocks = 200  # Adjust this number to change the number of blocks
    blocks = generate_blocks(block_size, num_blocks, terrain_rect) 

    fire1 = Fire(225, HEIGHT - block_size - 64, 16, 32)
    fire2 = Fire(425, HEIGHT - block_size - 64, 16, 32) 
    fire3 = Fire(725, HEIGHT - block_size - 64, 16, 32) 
    fire4 = Fire(1325, HEIGHT - block_size - 64, 16, 32) 
    fire5 = Fire(1625, HEIGHT - block_size * 2 - 64, 16, 32) 
    fire6 = Fire(1855, HEIGHT - block_size - 64, 16, 32) 
    fire7 = Fire(2150, HEIGHT - block_size - 64, 16, 32) 
    start1 = Start(-20, HEIGHT - block_size * 2.6 - 64, 64, 64)
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
    apple_objects = [apple1, apple2, apple3, apple4, apple5, apple6, apple7, apple8, apple9, apple10, apple11 ,apple12, apple13, apple14, apple15, apple16, apple17, apple18, apple19]

    font = pygame.font.Font('freesansbold.ttf', 25)
    fire1.on()
    fire2.on()
    fire3.on()
    fire4.on()
    fire5.on()
    fire6.on()
    fire7.on()
    start1.on()
    floor = [Block(i * block_size, HEIGHT - block_size, block_size, terrain_rect)
         for i in range((-WIDTH * 2) // block_size, (WIDTH * 15) // block_size)]

    objects = [*floor, *blocks, Block(0, HEIGHT - block_size * 2, block_size, terrain_rect), Block(block_size, HEIGHT - block_size * 3, block_size, terrain_rect),
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
           Block(block_size * 28, HEIGHT - block_size * 2, block_size, terrain_rect), Block(block_size * 29, HEIGHT - block_size * 2, block_size, terrain_rect),  Block(block_size * 30, HEIGHT - block_size * 2, block_size, terrain_rect), Block(block_size * 31, HEIGHT - block_size * 2, block_size, terrain_rect),
           Block(block_size * 32, HEIGHT - block_size * 2, block_size, terrain_rect), Block(block_size * 25, HEIGHT - block_size * 4, block_size, terrain_rect), Block(block_size * 26, HEIGHT - block_size * 4, block_size, terrain_rect), Block(block_size * 27, HEIGHT - block_size * 4, block_size, terrain_rect), Block(block_size * 29, HEIGHT - block_size * 4, block_size, terrain_rect),
           Block(block_size * 30, HEIGHT - block_size * 4, block_size, terrain_rect), Block(block_size * 31, HEIGHT - block_size * 4, block_size, terrain_rect), Block(block_size * 29, HEIGHT - block_size * 8, block_size, terrain_rect),
            Block(block_size * 26, HEIGHT - block_size * 6, block_size, terrain_rect), Block(block_size * 27, HEIGHT - block_size * 6, block_size, terrain_rect), Block(block_size * 27, HEIGHT - block_size * 8, block_size, terrain_rect),
           Block(block_size * 28, HEIGHT - block_size * 6, block_size, terrain_rect), Block(block_size * 29, HEIGHT - block_size * 6, block_size, terrain_rect),  Block(block_size * 30, HEIGHT - block_size * 6, block_size, terrain_rect),
           fire1, fire2, fire3, fire4, fire5, fire6, fire7, start1, *apple_objects ]
    
    offset_x = 0
    offset_y = 0
    scroll_area_width = 200
    scroll_area_height = 200
    camera_speed_x = 5
    camera_speed_y = 5
    run = True
    is_jumping = False
    score = 0
    game_over = False 
    restart_condition_met = False

    while run:
        clock.tick(FPS)
        # Update and draw player
        player.loop(FPS)
        player.draw(window, offset_x)
        # Update and draw fires
        for fire in fire_objects:
          fire.update()
          fire.draw(window, offset_x)
        # Update and draw start arrow
        for start1 in objects:
            start1.update()
            start1.draw(window, offset_x)

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
                       
        # Check for collision between player and fire objects
        for fire in fire_objects:
            if pygame.sprite.collide_mask(player, fire):
                # If collision detected, set game over state to True
                game_over = True
                break

        # Display the scoreboard
        score_text = font.render("Score: " + str(score), True, (0, 0, 0))
        window.blit(score_text, (10, 10))

        if game_over:
                        # Display game over screen
            game_over_screen(window)
            pygame.mixer.music.stop()  # Stop the background music
            pygame.display.update()

            # Wait for player to press space to restart
            wait_for_restart()
            offset_x, offset_y = restart(window, player, offset_x, offset_y, camera_speed_x, camera_speed_y, scroll_area_width, scroll_area_height)

            # Reset game state
            # Reset player position, score, etc.
            game_over = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()

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
        start1.loop()
        handle_move(player, objects)
        draw(window, background, bg_image, player, objects, offset_x)

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

        # Other game logic...

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
    fire_objects = [fire1, fire2, fire3, fire4, fire5, fire6, fire7]
    main(window, fire_objects)
