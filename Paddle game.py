import pygame
import random
# Initialize Pygame
pygame.init()
# Custom event IDs for color change events
SPRITE_COLOR_CHANGE_EVENT = pygame.USEREVENT + 1
BACKGROUND_COLOR_CHANGE_EVENT = pygame.USEREVENT + 2
# Define basic colors using pygame.Color
BLUE = pygame.Color('blue')
LIGHTBLUE = pygame.Color('lightblue')
DARKBLUE = pygame.Color('darkblue')
YELLOW = pygame.Color('yellow')
MAGENTA = pygame.Color('magenta')
ORANGE = pygame.Color('orange')
WHITE = pygame.Color('white')
RED = pygame.Color('red')
# Sprite class representing the ball
class Sprite(pygame.sprite.Sprite):
    def __init__(self, color, height, width):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.velocity = [random.choice([-2, 2]), random.choice([-2, 2])]
    def update(self):
        self.rect.move_ip(self.velocity)
        boundary_hit = False
        # Check for collision with left or right boundaries
        if self.rect.left <= 0 or self.rect.right >= 500:
            self.velocity[0] = -self.velocity[0]
            boundary_hit = True
        # Check for collision with top boundary
        if self.rect.top <= 0:
            self.velocity[1] = -self.velocity[1]
            boundary_hit = True
        # If the ball hits the bottom boundary, it's game over
        if self.rect.bottom >= 400:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        if boundary_hit:
            pygame.event.post(pygame.event.Event(SPRITE_COLOR_CHANGE_EVENT))
            pygame.event.post(pygame.event.Event(BACKGROUND_COLOR_CHANGE_EVENT))
    def change_color(self):
        self.image.fill(random.choice([YELLOW, MAGENTA, ORANGE, WHITE]))
class paddle(pygame.sprite.Sprite):
  def __init__(self, color, height, width):
    super().__init__()
    self.image = pygame.Surface([width, height])
    self.image.fill(color)
    self.rect = self.image.get_rect()
  def update(self, keys):
    if keys[pygame.K_LEFT] and self.rect.left > 0:
      self.rect.x -= 5
    if keys[pygame.K_RIGHT] and self.rect.right < 500:
      self.rect.x += 5
def change_background_color():
  global bg_color
  bg_color = [random.choice([BLUE, LIGHTBLUE, DARKBLUE])]
#Initializee sprites
all_sprites_list = pygame.sprite.Group()
ball = Sprite(WHITE, 20, 20)
ball.rect.x = random.randint(0, 480)
ball.rect.y = random.randint(0, 200)
all_sprites_list.add(ball)
paddle = paddle(RED, 10, 80)
paddle.rect.x = 220
paddle.rect.y = 370
all_sprites_list.add(paddle)
#Window
screen = pygame.display.set_mode((500, 400))
pygame.display.set_caption("Colorful Bounce")
bg_color = BLUE
screen.fill(bg_color)
exit = False
clock = pygame.time.Clock()
score = 0
while not exit:
  keys = pygame.key.get_pressed()
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      exit = True
    elif event.type == SPRITE_COLOR_CHANGE_EVENT:
      ball.change_color()
    elif event.type == BACKGROUND_COLOR_CHANGE_EVENT:
      change_background_color()
  paddle.update(keys)
  ball.update()
  if pygame.sprite.collide_rect(ball, paddle):
    ball.velocity[1] = -ball.velocity[1]
    score += 1
    print(f"score: {score}")
  screen.fill(bg_color)
  all_sprites_list.draw(screen)
  font = pygame.font.SysFont(None, 36)
  score_text = font.render(f"score: {score}", True, WHITE)
  screen.blit(score_text, (10, 10))
  pygame.display.flip()
  clock.tick(60)
pygame.quit()
