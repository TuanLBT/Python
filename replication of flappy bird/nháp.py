import pygame, sys
pygame.init()
c = pygame.display.set_mode((500,500))
pygame.display.set_caption('đây là một game ')

a = pygame.image.load('assets/ok.png')
pygame.display.set_icon(a) #chỉnh icon của sổ 
b = pygame.image.load('assets/back.png') # tạo ra một biến chứa surface 

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.flip() 
    c.blit(b,(0,0)) #đưa surface ra màn hình hiển thị
    pygame.draw.ellipse(b, (255,255,255), [(300,200),(100,300)], 5)