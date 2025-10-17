import math
from PIL import Image
import numpy as np
import cv2
world_rec = [0,0,256,256]



#points = [[100,50,1],[50,100,1],[200,200,1]]
points = list()


def get_dist(point1,point2):
   #print((((point2[0]-point1[0])**2) + ((point2[1]-point1[1])**2))**(1/2))
   return (((point2[0]-point1[0])**2) + ((point2[1]-point1[1])**2))**(1/2)

def get_vel(point,particle,time,big_g):
    force = (big_g * particle[2] * point[2])/(get_dist(point,particle)**2)
    amount = ((force * time) / particle[2])
    angle = math.atan2(particle[1] - point[1],particle[0] - point[0])
    vel =  [amount * -math.cos(angle),amount * -math.sin(angle)]
    return vel

def clamp(num,min,max):
    if num < min:
        return min
    if num > max:
        return max
    return num

def draw_point(size,point,color,data):
    x1 = clamp(int(point[0]),0,world_rec[2]-1)
    y1 = clamp(int(point[1]),0,world_rec[2]-1)
    for y in range(clamp(y1 - size,0,world_rec[2]-1),clamp(y1 + size,0,world_rec[2]-1)):
        for x in range(clamp(x1 - size,0,world_rec[2]-1),clamp(x1 + size,0,world_rec[2]-1)):
            if get_dist([x,y],[x1,y1]) < size:
                for i in range(3):
                    data[y][x][i] = color[i]
        

for i in range(3):
    points.append([np.random.random()*(world_rec[2]-1),np.random.random()*(world_rec[2]-1),10,[255 if i == 0 else 0,255 if i == 1 else 0,255 if i == 2 else 0]])
    
    

particle = [world_rec[3]/2,world_rec[3]/2,1]
particle_vel = [0,0]
time = 0
size = 3



time = 0
time_limit = 1000
sim_speed = 23
min_dist = 6

def make_video(runs):
    video = cv2.VideoWriter("Misc\Three Body\output.avi", cv2.VideoWriter_fourcc(*'DIVX'), 120, (world_rec[2], world_rec[3]))

    margin = 512
    
    for i in range(runs):
        time = 0
        big_g = 1
        particle = [np.random.random()*(world_rec[2]-1),np.random.random()*(world_rec[2]-1),1]
        particle_vel = [0,0]
        while(True):
            frame_data = np.empty((world_rec[2],world_rec[3],3),dtype=np.uint8)
            frame_data.fill(0)  
            
            for point in points:
                new_vel = get_vel(point,particle,sim_speed,big_g)
                particle_vel[0] += new_vel[0]
                particle_vel[1] += new_vel[1]
                
                draw_point(5,point,point[3],frame_data)
                    
            particle[0] += particle_vel[0]
            particle[1] += particle_vel[1]

            
            draw_point(2,particle,[255,255,255],frame_data)
                
            video.write(frame_data)
            time += 1
            #big_g += 100/time_limit
            if particle[0] > world_rec[2] + margin  or particle[0] < -margin  or particle[1] > world_rec[2] + margin  or particle[1] < -margin :
                    break
        print(i)
    video.release()
    print("Done!")

def make_image():
    image_data = np.empty((world_rec[2],world_rec[3],3),dtype=np.uint8)
    image_data.fill(0)  
    margin = 512
    
    for y in range(world_rec[2]):
        for x in range(world_rec[3]):

            particle_vel = [0,0]
            particle[0:2] = [x,y]
            time = 0
            big_g = 0
            min_dist = get_dist(points[0],particle)
            min_point = points[0]
            
            while(True):
                for point in points:
                    new_vel = get_vel(point,particle,sim_speed,big_g)
                    particle_vel[0] += new_vel[0]
                    particle_vel[1] += new_vel[1]
                    if get_dist(point,particle) < min_dist:
                        min_dist = get_dist(point,particle)
                        min_point = point
                        
                particle[0] += particle_vel[0]
                particle[1] += particle_vel[1]
                time += 1
                big_g += 10/time_limit
                #outside
                if particle[0] > world_rec[2] + margin or particle[0] < -margin or particle[1] > world_rec[2] + margin or particle[1] < -margin:
                    break
                print(((x + y * world_rec[2]) * 100)/world_rec[2]**2)
            
            for i in range(3):
                image_data[y][x][i] = min_point[3][i]
            
            
    for point in points:
        draw_point(5,point,[0,0,0],image_data)
        draw_point(4,point,point[3],image_data)
    
    image = Image.fromarray(image_data)
    image.save("Misc\Three Body\output.png")
    image.show()
    print("Done!")   

make_video(30) 
make_image()