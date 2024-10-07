from math import *
from tkinter import *
import keyboard

root=Tk()
root.title("Metal 2 edges controlled, 1 edge convection, 1 edge direct diff-conv solution")
root.geometry("1920x1080")
graph=Canvas(root,width=300,height=200,bg="black")
graph.pack(fill="both",expand=True)

def convert(coords,obs,theta):
    x,y,z=coords[0],coords[1],coords[2]

    if switch==-1:
        x,y=y,x
    
    x,z,y=-x,y,z
    obsx,obsy,obsz=obs[0],obs[1],obs[2]

    xr=x-obsx
    yr=y-obsy
    zr=z-obsz
    
    dyz=((yr)**2+(zr)**2)**.5
    dxz=((xr)**2+(zr)**2)**.5

    xp,yp=500,500
    
    if dyz>0:
        xp=1920*(xr/(2*dyz)*tan(theta)+.5) #magic
    if dxz>0: 
        yp=1080*(yr/(2*dxz)*tan(theta)+.5)

    #if abs(xp)>1920 or abs(yp)>1080:
        #xp,yp=0,0
        
    a=[xp,yp]
    return a

T=[]
Tn=[]
Tw=[]
Twn=[]
nx=30
ny=15
for i in range(nx):
    add=[]
    for j in range(ny):
        if i==0:
            add.append([i,j,-20])
        elif i==nx-1:
            add.append([i,j,20])
        else:
            add.append([i,j,0])
    T.append(add)
    Tn.append(add)
    Tw.append(0)
    Twn.append(0)


dt=.1
ds=1
Tinf=-10
Twl=2
Twr=3
alp=.5
alpw=.5
k=.5
h=.9
v=3

obs=[0,0,-80]
theta=120*pi/180
speed=.9
waterspeed=1
oval=5
global switch
switch=1
cont=1

while cont==1:
    Tw[0]=Twl
    Tw[len(Tw)-1]=Twr
    for i in range(1,nx-1):
        grad=(Tw[i]-Tw[i-1])/(1*ds)
        lap=(Tw[i+1]+Tw[i-1]-2*Tw[i])/(ds**2)
        Twn[i]+=(alpw*lap-v*grad)*dt
        for j in range(ny):
            if j==0:
                lap=(T[i-1][j][2]+T[i+1][j][2]+T[i][j+1][2]-3*T[i][j][2])/(ds**2)
                Tn[i][0][2]=Twn[i]#+=(alp*lap+h * (Tw[i] - T[i][0][2]))*dt #optional convection to water

            elif j==ny-1:
                lap=(T[i-1][j][2]+T[i+1][j][2]+T[i][j-1][2]-3*T[i][j][2])/(ds**2)
                Tn[i][ny-1][2]+=(alp*lap+h * (Tinf - T[i][ny-1][2]))*dt
                
            else:
                lap=(T[i-1][j][2]+T[i+1][j][2]+T[i][j-1][2]+T[i][j+1][2]-4*T[i][j][2])/(ds**2)
                Tn[i][j][2]+=alp*lap*dt
                
    for i in range(1,nx-1):
        Tw[i]=Twn[i]
        for j in range(ny):
            T[i][j][2]=Tn[i][j][2]

    for i in range(nx):
        for j in range(ny):
            xp,yp=convert([T[i][j][0],T[i][j][1],T[i][j][2]],obs,theta)
            graph.create_oval(xp-oval,yp-oval,xp+oval,yp+oval,fill="green")
    for i in range(nx-1):
        for j in range(ny-1):
            xp,yp=convert([T[i][j][0],T[i][j][1],T[i][j][2]],obs,theta)
            xp2,yp2=convert([T[i+1][j][0],T[i+1][j][1],T[i+1][j][2]],obs,theta)
            xp3,yp3=convert([T[i][j+1][0],T[i][j+1][1],T[i][j+1][2]],obs,theta)
            graph.create_line(xp,yp,xp2,yp2,fill="blue",width=2)
            graph.create_line(xp,yp,xp3,yp3,fill="red",width=2)
    for i in range(ny-1):
        xp,yp=convert([T[nx-1][i][0],T[nx-1][i][1],T[nx-1][i][2]],obs,theta)
        xp2,yp2=convert([T[nx-1][i+1][0],T[nx-1][i+1][1],T[nx-1][i+1][2]],obs,theta)
        graph.create_line(xp,yp,xp2,yp2,fill="red",width=2)
    for i in range(nx-1):
        xp,yp=convert([T[i][ny-1][0],T[i][ny-1][1],T[i][ny-1][2]],obs,theta)
        xp2,yp2=convert([T[i+1][ny-1][0],T[i+1][ny-1][1],T[i+1][ny-1][2]],obs,theta)
        graph.create_line(xp,yp,xp2,yp2,fill="blue",width=2)

    for i in range(nx-1):
        xp,yp=convert([T[i][0][0],T[i][0][1]-1,Tw[i]],obs,theta)
        xp2,yp2=convert([T[i+1][0][0],T[i+1][0][1]-1,Tw[i+1]],obs,theta)
        graph.create_line(xp,yp,xp2,yp2,fill="cyan",width=2)
        #graph.create_oval(xp-oval,yp-oval,xp+oval,yp+oval,fill="purple")

    if keyboard.is_pressed("up arrow"):
        obs[1]+=speed
    if keyboard.is_pressed("down arrow"):
        obs[1]-=speed
    if keyboard.is_pressed("left arrow"):
        obs[0]+=speed
    if keyboard.is_pressed("right arrow"):
        obs[0]-=speed
    if keyboard.is_pressed("w"):
        obs[2]+=speed
    if keyboard.is_pressed("s"):
        obs[2]-=speed
    if keyboard.is_pressed("o"):
        switch*=-1
    if keyboard.is_pressed("i"):
        Twl+=waterspeed
    if keyboard.is_pressed("k"):
        Twl-=waterspeed
    if keyboard.is_pressed("u"):
        Twr+=waterspeed
    if keyboard.is_pressed("j"):
        Twr-=waterspeed

    graph.create_text(360,20,text="Metal: 1 edge is convection to the air, 1 edge equals the water temp, the other 2 edges are held at constants",fill="dark red", font=("Helvetica 10 bold"))
    graph.create_text(360,40,text="Metal PDE: 2-D heat equation (Fourier's law); Water PDE: 1-D Convection-diffusion equation (upwind scheme)",fill="dark red", font=("Helvetica 10 bold"))
    graph.create_text(270,60,text="Controls--- Fly: w,s,arrows;  Water: i,k,u,j;  Flip axes: press o quickly; Quit: q",fill="dark red", font=("Helvetica 10 bold"))

    root.update()
    graph.delete("all")

    if keyboard.is_pressed("q"):
        cont=0
        root.destroy()








              
