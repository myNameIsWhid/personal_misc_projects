import math
from PIL import Image
import numpy as np
import cv2




def quad(start,size,starting_point,order,map):
    h_size = size//2
    size_2 = int(size**2)
    
    squares = list()
    squares.append(0 + start)    
    squares.append((size_2//4) + start)  
    squares.append((size_2//2) + start)  
    squares.append(((3 * size_2)//4) + start)  
    
    
   
    new_squares = list()
    for i in range(4):
        new_squares.append(0)
    for j in range(4):
        new_squares[order[j]] = squares[j]
        
    squares = new_squares

    starting_points = [[starting_point[0],starting_point[1] + h_size],starting_point,[starting_point[0] +  h_size,starting_point[1]],[starting_point[0] + h_size,starting_point[1] + h_size]]

    
    if size != 2:
        for i,o in enumerate(order):   
            quarter = squares[i]
            if o == 0:
                quad(quarter,size/2,starting_points[i],list(reversed(order[1:] + order[:1])),map)
            elif o == 3:
                quad(quarter,size/2,starting_points[i],list(reversed(order[3:] + order[:3])),map)
            else:
                quad(quarter,size/2,starting_points[i],order,map)
    else:
        for i,o in enumerate(order):   
            map[int(squares[i])] = starting_points[i]
          
          
size = 1024


map = list()
for i in range(size * size):
    map.append(0)



# print("1-",[order[0]] + list(reversed(order[1:4]))) #0 3 2 1
# print("2-",list(reversed(order[0:3])) + [order[3]])# 2 1 0 3

quad(0,size,[0,0],[0,1,2,3],map)


#print(map)

image_data = np.empty((size * 3,size * 3,3),dtype=np.uint8)
image_data.fill(0)  


            
frames = list()
video = cv2.VideoWriter("Hilbert\output.avi", cv2.VideoWriter_fourcc(*'DIVX'), 120, (size * 3, size * 3))

for i in range((size**2)):
    x = int(map[i][0])
    y = int(map[i][1])
    image_data[(y * 3)][(x * 3)] = [255 * (i/size**2),0,255 * (((size**2)-i)/size**2)]
    frames.append(Image.fromarray(image_data))
    video.write(image_data)
    if i < (size**2) - 1:
        for j in range(1,3):
            if map[i][0] < map[i + 1][0]:
                image_data[(y * 3)][(x * 3) + j] = [255 * (i/size**2),0,255 * (((size**2)-i)/size**2)]
                frames.append(Image.fromarray(image_data))
                video.write(image_data)
            if map[i][0] > map[i + 1][0]:
                image_data[(y * 3)][(x * 3) - j] = [255 * (i/size**2),0,255 * (((size**2)-i)/size**2)]
                frames.append(Image.fromarray(image_data))
                video.write(image_data)
            if map[i][1] > map[i + 1][1]:
                image_data[(y * 3) - j][(x * 3)] = [255 * (i/size**2),0,255 * (((size**2)-i)/size**2)]
                frames.append(Image.fromarray(image_data))
                video.write(image_data)
            if map[i][1] < map[i + 1][1]:
                image_data[(y * 3) + j][(x * 3)] = [255 * (i/size**2),0,255 * (((size**2)-i)/size**2)]
                frames.append(Image.fromarray(image_data))
                video.write(image_data)
    
        
    # video.write(image_data)
    # frames.append(Image.fromarray(image_data))


frames[0].save(
        'Hilbert\output.gif',
        save_all=True,
        append_images=frames[1:],
        duration=1,  # Duration of each frame in milliseconds
        loop=0      # 0 means loop indefinitely
    )

video.release()
    
    
    #starting_points = [starting_point,[starting_point[0] + h_size,starting_point[1]],[starting_point[0] + h_size,starting_point[1] + h_size],[starting_point[0],starting_point[1] + h_size]]
   
   