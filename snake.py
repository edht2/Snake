from config import *
from piece import Piece

exit = False
grid_size = 30
cube_size = 30
snake = [Piece(1, 4, 1, grid_size), Piece(2, 4, 1, grid_size)]
food = Piece(randint(10,900/grid_size), randint(10,900/grid_size), 0, grid_size)
box = pygame.Rect(grid_size, grid_size, screen.get_width()-grid_size, screen.get_height()-grid_size)
font = pygame.font.Font('CONSOLA.TTF', 40)
score = 0
death = False

while not exit:
  dt = clock.tick(fps) # set fps
  screen.fill('#001111')
  for event in pygame.event.get():
    if event.type == KEYDOWN:
      if event.key == K_BACKSPACE:
        exit = True
      elif event.type == QUIT:
        exit = True
      if event.key == K_LEFT:
        if snake[0].dir+2 != 3:
          snake[0].dir = 3
      elif event.key == K_UP:
        if snake[0].dir+2 != 2:
          snake[0].dir = 2
      elif event.key == K_RIGHT:
        if snake[0].dir-2 != 1:
          snake[0].dir = 1
      elif event.key == K_DOWN:
        if snake[0].dir-2 != 0:
          snake[0].dir = 0
      if event.key == K_TAB:
        snake = [Piece(1, 4, 0, grid_size), Piece(1, 3, 0, grid_size), Piece(1, 2, 0, grid_size), Piece(1, 1, 0, grid_size), Piece(2, 4, 0, grid_size), Piece(2, 3, 0, grid_size), Piece(2, 2, 0, grid_size), Piece(2, 1, 0, grid_size)]
        
  # Snake
  head = pygame.Rect(snake[0].x*grid_size, snake[0].y*grid_size, cube_size-1, cube_size-1)
  for index, snake_piece in enumerate(snake):
    segment = pygame.Rect(snake_piece.x*grid_size, snake_piece.y*grid_size, cube_size, cube_size)
    pygame.draw.rect(screen, (0, 255-index*2, 0), segment)
    
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
      fps = 10
      cube_size -= 10
    else:
      fps = 4

    
  # Food
  food_rect = pygame.Rect(food.x*grid_size, food.y*grid_size, cube_size, cube_size)
  pygame.draw.rect(screen, (255, 0, 0), food_rect)

  if head.colliderect(food_rect):
    snake.append(Piece(snake[len(snake)-1].x, snake[len(snake)-1].y, snake[len(snake)-1].dir, grid_size))
    valid_pos = True
    score += 1
    while valid_pos:
      food = Piece(randint(10,900/grid_size), randint(10,900/grid_size), 0, grid_size)
      for snake_piece in snake:
        if not (food.x == snake_piece.x and food.y == snake_piece):
          valid_pos = False
      
  # Score
  score_font = font.render(f"score : {score}", True, (255,255,255))
  screen.blit(score_font, (0,0))

  pygame.display.flip() # display the frame
  
  
  