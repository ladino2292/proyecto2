import pygame
import math
import random

BLANCO = [255,255,255]
VERDE = [0,255,0]
ROJO = [255,0,0]
AZUL =  [0,0,255]
NEGRO = [0,0,0]

ANCHO = 600
ALTO = 400

class Jugador(pygame.sprite.Sprite):
    def __init__(self,color):
        #Constructor
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface([40,50])
        self.image.fill(color)
        self.rect=self.image.get_rect()
        self.rect.x=0
        self.rect.y=400
        self.velx=0
        self.vely=0
    #Retorna la posicion del jugador
    def pos(self):
        p=[self.rect.x,self.rect.y]
        return p

    def update(self):
        self.rect.x +=self.velx
        self.rect.y +=self.vely

        #Limites para que el jugador no salga de la pantalla
        if self.rect.x>(ANCHO-self.rect.width):
            self.rect.x=ANCHO-self.rect.width
            self.velx=0;

        if self.rect.x<0:
            self.rect.x=0
            self.velx=0;

        if self.rect.y<0:
            self.rect.y=0
            self.vely=0;

        if self.rect.y>(ALTO-self.rect.width):
            self.rect.y=(ALTO-self.rect.width)
            self.vely=0;

class Rival(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface([40,50])
        self.image.fill(BLANCO)
        self.rect=self.image.get_rect()
        self.velx=5
        self.disparar=False
        self.temporizador=random.randrange(1000)

    def pos(self):
        p=[self.rect.x,self.rect.y]
        return p

    def update(self):
        self.rect.x +=self.velx
        if self.rect.x>(ANCHO-self.rect.width):
            self.velx=-5
        if self.rect.x<0:
            self.velx=5
        self.temporizador -=1

class Proyectil(pygame.sprite.Sprite):
    def __init__(self,pos,color):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface([10,10])
        self.image.fill(color)
        self.rect=self.image.get_rect()
        self.rect.x=pos[0]
        self.rect.y=pos[1]
        self.vely=-20

    def update(self):
        self.rect.y+=self.vely



if __name__ == '__main__':
    pygame.init()
    #Declaracion de variables
    pantalla = pygame.display.set_mode([ANCHO,ALTO])
    reloj = pygame.time.Clock()
    jugadores=pygame.sprite.Group()
    rivales=pygame.sprite.Group()
    balas=pygame.sprite.Group()
    balasRival=pygame.sprite.Group()

    marcador1=0
    marcador2=0

    #Agregar jugador 1
    j=Jugador(VERDE)
    jugadores.add(j)

    #Agregar jugador 2
    '''j2=Jugador(ROJO)
    jugadores.add(j2)'''

    #Espacio en que se puede crear rivales
    n=10
    for i in range(n):
        r=Rival()
        r.rect.x=random.randrange(ANCHO)-r.rect.width
        r.rect.y=random.randrange(ALTO)-150
        rivales.add(r)

    #ciclo para la ventana
    fin = False
    while not fin:
        #Gestion de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin=True

            #Gestion de teclas para jugador 1
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    j.velx=-5
                    j.vely=0
                if event.key == pygame.K_RIGHT:
                    j.velx=5
                    j.vely=0
                if event.key ==pygame.K_SPACE:
                    j.velx=0
                    j.vely=0

                #Controles jugador 2
                '''if event.key == pygame.K_a:
                        j2.velx=-5
                        j2.vely=0
                if event.key == pygame.K_d:
                        j2.velx=5
                        j2.vely=0
                if event.key == pygame.K_s:
                        j2.velx=0
                        j2.vely=5
                if event.key == pygame.K_w:
                        j2.velx=0
                        j2.vely=-5'''

            #Disparo de balas
            if event.type ==pygame.MOUSEBUTTONDOWN:
                print (j.pos())
                b=Proyectil(j.pos(), ROJO)
                balas.add(b)

        #rivales asesinados por jugador 1
        ls1=pygame.sprite.spritecollide(j,rivales,True)

        ##rivales asesinados por jugador 1
        '''ls2=pygame.sprite.spritecollide(j2,rivales,True)'''

        #Marcador jugador 1
        for e in ls1:
            print ('Marcador jugador 1: ')
            print (marcador1)
            marcador1=marcador1+1

        #Marcador jugador 2
        '''for e in ls2:
            print ('Marcador jugador 2: ')
            print (marcador2)
            marcador2=marcador2+1'''

        #Gestion de balas
        for b in balas:
            #colision de bala con rival
            ls=pygame.sprite.spritecollide(b,rivales,True)
            for e in ls:
                print ('colision')
                balas.remove(b)
            #Control de limite para balas
            if b.rect.y < -10:
                balas.remove(b)

        #Gestion de rivales
        for r in rivales:
            if r.temporizador == 0:
                r.disparar =True

            if r.disparar:
                b=Proyectil(r.pos(), BLANCO)
                b.vely=7
                balasRival.add(b)
                r.disparar=False
                r.temporizador=random.randrange(1000)


        #Gestion de balas rivales
        for b in balasRival:
            ls=pygame.sprite.spritecollide(b,jugadores,True)
            if b.rect.y >ALTO:
                balasRival.remove(b)

        #Gestion de control

        #Gestion de pantalla
        #Actualizar objetos
        balas.update()
        jugadores.update()
        rivales.update()
        balasRival.update()

        pantalla.fill(NEGRO)
        #Dibujar objetos
        jugadores.draw(pantalla)
        rivales.draw(pantalla)
        balas.draw(pantalla)
        balasRival.draw(pantalla)

        pygame.display.flip()
        reloj.tick(60)
