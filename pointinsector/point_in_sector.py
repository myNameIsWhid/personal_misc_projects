import math
from PIL import Image
import numpy as np

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
        red = 255 
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
        
# print(rainbow(0))


def get_dist(point1,point2):
   return (((point2[0]-point1[0])**2) + ((point2[1]-point1[1])**2))**(1/2)


def to_radian(num):
    if num > 2 * math.pi:
        return num - (2 * math.pi)
    if num <= 0:
        return (2 * math.pi) + num
    return num




def is_point_in_sector(sector,point):
    if get_dist(sector[0],point) > sector[1]: # if not with radius, its not in sector
        return False
    
    if sector[3] >= 2 * math.pi: # if view cone >= 360, then if its within the radius its in the sector
        return True
    
    bound1 = to_radian(sector[2] - sector[3]/2)
    bound2 = to_radian(sector[2] + sector[3]/2)
    point_angle = to_radian(math.atan2(sector[0][1] - point[1],sector[0][0] - point[0]) + math.pi/2)
    
    if bound1 > bound2: # if view cone contains 2Pi or 0, then no comparison can be made and the angles must be adjusted
        point_angle =  to_radian(point_angle + ((2 * math.pi) - bound1))
        bound2 +=  ((2 * math.pi) - bound1)
        bound1 = 0

    if point_angle >= bound1 and point_angle <= bound2:
        return True
    
    return False


sector = [[0.5,0.5],0.5,0,0]
res_rec = [0,0,256,256]
sim_rec = [0.0,0.0,1.0,1.0]
inside_color = [0,0,255]
outside_color = [255,255,255]

frame_count = 240
frames = list()
for f in range(frame_count):
    
    
        
        
        
    inside_color = rainbow(sector[3],2* math.pi)
    # outside_color = rainbow((f + frame_count/2) % frame_count,frame_count)
    
    image_data = np.empty((res_rec[2],res_rec[3],3),dtype=np.uint8)
    image_data.fill(0)  
    sector[2] += (4 * math.pi)/frame_count
    sector[3] = math.sin(((f * 2 * math.pi)/frame_count) - (math.pi/2)) * (math.pi) + math.pi
    sector[2] = to_radian(sector[2])
    print((f/frame_count) * 100)

    for y in range(res_rec[3]):
        for x in range(res_rec[2]):
            x1 = ((x/res_rec[2]) * sim_rec[2]) + sim_rec[0]
            y1 = ((y/res_rec[3]) * sim_rec[3]) + sim_rec[1]
            point = [x1,y1]
            if is_point_in_sector(sector,point):
                for i in range(3):
                    image_data[x][y][i] = inside_color[i]
            else:
                for i in range(3):
                    image_data[x][y][i] = outside_color[i]
                    
    image = Image.fromarray(image_data)
    frames.append(image)
    
frames[0].save(
    'pointinsector\output.gif',
    save_all=True,
    append_images=frames[1:],
    duration=50,  # Duration of each frame in milliseconds
    loop=0      # 0 means loop indefinitely
    )      
# image.save("pointinsector\output.png")
# image.show()
print("Done!")   
            

