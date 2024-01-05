from config import *
from piece import Piece

def generate_food(snake, grid_size):
  valid_pos = False
  while not valid_pos:
    food = Piece(randint(0,900/grid_size), randint(0,900/grid_size), 0, grid_size)
    for snake_piece in snake:
      if not food.x == snake_piece.x and food.y == snake_piece.y:
        valid_pos = True
  return food

exit = False
nhs = False
hi_score = int(open('hi-scores.txt', 'r').readline().strip())
grid_size = 30
cube_size = 30
menu = False
selected = 1
snake = [Piece(1, 4, 1, grid_size), Piece(2, 4, 1, grid_size)]
food = Piece(randint(10,900/grid_size), randint(10,900/grid_size), 0, grid_size)
box = pygame.Rect(grid_size, grid_size, screen.get_width()-grid_size, screen.get_height()-grid_size)
font = pygame.font.Font('CONSOLA.TTF', 60)
mfont = pygame.font.Font('CONSOLA.TTF', 20)
score = 0
death = False
menu_options = [
  (' Start ', 0),
  (' Difficulty ', 1)
]

while not exit:
  dt = clock.tick(fps) # set fps
  screen.fill('#001111')
  
  # Menu                                     
  if menu:
    fps = 10
    index = 0
    title = font.render('Snake', True, '#ffffff')                               
    menu_dimensions = pygame.Rect(screen.get_width()/2-150, screen.get_height()/2-150, 300, 300)
    screen.blit(title, (menu_dimensions.x, menu_dimensions.y-70))
    menu_rect = pygame.draw.rect(screen, (240,240,240), menu_dimensions, 2)
    for menu_option in menu_options:
      index += 30
      focused_bc = None
      focused_i = ''
      focused_tc = '#ffffff'
      if selected == menu_option[1]:
        focused_bc = '#ffffff'
        focused_tc = '#000000'
        focused_i = '> '
        
      option = f"{focused_i}{menu_option[0]}"
      text = mfont.render(option, True, focused_tc, focused_bc)
      screen.blit(text, (menu_rect.x, menu_rect.y+index))
    
    
  for event in pygame.event.get():
    if event.type == KEYDOWN:
      if event.key == K_BACKSPACE:
        exit = True
      elif event.type == QUIT:
        exit = True
      if event.key == K_DOWN and menu:
        if selected + 1 > len(menu_options) - 1:
          print("top")
          selected = 0
        else:
          selected += 1
          
      if event.key == K_UP and menu:
        if selected - 1 < 0:
          selected = len(menu_options)-1
        else:
          selected -= 1
      
      if event.key == K_RIGHT and menu:
        if selected == 0:
          menu = False
          nhs = False
          
      if event.key == K_LEFT and not menu:
        if snake[0].dir+2 != 3:
          snake[0].dir = 3
      elif event.key == K_UP and not menu:
        if snake[0].dir+2 != 2:
          snake[0].dir = 2
      elif event.key == K_RIGHT and not menu:
        if snake[0].dir-2 != 1:
          snake[0].dir = 1
      elif event.key == K_DOWN and not menu:
        if snake[0].dir-2 != 0:
          snake[0].dir = 0
      
  # Snake
  if not menu:
    colour_lg = True
    head = pygame.Rect(snake[0].x*grid_size, snake[0].y*grid_size, cube_size-1, cube_size-1)
    for index, snake_piece in enumerate(snake):
      segment = pygame.Rect(snake_piece.x*grid_size, snake_piece.y*grid_size, cube_size, cube_size)
      if colour_lg:
        pygame.draw.rect(screen, (0, 255, 0), segment)
        colour_lg = False
      else:
        pygame.draw.rect(screen, (0, 150, 0), segment)
        colour_lg = True
      
      if head.colliderect(segment) and index != 0:
        death = True
      
      if not head.colliderect(box):
        death = True
        
    if not death:
      if snake[0].dir == 0:
        snake.insert(0, Piece(snake[0].x, snake[0].y+1, snake[0].dir, grid_size))
      elif snake[0].dir == 1:
        snake.insert(0, Piece(snake[0].x+1, snake[0].y, snake[0].dir, grid_size))
      elif snake[0].dir == 2:
        snake.insert(0, Piece(snake[0].x, snake[0].y-1, snake[0].dir, grid_size))
      elif snake[0].dir == 3:
        snake.insert(0, Piece(snake[0].x-1, snake[0].y, snake[0].dir, grid_size))
      snake.pop(len(snake)-1)
    else:
      if cube_size > 0:
        fps = 20
        cube_size -= 5
      else:
        fps = 8
        menu = True 
        death = False
        cube_size = grid_size
        snake = [Piece(1, 4, 1, grid_size), Piece(2, 4, 1, grid_size)]

    
  # Food
  if not menu:
    food_rect = pygame.Rect(food.x*grid_size, food.y*grid_size, cube_size, cube_size)
    pygame.draw.rect(screen, (255, 0, 0), food_rect)

    if head.colliderect(food_rect):
      score += 1
      snake.append(Piece(snake[len(snake)-1].x, snake[len(snake)-1].y, snake[len(snake)-1].dir, grid_size))
      food = generate_food(snake, grid_size)
      
     
    # Score
    score_font = font.render(f"{score}", True, (255,255,255))
    if score > hi_score:
      open('hi-score.txt', 'r').write(score)
      hi_score = score
      nhs = True
    screen.blit(score_font, (430,0))

  pygame.display.flip() # display the frame
  
  
  