import pygame, sys, random
from pygame import mixer 

#tạo hàm 
def draw_floor():
    screen.blit(floor,(floor_x_pos,650)) #gọi ra biến load cái sàn
    screen.blit(floor,(floor_x_pos+432,650)) 
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (500,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop = (500,random_pipe_pos-700))
    return bottom_pipe, top_pipe
def move_pipe(pipes): #nhận các ống từ list và di chuyển sang bên trái 
    for pipe in pipes: 
        pipe.centerx -= 5
    return pipes
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 768:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True) #true --> lật theo chiều y hoặc x, Flase --> không lật 
            screen.blit(flip_pipe,pipe)
def add_score(pipes):
    for pipe in pipes:
        global score
        if pipe.centerx <= 20:
            score +=0.5 
            pipes.remove(pipe)
def check_collistion(pipes):#pipe_list được đưa vào pipes, với pipe_list là một list
    for pipe in pipes:
        if bird_rect.colliderect(pipe): #2 khối hình chữ nhật, cụ thể hơn là chim và cột chạm nhau sẽ trả ra false, không thì trả là true 
            hit_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650: #nếu chim đi quá trục y khoảng âm 75 pixel hay dương 650 pixel thì sẽ tính là false, không thì trả là true 
        return False
    return True
def rotate_bird(bird1): #bird được đưa vào bird1, với bird là một list gồm các surface: bird_down, bird_mid  và bird_up
    new_bird = pygame.transform.rotozoom(bird1,bird_movement*3,1)
    return new_bird
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird, new_bird_rect
def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game over':
        score_surface = game_font.render(f'Score: {int(score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}',True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (216,610))
        screen.blit(high_score_surface,high_score_rect)
def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score
def hitscore_sound(pipes):
    global pipe
    for pipe in pipes:
        if pipe.centerx <= 20:
            score_sound.play()



a = pygame.image.load('assets/ok.png')
pygame.display.set_icon(a) #chỉnh icon của sổ 

pygame.mixer.pre_init(frequency=44100, size=-16, channels =2, buffer=512) #chen am thanh sao cho thich hop hon

pygame.init() # khỏi tạo 

screen = pygame.display.set_mode((432,768)) #tạo ra cửa sổ pygame 
clock = pygame.time.Clock() # tạo ra một biến điều chỉnh fps của game 
game_font = pygame.font.Font('04B_19.ttf',40)# kiểu chữ từ file 

#tạo ra các biến khác cho trò chơi
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0

#tạo ra các biến để load hình ảnh bg và sàn (floor)
bg = pygame.image.load('assets/background-night.png')
bg = pygame.transform.scale2x(bg) #phóng to 2 lần 

#tạo sàn 
floor = pygame.image.load('assets/floor.png')
floor = pygame.transform.scale2x(floor)

#tạo ta một biến riêng để cái sàn nó di chuyển 
floor_x_pos = 0

#tạo chym 
#bird = pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
#bird = pygame.transform.scale2x(bird)
bird_down = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png')).convert_alpha()
bird_mid = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png')).convert_alpha()
bird_up = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png')).convert_alpha()
bird_list = [bird_down, bird_mid, bird_up]
bird_index = 0
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center = (100,384)) #tọa độ của hình chữ nhật con chim 

#tạo timer cho chym 
birdflap = pygame.USEREVENT + 1 #Usserevent có giá trị là 24, dòng này cho mỗi lần loop là gửi một tín hiệu event từ 24 đến 32. Còn 1 đến 23 event đầu đã bị pygame sử dụng trước rồi 
pygame.time.set_timer(birdflap,100) #dòng này lầ timer, nghĩa là birdflap sẽ gửi tín hiệu event, sau đó bị trì hoãn với thời gian là 100 mili giây rồi gửi lặp lại
#tóm lại, lặp lại như vậy sẽ tạo ra chuyển động vỗ cánh cho con chim 

#tạo ống 
pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list =[]

#tao timer
spawnpipe = pygame.USEREVENT +1 
pygame.time.set_timer(spawnpipe,1100) #hoạt động tương tự với vỗ cánh ở trên 
pipe_height = [200,300,400] #tạo ra một list chứa các kích thước kahcs nhau của ống 

#tao man hinh ket thuc
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png')).convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (216,384))

#chen am thanh
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')

#while loop cua tro choi
while True:
    for event in pygame.event.get():
        #thoát chương trình 
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #tương tác bằng chuột 
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_presses = pygame.mouse.get_pressed()
            if mouse_presses[0] and game_active:
                #chuột trái được nhấn và game hoạt động thì  
                bird_movement = 0
                bird_movement =-6.5 #con chim nhảy lên một khoảng = 7 pixel theo chiều y 
                flap_sound.play() #phát tiếng khi chim nhảy 
            if mouse_presses[0] and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100,384)
                bird_movement = 0
                score = 0
        if event.type == spawnpipe:
            #khi tín hiệu event từ spawmpipe gửi đến thì pip_list sẽ thêm vào các phần tử tạo ra từ hàm create_pipe()
            pipe_list.extend(create_pipe())
        if event.type == birdflap:
            #hiển thị chuyển động vỗ cánh 
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
        bird, bird_rect = bird_animation()
            
    screen.blit(bg,(0,0)) #gọi ra biến load hình bg tai toa do (0,0)
    if game_active:
        #chym
        bird_movement += gravity    #tọa độ của chym tăng dần theo chiều y 
        rotated_bird = rotate_bird(bird) #gọi hàm ra và nhét bird là một list vào hàm đó 
        bird_rect.centery += bird_movement # khiến hình chữ nhật (con chim) chuyển động theo còn chim 
        screen.blit(rotated_bird,bird_rect)  #hiển thị mớ chuyển động đó ra màn hình 
        
        #va chạm 
        game_active = check_collistion(pipe_list) #gọi hàm ra và nhét pipe_list là một list vào hàm đó, nếu hàm trả ra false thì sẽ dừng trò chơi, nếu trả là true thì trò chơi tiếp tục 

        #ống 
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)

        #ghi điểm 
        add_score(pipe_list)
        score_display('main game')
        hitscore_sound(pipe_list)
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score,high_score)
        score_display('game over')
    #sàn 
    floor_x_pos -= 1 #cho cái sàn lùi về phía bên trái theo trục x 
    draw_floor()

    if floor_x_pos <= -432:
        floor_x_pos = 0
    pygame.display.flip() # không có dòng này thì tối màn hình game tối thui nha :>
    clock.tick(120)