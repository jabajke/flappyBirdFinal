import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

font1 = pygame.font.Font(None, 35)
font2 = pygame.font.Font(None, 80)

imgBG = pygame.image.load('images/background.png')
imgBird = pygame.image.load('images/bird.png')
imgPT = pygame.image.load('images/pipe_top.png')
imgPB = pygame.image.load('images/pipe_bottom.png')

py, sy, ay = HEIGHT // 2, 0, 0
player = pygame.Rect(WIDTH // 3, py, 34, 24)
frame = 0

state = 'start'
timer = 10

pipes = []
bges = [pygame.Rect(0, 0, 288, 600)]

lives = 3
scores = 0

play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

    press = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()
    click = press[0] or keys[pygame.K_SPACE]

    if timer > 0:
        timer -= 1

    frame = (frame + 0.2) % 4

    for i in range(len(bges) - 1, -1, -1):
        bg = bges[i]
        bg.x -= 1

        if bg.right < 0:
            bges.remove(bg)

        if bges[len(bges) - 1].right <= WIDTH:
            bges.append(pygame.Rect(bges[len(bges) - 1].right, 0, 288, 600))

    for i in range(len(pipes) - 1, -1, -1):
        pipe = pipes[i]
        pipe.x -= 3

        if pipe.right < 0:
            pipes.remove(pipe)

    if state == 'start':
        if click and timer == 0 and len(pipes) == 0:
            state = 'play'

        py += (HEIGHT // 2 - py) * 0.1
        player.y = py

    elif state == 'play':
        if click:
            ay = -2
        else:
            ay = 0

        py += sy
        sy = (sy + ay + 1) * 0.98
        player.y = py

        if len(pipes) == 0 or pipes[len(pipes) - 1].x < WIDTH - 200:
            pipes.append(pygame.Rect(WIDTH, 0, 52, 200))
            pipes.append(pygame.Rect(WIDTH, 400, 52, 200))

        if player.top < 0 or player.bottom > HEIGHT:
            state = 'fall'

        for pipe in pipes:
            if player.colliderect(pipe):
                state = 'fall'

    elif state == 'fall':
        sy, ay = 0, 0
        state = 'start'
        timer = 60

    else:
        pass

    window.fill('black')
    for bg in bges:
        window.blit(imgBG, bg)

    for pipe in pipes:
        if pipe.y == 0:
            rect = imgPT.get_rect(bottomleft=pipe.bottomleft)
            window.blit(imgPT, rect)
        else:
            rect = imgPB.get_rect(topleft=pipe.topleft)
            window.blit(imgPB, rect)

    image = imgBird.subsurface(34 * int(frame), 0, 34, 24)
    image = pygame.transform.rotate(image, -sy * 2)
    window.blit(image, player)

    text = font1.render('Очки: ' + str(scores), True, 'black')
    window.blit(text, (10, 10))

    text = font1.render('Жизни: ' + str(lives), True, 'black')
    window.blit(text, (10, HEIGHT - 30))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
