from config import *
from piece import Piece

def generate_food(snake):
  valid_pos = False
  while not valid_pos:
    x = randint(1,900/GRID_SIZE-1)
    y = randint(1,900/GRID_SIZE-1)
    invalid_attemt = False
    
    for snake_piece in snake:
      if x == snake_piece.x and y == snake_piece.y:
        invalid_attemt = True
    if not invalid_attemt:
      valid_pos = True
  return Piece(x, y, 0, GRID_SIZE)

def eat(score, snake):
  score += 1
  snake.append(Piece(snake[len(snake)-1].x, snake[len(snake)-1].y, snake[len(snake)-1].dir, GRID_SIZE))
  return snake, score

exit = False

# Game vars
difficulty = 3 # d+5=fps · where d=difficulty
GRID_SIZE = 20
cube_size = 20
snake = [Piece(1, 4, 1, GRID_SIZE), Piece(2, 4, 1, GRID_SIZE)]
food = generate_food(snake)

# Menu vars
menu = True
nhs = False
selected = 1
menu_tags = [
  ('Start ', 0) ]
hi_score_txt = open('hi-score.txt', 'r')
hi_score = int(hi_score_txt.readline().strip())
hi_score_txt.close()

box = pygame.Rect(0, 0, screen.get_width(), screen.get_height())
font = pygame.font.Font('CONSOLA.TTF', 60)
mfont = pygame.font.Font('CONSOLA.TTF', 20)
score = 0
death = False

while not exit:
  if not menu:
    fps = difficulty+4
  else:
    fps = 10
    
  dt = clock.tick(fps) # wait
  screen.fill('#001111')
  mtt = False 
  
  # Menu                                     
  if menu:
    index = 40
    
    menu_dimensions = pygame.Rect(screen.get_width()/2-150, screen.get_height()/2-150, 300, 300)
    menu_rect = pygame.draw.rect(screen, (240,240,240), menu_dimensions, 4)
    
    title = font.render('Snake', True, '#ffffff')   
    screen.blit(title, (menu_dimensions.x, menu_dimensions.y-70))                    
    
    if nhs: hs = f"New record - {hi_score}"
    else: hs = f"Score - {score}"
      
    text = mfont.render(hs, True, '#eeee00')
    screen.blit(text, (menu_rect.x+10, menu_rect.y+10))
    
    menu_options = menu_tags
    print(menu_tags)
      
    for i, option in enumerate(menu_options):
      index += 30
      focused_bc = None
      focused_i = ''
      focused_tc = '#ffffff'
      if selected == option[1]:
        focused_bc = '#ffffff'
        focused_tc = '#000000'
        focused_i = '> '
        
      option_text = f"{focused_i}{option[0]}"
      text = mfont.render(option_text, True, focused_tc, focused_bc)
      screen.blit(text, (menu_rect.x+10, menu_rect.y+index))
      
      try:
        if option[2]:
          for sub_option in option[3]:
            menu_options.insert(i+1, sub_option)
      except:
        pass
        
  
  for event in pygame.event.get():
    if event.type == KEYDOWN:
      if event.key == K_BACKSPACE:
        exit = True
      elif event.type == QUIT:
        exit = True
        
      # Menu navigation
      if event.key == K_DOWN and menu:
        if selected + 1 > len(menu_options) - 1:
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
          food = generate_food(snake)
          menu = False
          nhs = False
          score = 0
          
      # Snake navigation
      if event.key == K_LEFT and not menu and not mtt:
        if snake[0].dir+2 != 3:
          snake[0].dir = 3
          mtt = True
      elif event.key == K_UP and not menu and not mtt:
        if snake[0].dir+2 != 2:
          snake[0].dir = 2
          mtt = True
      elif event.key == K_RIGHT and not menu and not mtt:
        if snake[0].dir-2 != 1:
          snake[0].dir = 1
          mtt = True
      elif event.key == K_DOWN and not menu and not mtt:
        if snake[0].dir-2 != 0:
          snake[0].dir = 0
          mtt = True
      
  # Snake
  if not menu:
    colour_lg = True
    head = pygame.Rect(snake[0].x*GRID_SIZE, snake[0].y*GRID_SIZE, cube_size-10, cube_size-10)
    for index, snake_piece in enumerate(snake):
      segment = pygame.Rect(snake_piece.x*GRID_SIZE, snake_piece.y*GRID_SIZE, cube_size, cube_size)
      
      if index == 0:
        if len(snake) > 4:
          segment = pygame.Rect(snake_piece.x*GRID_SIZE-3, snake_piece.y*GRID_SIZE-3, cube_size+6, cube_size+6)
        pygame.draw.rect(screen, (255, 255, 0), segment)
      elif colour_lg: 
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
        snake.insert(0, Piece(snake[0].x, snake[0].y+1, snake[0].dir, GRID_SIZE))
      elif snake[0].dir == 1:
        snake.insert(0, Piece(snake[0].x+1, snake[0].y, snake[0].dir, GRID_SIZE))
      elif snake[0].dir == 2:
        snake.insert(0, Piece(snake[0].x, snake[0].y-1, snake[0].dir, GRID_SIZE))
      elif snake[0].dir == 3:
        snake.insert(0, Piece(snake[0].x-1, snake[0].y, snake[0].dir, GRID_SIZE))
      snake.pop(len(snake)-1)
    else:
      if cube_size > 0:
        fps = 20
        cube_size -= 5
      else:
        fps = difficulty+4
        menu = True 
        death = False
        cube_size = GRID_SIZE
        snake = [Piece(1, 4, 1, GRID_SIZE), Piece(2, 4, 1, GRID_SIZE)]

    
  # Food
  if not menu:
    food_rect = pygame.Rect(food.x*GRID_SIZE, food.y*GRID_SIZE, cube_size, cube_size)
    pygame.draw.rect(screen, (255, 0, 0), food_rect)

    if head.colliderect(food_rect):
      foo = eat(score, snake)
      snake = foo[0]
      score = foo[1]
      food = generate_food(snake)
      
     
    # Score
    score_font = font.render(f"{score}", True, (255,255,255))
    if score > hi_score:
      score_file = open('hi-score.txt', 'w')
      score_file.write(str(score))
      score_file.close()
      hi_score = score
      nhs = True
    screen.blit(score_font, (430,0))

  pygame.display.flip() # display the frame
  
  
  
  