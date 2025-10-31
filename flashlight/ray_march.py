from math import pi,atan2,cos,sin,ceil
import numpy as np
from PIL import Image

sector = [[0.5,0.5],0.45,0,pi]
res_rec = [0,0,64,64]
sim_rec = [0.0,0.0,1,1]
obstacles = [[[0.2,0.2],[0.2,0.8]]]

def clamp(num,min,max):
    if num < min:
        return min
    if num > max:
        return max
    return num

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

def get_dist_squared(point1,point2):
   return ((point2[0]-point1[0])**2) + ((point2[1]-point1[1])**2)


def to_radian(num):
    if num > 2 * pi:
        return num - (2 * pi)
    if num <= 0:
        return (2 * pi) + num
    return num

def quadrant(angle):
    angle = to_radian(angle)
    if angle >= 0 and angle < pi/2:
        return 1
    if angle >= pi/2 and angle < pi:
        return 2
    if angle >= pi and angle < 3 * pi/2:
        return 3
    if angle >=  3 * pi/2 and angle <= 2 * pi:
        return 4

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
        
    res = 80#int(res_rec[3] * 180/512)

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
                if get_dist_squared(point_on_line,[x1,y1]) <= width**2:
                    for j in range(3):
                        image_data[x][y][j] = color[j]
                    break
    
def draw_sector(sector,image_data,res_rec,sim_rec,inside_color):
    theta1 = to_radian(sector[2] + sector[3]/2) + pi/2
    theta2 = to_radian(sector[2] - sector[3]/2) + pi/2
    theat2_point = [cos(theta2) * sector[1] + sector[0][0],sin(theta2) * sector[1] + sector[0][1]]
    theat1_point = [cos(theta1) * sector[1] + sector[0][0],sin(theta1)  * sector[1] + sector[0][1]]
    # theta1 += pi/2
    # theta2 += pi/2

    if quadrant(theta1) == 1:
        if quadrant(theta2) == 1:
            x_bounds = [sector[0][0],theat2_point[0]]
            y_bounds = [theat1_point[1],sector[0][1]]
            print("11")
        elif quadrant(theta2) == 2:
            x_bounds = [sector[0][0] - sector[1],sector[0][0] + sector[1]]
            y_bounds = [sector[0][1] - sector[1],max(theat1_point[1],theat2_point[1])]
        elif quadrant(theta2) == 3:
            x_bounds = [theat2_point[0],sector[0][0] + sector[1]]
            y_bounds = [sector[0][1] - sector[1],theat1_point[1]]
        elif quadrant(theta2) == 4:
            x_bounds = [sector[0][0],sector[0][0] + sector[1]]
            y_bounds = [theat2_point[1],theat1_point[1]]
             #43
    elif quadrant(theta1) == 2:
        if quadrant(theta2) == 1:
            x_bounds = [theat1_point[0],theat2_point[0]]
            y_bounds = [sector[0][1],sector[0][1] + sector[1]] #14
        elif quadrant(theta2) == 2:
            x_bounds = [theat1_point[0],sector[0][0]]
            y_bounds = [theat2_point[1],sector[0][1]]
            print("22")
        elif quadrant(theta2) == 3:
            x_bounds = [min(theat2_point[0],theat1_point[0]),sector[0][0] + sector[1]]
            y_bounds = [sector[0][1] - sector[1],sector[0][1] + sector[1]]
        elif quadrant(theta2) == 4:
            x_bounds = [theat1_point[0],sector[0][0] + sector[1]]
            y_bounds = [theat2_point[1],sector[0][1] + sector[1]]
    elif quadrant(theta1) == 3:
        if quadrant(theta2) == 1:
            x_bounds = [sector[0][0] - sector[1],theat2_point[0]]
            y_bounds = [theat1_point[1],sector[0][1] + sector[1]]
        elif quadrant(theta2) == 2:
            x_bounds = [sector[0][0] - sector[1],sector[0][0]]
            y_bounds = [theat1_point[1],theat2_point[1]]
          # 21
        elif quadrant(theta2) == 3:
            x_bounds = [theat2_point[0],sector[0][0]]
            y_bounds = [sector[0][0],theat1_point[1]]
            print("33")
        elif quadrant(theta2) == 4:
            x_bounds = [sector[0][0] - sector[1],sector[0][0] + sector[1]]
            y_bounds = [min(theat1_point[1],theat2_point[1]),sector[0][1] + sector[1]]
            
    elif quadrant(theta1) == 4:
         if quadrant(theta2) == 1:
            x_bounds = [sector[0][0] - sector[1],max(theat1_point[0],theat2_point[0])]
            y_bounds = [sector[0][1] - sector[1],sector[0][1] + sector[1]]
         elif quadrant(theta2) == 2:
            x_bounds = [sector[0][0] - sector[1],theat1_point[0]]
            y_bounds = [sector[0][1] - sector[1],theat2_point[1]]
         elif quadrant(theta2) == 3:
            x_bounds = [theat2_point[0],theat1_point[0]]
            y_bounds = [sector[0][1] - sector[1],sector[0][1],sector[0][1]]
             # 32
         elif quadrant(theta2) == 4:
            x_bounds = [sector[0][0],theat1_point[0]]
            y_bounds = [sector[0][1],theat2_point[1]]

            
            
            
            
        

    
    
    
    # x_bounds = [sector[0][0] - sector[1],sector[0][0] + sector[1]]
    # y_bounds = [sector[0][1] - sector[1],sector[0][1] + sector[1]]
    
    # draw_line([[x_bounds[0],y_bounds[0]],[x_bounds[1],y_bounds[1]]],image_data,res_rec,sim_rec,[125,125,125])
     
    # print(int(clamp((y_bounds[0]/sim_rec[3]) * res_rec[3],0,res_rec[3] - 1)))
    
    
    y1 = int(clamp(((y_bounds[0])/sim_rec[2]) * res_rec[2],0,res_rec[2] - 1))
    y2 = int(clamp(((y_bounds[1])/sim_rec[2]) * res_rec[2],0,res_rec[2]))
    x1 = int(clamp(((x_bounds[0])/sim_rec[2]) * res_rec[2],0,res_rec[2] - 1))
    x2 = int(clamp(((x_bounds[1])/sim_rec[2]) * res_rec[2],0,res_rec[2]))
    # print(sector[0][0],x1)
    color1 = rainbow(quadrant(theta1) - 1,4)
    color2 = rainbow(quadrant(theta2) - 1,4)

    draw_line([[x_bounds[0],y_bounds[0]],[x_bounds[1],y_bounds[0]]],image_data,res_rec,sim_rec,color1)
    draw_line([[x_bounds[1],y_bounds[0]],[x_bounds[1],y_bounds[1]]],image_data,res_rec,sim_rec,color2)
    draw_line([[x_bounds[1],y_bounds[1]],[x_bounds[0],y_bounds[1]]],image_data,res_rec,sim_rec,color2)
    draw_line([[x_bounds[0],y_bounds[1]],[x_bounds[0],y_bounds[0]]],image_data,res_rec,sim_rec,color1)
    
    
    # x1 = int(clamp(((sector[0][0] - sector[1])/sim_rec[2]) * res_rec[2],0,res_rec[2] - 1))
    # x2 = int(clamp(((sector[0][0] + sector[1])/sim_rec[2]) * res_rec[2],0,res_rec[2]))
    # y1 = int(clamp(((sector[0][1] - sector[1])/sim_rec[2]) * res_rec[2],0,res_rec[2] - 1))
    # y2 = int(clamp(((sector[0][1] + sector[1])/sim_rec[2]) * res_rec[2],0,res_rec[2]))
    
    # print("x1",x1)
    # print("x2",x2)
    
    # print("y1",y1)
    # print("y2",y2)
    
    for y in range(y1,y2):
        for x in range(x1,x2):
            
            point_x = ((x/res_rec[2]) * sim_rec[2]) + sim_rec[0]
            point_y = ((y/res_rec[3]) * sim_rec[3]) + sim_rec[1]
            point = [point_x,point_y]
            if is_point_in_sector(sector,point):
                for i in range(3):
                    image_data[x][y][i] = inside_color[i]
            # else:
            #     for i in range(3):
            #         image_data[x][y][i] = outside_color[i]
     
    theta1 = to_radian(sector[2] + sector[3]/2)  + pi/2
    theta2 = to_radian(sector[2] - sector[3]/2) + pi/2
    theat2_point = [cos(theta2 ) * sector[1] + sector[0][0],sin(theta2) * sector[1] + sector[0][1]]
    theat1_point = [cos(theta1) * sector[1] + sector[0][0],sin(theta1)  * sector[1] + sector[0][1]]
           
    draw_line([[sector[0][0],sector[0][1]],[theat1_point[0],theat1_point[1]]],image_data,res_rec,sim_rec,[255,0,0])
    draw_line([[sector[0][0],sector[0][1]],[theat2_point[0],theat2_point[1]]],image_data,res_rec,sim_rec,[0,0,255])

def make_gif(sector,res_rec,sim_rec,frame_count):
    inside_color = [255,255,255]
    # outside_color =  [0,0,0]
    
    frames = list()
    for f in range(frame_count):

        image_data = np.empty((res_rec[2],res_rec[3],3),dtype=np.uint8)
        image_data.fill(0)  
        sector[2] += (2 * pi)/frame_count
        sector[2] = to_radian(sector[2])
        sector[3] = sin(((f * 2 * pi)/frame_count) - (pi/2)) * (pi/2) + (pi)
        print((f/frame_count) * 100)

        draw_sector(sector,image_data,res_rec,sim_rec,inside_color)
                        
        # lines = approx_sector_with_lines(sector,int(sector[3]//(2*pi/35) + 1))      
        # colors  = get_n_colors(int(sector[3]//(2*pi/35) + 3))      
        # for i,line in enumerate(lines):
        #     draw_line(line,image_data,res_rec,sim_rec,colors[i],4)
        
        # theta1 = to_radian(sector[2] + sector[3]/2) + pi/2
        # theta2 = to_radian(sector[2] - sector[3]/2) + pi/2
        # theat1_point = [cos(theta1) * sector[1] + sector[0][0],sin(theta1) * sector[1] + sector[0][1]]
        # theat2_point = [cos(theta2) * sector[1] + sector[0][0],sin(theta2) * sector[1] + sector[0][1]]
        
        # color = rainbow(quadrant(theta1 - pi/2) - 1,4)
        # #red 1
        # #green 2
        # # cyan 3
        # # purple 4
        
        # draw_line([[sector[0][0],sector[0][1]],[theat1_point[0],theat1_point[1]]],image_data,res_rec,sim_rec,color)
        # color = rainbow(quadrant(theta2 - pi/2) - 1,4)
        # draw_line([[sector[0][0],sector[0][1]],[theat2_point[0],theat2_point[1]]],image_data,res_rec,sim_rec,color)
        
        
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
    lines = approx_sector_with_lines(sector,max(int(sector[3]//(2*pi/11) + 1),3))
    for obstacle in obstacles:
        for line in lines:
            if intersect(line,obstacle):
                return True
    return False

def bifurcate_sectors(sectors):
    bifurcated = []
    for sector in sectors:
        bifurcated.append([sector[0],sector[1],to_radian(sector[2] + sector[3]/4),sector[3]/2,sector[4] - 1])
        bifurcated.append([sector[0],sector[1],to_radian(sector[2] - sector[3]/4),sector[3]/2,sector[4] - 1])
    return bifurcated
        

def get_rays(point,angle,viewcone,sim_rec):
    split_limit = 7
    sectors = [[point,0,angle,viewcone,split_limit]]
    tolerance = 0.0001

    split_amount = 1
    
    rays = []
    
    while len(sectors) != 0:
        new_sectors = []
        for sector in sectors:
            march_amount = min(sim_rec[3],sim_rec[2])
            
            if sector[4] == 0:
                rays.append(sector)
                continue

            while True:
                
                if sector[1] > max(sim_rec[3],sim_rec[2]) * 2:
                    sector[1] = max(sim_rec[3],sim_rec[2])
                    rays.append(sector)
                    break
                
                if march_amount <= tolerance:
                    # for i in range(split_amount):
                    initial_split = bifurcate_sectors([sector])
                    bifurcated_sectors = [initial_split[0],initial_split[1]]
                    
                    for _ in range(split_amount - 1):
                        n_bifurcated_sectors = []
                        for bisector in bifurcate_sectors(bifurcated_sectors):
                            n_bifurcated_sectors.append(bisector)
                        bifurcated_sectors = n_bifurcated_sectors
                        
                    for bisector in bifurcated_sectors:
                        new_sectors.append(bisector)
                    break

                if not does_sector_intersect_obstacles(sector):
                    sector[1] += march_amount
                else:
                    sector[1] -= march_amount
                    march_amount = march_amount/2 # quick half
                    
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
        # print("getting rays")
        sectors = get_rays(sector[0],sector[2],sector[3],sim_rec)
        # print("drawng sectors")
        colors = get_n_colors(len(sectors))
        for i,sector_1 in enumerate(sectors):
            draw_sector(sector_1,image_data,res_rec,sim_rec,rainbow(sector_1[4],5))
        # print("drawng lines")
        
        
        # for i,sector_1 in enumerate(sectors):
        #     lines = approx_sector_with_lines(sector_1,3)
        #     for line in lines:
        #         draw_line(line,image_data,res_rec,sim_rec,[255,255,255],0.5)
        
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





# make_light_gif(sector,res_rec,sim_rec,120)
    
def test_gif(sector,res_rec,sim_rec):
    inside_color = [0,0,0]
    # outside_color =  [0,0,0]
    
    frames = list()
    x1 = int(clamp(((sector[0][0] - sector[1])/sim_rec[2]) * res_rec[2],0,res_rec[2] - 1))
    x2 = int(clamp(((sector[0][0] + sector[1])/sim_rec[2]) * res_rec[2],0,res_rec[2]))
    y1 = int(clamp(((sector[0][1] - sector[1])/sim_rec[2]) * res_rec[2],0,res_rec[2] - 1))
    y2 = int(clamp(((sector[0][1] + sector[1])/sim_rec[2]) * res_rec[2],0,res_rec[2]))
    
    # print("x1",x1)
    # print("x2",x2)
    
    # print("y1",y1)
    # print("y2",y2)
    
    image_data = np.empty((res_rec[2],res_rec[3],3),dtype=np.uint8)
    image_data.fill(255)  
    
    for y in range(y1,y2):
        for x in range(x1,x2):
            
            point_x = ((x/res_rec[2]) * sim_rec[2]) + sim_rec[0]
            point_y = ((y/res_rec[3]) * sim_rec[3]) + sim_rec[1]
            point = [point_x,point_y]
            if is_point_in_sector(sector,point):
                for i in range(3):
                    image_data[x][y][i] = inside_color[i]
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



# test_gif(sector,res_rec,sim_rec)
make_gif(sector,res_rec,sim_rec,120)