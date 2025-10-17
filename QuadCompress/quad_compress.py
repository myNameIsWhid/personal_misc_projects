from PIL import Image
import numpy as np
import math
image = Image.open("balloon.png")
data = np.asarray(image)

def avg_color_of_image(image_data):
    skip = 1
    sum = [0.0,0.0,0.0]
    size = float(len(image_data) * len(image_data[0]))/(skip * skip)
   # if size == 1:
     #   print("small")
    for x in range(int(len(image_data)//skip)):
        for y in range(int(len(image_data[0])//skip)):
            pixel = image_data[x * skip][y * skip]
            for i in range(3):
                sum[i] += float(pixel[i])
   
    return [int(sum[0]/size) ,int(sum[1]/size) ,int(sum[2]/size)]

def standard_deviation_color_of_image(image_data, mean):
    skip = 1
    if len(image_data) == skip:
        return [0,0,0]
    
    sum = [0.0,0.0,0.0]
    st_dev = [0.0,0.0,0.0]
    for x in range(int(len(image_data)//skip)):
        for y in range(int(len(image_data[0])//skip)):
            pixel = image_data[x * skip][y * skip]
            for i in range(3):
                sum[i] += (float(pixel[i]) - float(mean[i])) ** 2
    size = (len(image_data) * len(image_data[0]))/(skip * skip)
    for i in range(3):
        st_dev[i] = math.sqrt(sum[i]/(size - 1))
    return st_dev

def avg(list):
    sum = 0.0
    for i in range(len(list)):
        sum += list[i]
    return int(sum/len(list))

def quad_tree(new_image,image_square,source,tolerance,res):
    
    width = int(image_square[2])
    height = int(image_square[3])
    starting_point = [int(image_square[0]),int(image_square[1])]
    nw = np.empty((int(width/2),int(height/2),3),dtype=np.uint8)
    ne = np.empty((int(width/2),int(height/2),3),dtype=np.uint8)
    se = np.empty((int(width/2),int(height/2),3),dtype=np.uint8)
    sw = np.empty((int(width/2),int(height/2),3),dtype=np.uint8)
    starting_points = [starting_point,[starting_point[0] + width/2,starting_point[1]],[starting_point[0] + width/2,starting_point[1] + height/2],[starting_point[0],starting_point[1] + height/2]]
   
    lower_range = width/2 - 1
    upper_range = width/2 
    
    squares = list()
    for x in range(width):
        for y in range(height):
            pixel = [0,0,0]
            for i in range(3):
                pixel[i] = int(source[int(x + starting_point[0])][int(y + starting_point[1])][i])
            if x <= lower_range and y <= lower_range:
                nw[x][y] = pixel
            elif x >= upper_range and y  <= lower_range:
                ne[int(x - width/2)][y] = pixel
            elif x >= upper_range and y >= upper_range:
                se[int(x - width/2)][int(y - height/2)] = pixel
            elif x <= lower_range and y >= upper_range:
                sw[x][int(y - height/2)] = pixel
            else:
                print(f"Missing Pixel at ({x} , {y}) with half-width {width/2}")          
                
    squares.append(nw)
    squares.append(ne)
    squares.append(se)
    squares.append(sw)
    
    for i in range(len(squares)):
        square = squares[i]
        avg_color = avg_color_of_image(square)
        if avg(standard_deviation_color_of_image(square,avg_color)) > tolerance and width/2 > res:
            quad_tree(new_image,[starting_points[i][0],starting_points[i][1],width/2,height/2],source,tolerance,res)
        else:
            # if len(square) <= res:
            #     color = [max(avg_color),max(avg_color),max(avg_color)]
            # else:
            #     color = [0,0,0]
                
            for x in range(int(starting_points[i][0]),int(starting_points[i][0] + width/2)):
                for y in range(int(starting_points[i][1]),int(starting_points[i][1] + height/2)):
                        new_image[x][y] = avg_color
                    


frames = list()
for i in range(50):
    new_image_data = np.empty((image.size[1],image.size[0],3),dtype=np.uint8)
    new_image_data.fill(0)
    quad_tree(new_image_data,[0,0,len(data),len(data)],data,i,1)
    #Image.fromarray(new_image_data).show()
    frames.append(Image.fromarray(new_image_data))
    print(i)
    
    
    
frames[0].save(
        'output4.gif',
        save_all=True,
        append_images=frames[1:],
        duration=100,  # Duration of each frame in milliseconds
        loop=0    # 0 means loop indefinitely
    )




#new_image.save("Misc/Quad/output.png")
#frames[0].show()