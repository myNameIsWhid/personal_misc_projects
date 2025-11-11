import math
import numpy as np
from PIL import Image
bounds = [[-2,1],[-1,1]]
# bounds = [[-1.7670,-1.7662],[0.0415,0.042]]
size = 200
res_rec = [0,0,(bounds[0][1] - bounds[0][0])  * size,(bounds[1][1] - bounds[1][0]) * size]

image_data = np.empty((int(res_rec[2]),int(res_rec[3]),3),dtype=np.uint8)
image_data.fill(0)  

tolerance = 100
precisoion = 1000 # tolerance > precisoion  

i = (-1)**(1/2)

for x in range(int(res_rec[2])):
    print(x/res_rec[2])
    for y in range(int(res_rec[3])):
        
        x1 = ((x/res_rec[2]) * (bounds[0][1] - bounds[0][0])) + bounds[0][0]
        y1 = ((y/res_rec[3]) * (bounds[1][1] - bounds[1][0])) + bounds[1][0]
        image_data[x][y]  = [0,0,0]
        z = complex(0)
        for _ in range(precisoion):
            z = z*z + (x1 + y1 * i)
            if max(abs(z.real), abs(z.imag)) > tolerance:
                break
            
        color = min((max(abs(z.real),abs(z.imag))/tolerance) * 255,255)
        image_data[x][y] = [color, color, color]

image = Image.fromarray(image_data)
image.show()  
image.save("mandelbrot/output.png")
