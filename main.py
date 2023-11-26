import random
from sys import exit

import pygame

pygame.init()
clock = pygame.time.Clock()

win_height = 720
win_width = 551
window = pygame.display.set_mode((win_width, win_height))

bird_images = [
    pygame.image.load("assets/sprites/bluebird-downflap.png"),
    pygame.image.load("assets/sprites/bluebird-midflap.png"),
    pygame.image.load("assets/sprites/bluebird-upflap.png"),
]
skyline_image = pygame.image.load("assets/sprites/background.png")
ground_image = pygame.image.load("assets/sprites/ground.png")
top_pipe_image = pygame.image.load("assets/sprites/pipe-top.png")
bottom_pipe_image = pygame.image.load("assets/sprites/pipe-bottom.png")
game_over_image = pygame.image.load("assets/sprites/gameover.png")
start_image = pygame.image.load("assets/sprites/start.png")
image0 = pygame.image.load("assets/sprites/0.png")
image1 = pygame.image.load("assets/sprites/1.png")
image2 = pygame.image.load("assets/sprites/2.png")
image3 = pygame.image.load("assets/sprites/3.png")
image4 = pygame.image.load("assets/sprites/4.png")
image5 = pygame.image.load("assets/sprites/5.png")
image6 = pygame.image.load("assets/sprites/6.png")
image7 = pygame.image.load("assets/sprites/7.png")
image8 = pygame.image.load("assets/sprites/8.png")
image9 = pygame.image.load("assets/sprites/9.png")


die_sound = pygame.mixer.Sound("assets/audio/die.wav")
crash_sound = pygame.mixer.Sound("assets/audio/hit.wav")
score_sound = pygame.mixer.Sound("assets/audio/point.wav")
flap_sound = pygame.mixer.Sound("assets/audio/wing.wav")


scroll_speed = 1
bird_start_position = (100, 250)
score = 0


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = bird_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = bird_start_position
        self.image_index = 0
        self.vel = 0
        self.flap = False
        self.alive = True

    def update(self, user_input):
        # animate bird
        if self.alive:
            self.image_index += 1
        if self.image_index >= 30:
            self.image_index = 0
        self.image = bird_images[self.image_index // 10]

        # gravity and flap
        self.vel += 0.5
        if self.vel > 7:
            self.vel = 7
        if self.rect.y < 500:
            self.rect.y += int(self.vel)
        # can only flap once highest point reached
        if self.vel == 0:
            self.flap = False

        # rotate bird
        self.image = pygame.transform.rotate(self.image, self.vel * -7)

        # user input
        if (
            user_input[pygame.K_SPACE]
            and not self.flap
            and self.rect.y > 0
            and self.alive
        ):
            self.flap = True
            self.vel = -7
            pygame.mixer.Sound.play(flap_sound)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, image, pipe_type):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.enter, self.exit, self.passed = False, False, False
        self.pipe_type = pipe_type

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.x <= -win_width:
            self.kill()

        # Score
        global score
        if self.pipe_type == "bottom":
            if bird_start_position[0] > self.rect.topleft[0] and not self.passed:
                self.enter = True
            if bird_start_position[0] > self.rect.topright[0] and not self.passed:
                self.exit = True
            if self.enter and self.exit and not self.passed:
                self.passed = True
                score += 1
                pygame.mixer.Sound.play(score_sound)


class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = ground_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.x <= -win_width:
            self.kill()


def quit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


def main():
    global score

    # instantiate bird
    bird = pygame.sprite.GroupSingle()
    bird.add(Bird())

    # Setup pipes
    pipe_timer = 0
    pipes = pygame.sprite.Group()

    # Instantiate ground
    x_pos_ground, y_pos_ground = 0, 520
    ground = pygame.sprite.Group()
    ground.add(Ground(x_pos_ground, y_pos_ground))

    # Sound flag
    play_crash_sound = True

    run = True
    while run:
        quit_game()

        # Reset frame
        window.fill((0, 0, 0))

        # User input
        user_input = pygame.key.get_pressed()

        # Draw background
        window.blit(skyline_image, (0, 0))

        # Spawn ground
        if len(ground) <= 2:
            ground.add(Ground(win_width, y_pos_ground))

        # Draw - pipes, ground and bird
        pipes.draw(window)
        ground.draw(window)
        bird.draw(window)

        # Show Score
        digits = [int(i) for i in str(score)]
        i = 0
        for digit in digits:
            if digit == 0:
                window.blit(image0, (win_width // 2 - 20 + i * 15, win_height // 11))
            if digit == 1:
                window.blit(image1, (win_width // 2 - 20 + i * 15, win_height // 11))
            if digit == 2:
                window.blit(image2, (win_width // 2 - 20 + i * 15, win_height // 11))
            if digit == 3:
                window.blit(image3, (win_width // 2 - 20 + i * 15, win_height // 11))
            if digit == 4:
                window.blit(image4, (win_width // 2 - 20 + i * 15, win_height // 11))
            if digit == 5:
                window.blit(image5, (win_width // 2 - 20 + i * 15, win_height // 11))
            if digit == 6:
                window.blit(image6, (win_width // 2 - 20 + i * 15, win_height // 11))
            if digit == 7:
                window.blit(image7, (win_width // 2 - 20 + i * 15, win_height // 11))
            if digit == 8:
                window.blit(image8, (win_width // 2 - 20 + i * 15, win_height // 11))
            if digit == 9:
                window.blit(image9, (win_width // 2 - 20 + i * 15, win_height // 11))
            i += 1

        # Update - pipes, ground and bird
        if bird.sprite.alive:
            pipes.update()
            ground.update()
        bird.update(user_input)

        # Collision Detection
        collision_pipes = pygame.sprite.spritecollide(bird.sprites()[0], pipes, False)
        collision_ground = pygame.sprite.spritecollide(bird.sprites()[0], ground, False)
        if collision_pipes or collision_ground:
            bird.sprite.alive = False
            if collision_ground:
                window.blit(
                    game_over_image,
                    (
                        win_width // 2 - game_over_image.get_width() // 2,
                        win_width // 2 - game_over_image.get_width() // 2,
                    ),
                )
                if play_crash_sound:
                    play_crash_sound = False
                    pygame.mixer.Sound.play(crash_sound)
                if user_input[pygame.K_r]:
                    score = 0
                    main()
                    break

        # Spawn pipes
        if pipe_timer <= 0 and bird.sprite.alive:
            x_top, x_bottom = 550, 550
            y_top = random.randint(-600, -480)
            # randomize gap
            y_bottom = y_top + random.randint(130, 150) + bottom_pipe_image.get_height()
            pipes.add(Pipe(x_top, y_top, top_pipe_image, "top"))
            pipes.add(Pipe(x_bottom, y_bottom, bottom_pipe_image, "bottom"))
            pipe_timer = random.randint(180, 250)
        pipe_timer -= 1

        clock.tick(60)
        pygame.display.update()


main()
