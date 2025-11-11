import math
import numpy as np
from PIL import Image

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


bounds = [[-2.1,0.7],[-1.2,1.2]]
# bounds = [[-1.7670,-1.7662],[0.0415,0.042]]
size = 8000 * 2 * 2
ratio = (bounds[0][1] - bounds[0][0])/(bounds[1][1] - bounds[1][0])
res_rec = [0,0, ratio * size, size]


tolerance = 4
precision = 100 # tolerance > precision  

frames = []
i = (-1)**(1/2)

for n in range(1):
    
    
    image_data = np.empty((int(res_rec[3]),int(res_rec[2]),3),dtype=np.uint8)
    image_data.fill(0)  
    for x in range(int(res_rec[2])):
        print(x/int(res_rec[2]))
        for y in range(int(res_rec[3])):
            
            x1 = ((x/res_rec[2]) * (bounds[0][1] - bounds[0][0])) + bounds[0][0]
            y1 = ((y/res_rec[3]) * (bounds[1][1] - bounds[1][0])) + bounds[1][0]
            image_data[y][x]  = [0,0,0]
            z = complex(0)
            c = complex(x1 + y1 * i)
            for _ in range(precision):
                z = z*z + c
                if max(abs(z.real), abs(z.imag)) > tolerance:
                    break
            
            if max(abs(z.real), abs(z.imag)) < tolerance:
                 color = rainbow(max(abs(z.real), abs(z.imag)),tolerance) #min((max(abs(z.real),abs(z.imag))/tolerance) * 255,255)
            else:
                color = [0,0,0]
            image_data[y][x] = color
    image = Image.fromarray(image_data)
    frames.append(image)
    # tolerance += 1
        
frames[0].save(
    'mandelbrot/output.gif',
    save_all=True,
    append_images=frames[1:],
    duration=10,  # Duration of each frame in milliseconds
    loop=0      # 0 means loop indefinitely
    )      
print("Done!")  


# image.show()  
# image.save("mandelbrot/output.png")
