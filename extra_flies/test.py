import socket
import pygame as pg

def Main():
    host = '10.119.228.157'
    port = 5000


    pg.init()
    display_screen = pg.display.set_mode((1900, 1000))



    clock = pg.time.Clock()

    s = socket.socket()
    s.connect((host,port))
    filename =  "PATH_TO_PIC"
    isExit = False
    while not isExit:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                isExit = True
        data = s.recv(1024)
        print (data)
        filesize = data

        f = open(filename, 'wb')
        data = s.recv(1024)
        totalRecv  =  len(data)
        f.write(data)
        while totalRecv < filesize:
            data = s.recv(1024)
            totalRecv += len(data)
            f.write(data)
        showImg = pg.image.load('PATH_TO_PIC')
        display_screen.blit(showImg, (0,0))
        pg.display.flip()
        clock.tick(60)
    s.close()

if __name__ == '__main__':
    Main()