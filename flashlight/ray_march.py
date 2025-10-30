from math import pi,atan2,cos,sin,ceil
import numpy as np
from PIL import Image

sector = [[0.5,0.5],0.45,0,pi/2]
res_rec = [0,0,512,512]
sim_rec = [0.0,0.0,1,1]
obstacles = [[[0.2,0.2],[0.2,0.8]]]

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
   return (((point2[0]-point1[0])**2) + ((point2[1]-point1[1])**2))**(1/2)


def to_radian(num):
    if num > 2 * pi:
        return num - (2 * pi)
    if num <= 0:
        return (2 * pi) + num
    return num

# center, radius angle, viewcone


def is_point_in_sector(sector,point):
    if get_dist(sector[0],point) > sector[1]: # if not within radius, its not in sector
        return False
    
    if sector[3] >= 2 * pi: # if view cone >= 360, and its within the radius, then its in the sector
        return True
    
    bound1 = to_radian(sector[2] - sector[3]/2)
    bound2 = to_radian(sector[2] + sector[3]/2)
    point_angle = to_radian(atan2(sector[0][1] - point[1],sector[0][0] - point[0]) + pi/2)
    
    if bound1 > bound2: # if view cone contains 2Pi or 0, then no comparison can be made and the angles must be adjusted
        point_angle =  to_radian(point_angle + ((2 * pi) - bound1))
        bound2 +=  ((2 * pi) - bound1)
        bound1 = 0

    if point_angle >= bound1 and point_angle <= bound2:
        return True
    
    return False


# do lines intercet

def is_counterclockwise(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

# Return true if line segments AB and CD intersect
def intersect(line1,line2):
    A = line1[0]
    B = line1[1]
    C = line2[0]
    D = line2[1]
    return is_counterclockwise(A,C,D) != is_counterclockwise(B,C,D) and is_counterclockwise(A,B,C) != is_counterclockwise(A,B,D)

def approx_sector_with_lines(sector,res):
    start = sector[2] - sector[3]/2 + pi/2 # + pi/2 to start a 0
    lines = []
    
    point2 = [sector[0][0] + (cos(start) * sector[1]),sector[0][1] + (sin(start) * sector[1])]
    lines.append([sector[0],point2]) # starting line to center
        
    for i in range(res):
        point_angle = start + ((i / res) * sector[3])
        point1 = [sector[0][0] + (cos(point_angle) * sector[1]),sector[0][1] + (sin(point_angle) * sector[1])]
        
        point_angle = start + (((i + 1) / res) * sector[3])
        point2 = [sector[0][0] + (cos(point_angle) * sector[1]),sector[0][1] + (sin(point_angle) * sector[1])]
        
        lines.append([point1,point2])
        
    lines.append([point2,sector[0]]) # ending line to center
    return lines

def draw_line(line,image_data,res_rec,sim_rec,color,width = 1):
    width = width/res_rec[3]
    min = [0,0]
    max = [0,0]
    if line[0][0] > line[1][0]:
        max[0] = line[0][0]
        min[0] = line[1][0]
    else:
        max[0] = line[1][0]
        min[0] = line[0][0]
        
    if line[0][1] > line[1][1]:
        max[1] = line[0][1]
        min[1] = line[1][1]
    else:
        max[1] = line[1][1]
        min[1] = line[0][1]
        
    res = 40

    angle = atan2(line[1][1] - line[0][1],line[1][0] - line[0][0]) 
    dist = get_dist(max,min)
      
    for y in range(int((min[1]/sim_rec[3]) * res_rec[3] - (width * res_rec[3])),int((max[1]/sim_rec[3]) * res_rec[3] + (width * res_rec[3]))):
        if y < 0:
            continue
        if y >=res_rec[3]:
            break
        for x in range(int((min[0]/sim_rec[2]) * res_rec[2] - (width * res_rec[3])),int((max[0]/sim_rec[2]) * res_rec[2] + (width * res_rec[3]))):
            if x < 0:
                continue
            if x >= res_rec[2]:
                break
            x1 = ((x/res_rec[2]) * sim_rec[2]) + sim_rec[0]
            y1 = ((y/res_rec[3]) * sim_rec[3]) + sim_rec[1]
            
            for i in range(res):
                point_on_line = [line[0][0]+ ((cos(angle) * dist) * (i/res)),line[0][1] + ((sin(angle) * dist) * (i/res))]
                if get_dist(point_on_line,[x1,y1]) <= width:
                    for j in range(3):
                        image_data[x][y][j] = color[j]
                    break
    
def draw_sector(sector,image_data,res_rec,sim_rec,inside_color,outside_color = [0,0,0]):
     for y in range(res_rec[3]):
        for x in range(res_rec[2]):
            x1 = ((x/res_rec[2]) * sim_rec[2]) + sim_rec[0]
            y1 = ((y/res_rec[3]) * sim_rec[3]) + sim_rec[1]
            point = [x1,y1]
            if is_point_in_sector(sector,point):
                for i in range(3):
                    image_data[x][y][i] = inside_color[i]
            # else:
            #     for i in range(3):
            #         image_data[x][y][i] = outside_color[i]

def make_gif(sector,res_rec,sim_rec,frame_count):
    inside_color = [255,255,255]
    outside_color =  [0,0,0]
    
    frames = list()
    for f in range(frame_count):

        image_data = np.empty((res_rec[2],res_rec[3],3),dtype=np.uint8)
        image_data.fill(0)  
        sector[2] += (4 * pi)/frame_count
        sector[2] = to_radian(sector[2])
        sector[3] = sin(((f * 2 * pi)/frame_count) - (pi/2)) * (pi) + pi
        print((f/frame_count) * 100)

        draw_sector(sector,image_data,res_rec,sim_rec,inside_color,outside_color)
                        
        lines = approx_sector_with_lines(sector,int(sector[3]//(2*pi/35) + 1))      
        colors  = get_n_colors(int(sector[3]//(2*pi/35) + 3))      
        for i,line in enumerate(lines):
            draw_line(line,image_data,res_rec,sim_rec,colors[i],4)
            
        image = Image.fromarray(image_data)
        frames.append(image)
        
    frames[0].save(
        'flashlight\output.gif',
        save_all=True,
        append_images=frames[1:],
        duration=50,  # Duration of each frame in milliseconds
        loop=0      # 0 means loop indefinitely
        )      
    print("Done!")  
    
def does_sector_intersect_obstacles(sector):
    lines = approx_sector_with_lines(sector,int(sector[3]//(2*pi/11) + 1))
    for obstacle in obstacles:
        for line in lines:
            if intersect(line,obstacle):
                return True
    return False



def get_rays(point,angle,viewcone,sim_rec):
    split_limit = 5
    sectors = [[point,0,angle,viewcone,split_limit]]
    tolerance = sim_rec[3]/1000

    split_amount = 2
    
    rays = []
    
    while len(sectors) != 0:
        new_sectors = []
        for sector in sectors:
            march_amount = 0.0001
            
            if sector[4] == 0:
                rays.append(sector)
                continue

            while True:
                if sector[1] > max(sim_rec[3],sim_rec[2]):
                    rays.append(sector)
                    break
                
                if march_amount <= tolerance:
                    # for i in range(split_amount):
                    new_sectors.append([point,sector[1],to_radian(sector[2] + sector[3]/4),sector[3]/2,sector[4] - 1])
                    new_sectors.append([point,sector[1],to_radian(sector[2] - sector[3]/4),sector[3]/2,sector[4] - 1])
                    break

                if not does_sector_intersect_obstacles(sector):
                    sector[1] += march_amount
                else:
                    sector[1] -= march_amount
                    march_amount /= 2 # quick half
                    
        sectors = new_sectors
    return rays
    
def make_light_gif(sector,res_rec,sim_rec,frame_count):
    inside_color = [255,255,255]
    
    frames = list()
    for f in range(frame_count):

        image_data = np.empty((res_rec[2],res_rec[3],3),dtype=np.uint8)
        image_data.fill(0)  
        sector[2] += (2 * pi)/frame_count
        sector[2] = to_radian(sector[2])
        # sector[3] = sin(((f * 2 * pi)/frame_count) - (pi/2)) * (pi) + pi
        print((f/frame_count) * 100)
        
        sectors = get_rays(sector[0],sector[2],sector[3],sim_rec)
        colors = get_n_colors(len(sectors))
        for i,sector_1 in enumerate(sectors):
            draw_sector(sector_1,image_data,res_rec,sim_rec,colors[i])
            
        image = Image.fromarray(image_data)
        frames.append(image)
        
    frames[0].save(
        'flashlight\output.gif',
        save_all=True,
        append_images=frames[1:],
        duration=50,  # Duration of each frame in milliseconds
        loop=0      # 0 means loop indefinitely
        )      
    print("Done!")  
            
            
                
        
    
    
    
    
# center, radius angle, viewcone

# ^^^ must be same ratio



chloe = np.asarray(Image.open("flashlight/chloe_512.png"))

    
make_light_gif(sector,res_rec,sim_rec,60)
    


