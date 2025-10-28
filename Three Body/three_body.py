import math
from PIL import Image
import numpy as np
from joblib import Parallel, delayed
# import cv2
world_rec = [0,0,2048,2048]
view_rec = [0.0,0.0,2048.0,2048.0]
# view_rec = [384.0,384.0,256.0,256.0]
zoom_speed = 512.0/121




#points = [[100,50,1],[50,100,1],[200,200,1]]
points = list()

def rainbow(i,length = 1):
    green = 0
    if  i <= length/6:
        green  = max(((i)/(length/6)) * 255,0)
    elif i >= length/6 and i <= length/2:
        green = 255
    elif i >= length/2 and i < 2* length/3:
          green = max((((2 * length/3) - i)/(length/6)) * 255,0)
        
    red = 0
    if i < length/6:
        red = 255 #
    elif i >= length/6 and i < length/3:
        red  = max((((length/3) - i)/(length/6)) * 255,0)
    elif i >= 2 * length/3 and i < 5 * length/6:
        red = max(((i - (2 * length/3))/(length/6)) * 255,0)
    elif i >=  5 * length/6:
        red = 255
        
    blue = 0
    if i >= length/3 and i <= length/2:
        blue = max(((i - (length/3))/(length/6)) * 255,0)
    elif i >= length/2 and i <= 5 * length/6:
        blue  = 255
    elif i >= 5 * length/6:
        blue =  max((((length) - i)/(length/6)) * 255,0)

    return[red,green,blue]

def get_n_colors(n):
    colors = [] # 3/4 + 1/8
    for i in range(n):
        colors.append(rainbow(i,n))
    return colors

def get_dist(point1,point2):
   #print((((point2[0]-point1[0])**2) + ((point2[1]-point1[1])**2))**(1/2))
   return (((point2[0]-point1[0])**2) + ((point2[1]-point1[1])**2))**(1/2)

def get_dist_fast(point1,point2):
   return ((point2[0]-point1[0])**2) + ((point2[1]-point1[1])**2)

def get_vel(point,particle,time,big_g):
    force = (big_g * point[2])/(get_dist_fast(point,particle))
    amount = ((force * time))
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
    for y in range(clamp(y1 - size,0,world_rec[2]-1),clamp(y1 + size + 1,0,world_rec[2]-1)):
        for x in range(clamp(x1 - size,0,world_rec[2]-1),clamp(x1 + size + 1,0,world_rec[2]-1)):
            if math.ceil(get_dist([x,y],[x1,y1])) < size:
                for i in range(3):
                    data[y][x][i] = color[i]
        

# colors = [[255,0,0],[0,255,0],[0,0,255]]
pos = [[10.00001,5.00001],[5.0001,10.001],[20.0001,20.00001]]
n = 6
colors = get_n_colors(n)
for i in range(n):
    points.append([np.random.random()*(world_rec[2]-1),np.random.random()*(world_rec[2]-1),10,colors[i]])
# for i in range(3):
#     points.append([pos[i][0],pos[i][1],10,colors[i]])
    

particle = [world_rec[3]/2,world_rec[3]/2,1]
particle_vel = [0,0]
time = 0




time = 0
time_limit = 1000
sim_speed = 40

def get_subrec(world_rec_portion,size,view_rec):
    image_data = np.empty((world_rec_portion[2],world_rec_portion[3],3),dtype=np.uint8)
    image_data.fill(0)  
    margin = size/2
    
    for y in range(world_rec_portion[1],world_rec_portion[1] + world_rec_portion[3]):
        for x in range(world_rec_portion[0],world_rec_portion[0] + world_rec_portion[2]):
            
            x1 = ((x/size) * view_rec[2]) + view_rec[0]
            y1 = ((y/size) * view_rec[3]) + view_rec[1]
            
            particle_vel = [0,0]
            particle[0:2] = [x1,y1]
            min_dist = get_dist_fast(points[0],particle)
            min_point = points[0]
            big_g = 1
            while(True):
                for point in points:
                    new_vel = get_vel(point,particle,sim_speed,big_g)
                    particle_vel[0] += new_vel[0]
                    particle_vel[1] += new_vel[1]
                    dist = get_dist_fast(point,particle)
                    if dist  < min_dist:
                        min_dist = dist 
                        min_point = point
                        
                particle[0] += particle_vel[0]
                particle[1] += particle_vel[1]
                big_g += 0.001
                #outside
                if particle[0] > world_rec[2] + margin or particle[0] < -margin or particle[1] > world_rec[2] + margin or particle[1] < -margin:
                    break
            for i in range(3):
                image_data[y - world_rec_portion[1]][x - world_rec_portion[0]][i] = min_point[3][i]
    return [world_rec_portion,image_data]
            
    

def run_process_pool(num_workers,recs,size,view_rec):
      return Parallel(n_jobs=num_workers)(
        delayed(get_subrec)(recs[i],size,view_rec) for i in range(num_workers)
    )
      


def make_video(runs):
    # video = cv2.VideoWriter("Misc\Three Body\output.avi", cv2.VideoWriter_fourcc(*'DIVX'), 120, (world_rec[2], world_rec[3]))

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
    
    for y in range(world_rec[3]):
        for x in range(world_rec[2]):

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

def make_image_fast(size, viewrec):
    
    # 11 min 1024, 60 workers at mn = 3
    # 11 min 1024, 16 worker at n = 4
    max_workers = 60
    n = 3
    square = 4**n
    recs = list()
    for i in range(square):
        recs.append([(i % (int(square**(1/2)))) * (size//(2**n)),(i // (int(square**(1/2)))) * (size//(2**n)),(size//(2**n)),(size//(2**n))])
    image_data = np.empty((world_rec[2],world_rec[3],3),dtype=np.uint8)
    image_data.fill(0)  
    
    while len(recs) > 0:
        image_data_portions = run_process_pool(min(max_workers,len(recs)),recs,size,viewrec)
        for image_data_portion in image_data_portions:
            rec = image_data_portion[0]
            c_image_data = image_data_portion[1]
            for y in range(rec[1],rec[1] + rec[3]):
                for x in range(rec[0],rec[0] + rec[2]):
                        image_data[y][x] = c_image_data[y - rec[1]][x - rec[0]]
            del recs[recs.index(rec)]
            print(((square - len(recs))/square) * 100)
                       
    
    for point in points:
        draw_point(3,point,[0,0,0],image_data)
        draw_point(2,point,point[3],image_data)

    image = Image.fromarray(image_data)
    image.save("Three Body\output.png")
    image.show()
    print("Done!")   
    
def make_gif_fast(size,view_rec,frame_amount = 40):
    
    frames = list()
    
    # 11 min 1024, 60 workers at mn = 3
    # 11 min 1024, 16 worker at n = 4

    max_workers = 60
    n = 3
    square = 4**n
    
    for f in range(frame_amount):
        recs = list()
        for i in range(square):
            recs.append([(i % (int(square**(1/2)))) * (size//(2**n)),(i // (int(square**(1/2)))) * (size//(2**n)),(size//(2**n)),(size//(2**n))])
        image_data = np.empty((world_rec[2],world_rec[3],3),dtype=np.uint8)
        image_data.fill(0)  
        
        while len(recs) > 0:
            image_data_portions = run_process_pool(min(max_workers,len(recs)),recs,size,view_rec)
            for image_data_portion in image_data_portions:
                rec = image_data_portion[0]
                c_image_data = image_data_portion[1]
                for y in range(rec[1],rec[1] + rec[3]):
                    for x in range(rec[0],rec[0] + rec[2]):
                            image_data[y][x] = c_image_data[y - rec[1]][x - rec[0]]
                del recs[recs.index(rec)]
                # print(((square - len(recs))/square) * 100)
    #   for point in points:
    #   draw_point(3,point,[0,0,0],image_data)
    #   draw_point(2,point,point[3],image_data)
        view_rec = [view_rec[0] + zoom_speed/2,
                    view_rec[1] + zoom_speed/2,
                    view_rec[2] - zoom_speed,
                    view_rec[3] - zoom_speed]
        
      
        print((f * 100)/frame_amount)
        image = Image.fromarray(image_data)
        frames.append(image)
        
    frames[0].save(
    'Three body\output.gif',
    save_all=True,
    append_images=frames[1:],
    duration=50,  # Duration of each frame in milliseconds
    loop=0      # 0 means loop indefinitely
    )      

    print("Done!")   
                
     
# make_video(30) 
# make_image()
make_image_fast(world_rec[2],view_rec)
# make_gif_fast(world_rec[2],view_rec,120)