from PIL import Image
import numpy as np
import math

def get_similarity_of_colors(color1,color2):
    avg = 0.0
    for i in range(3):
        avg += abs(color1[i]-color2[i]) 
    return int(avg/3.0)

def get_dist(point1,point2):
   return (((point2[0]-point1[0])**2) + ((point2[1]-point1[1])**2))**(1/2)

def get_compatibility(pixel1,pixel2):
    if get_dist(pixel1[0],pixel2[0]) != 0:
        return ((255 - get_similarity_of_colors(pixel1[1],pixel2[1])))/(get_dist(pixel1[0],pixel2[0]))
    else:
        return (255 - get_similarity_of_colors(pixel1[1],pixel2[1]))/1


image1 = Image.open("ImageMorph/fall_256.png")
image2 = Image.open("ImageMorph/night_256.png")

data1 =  np.asarray(image1)
data2 = np.asarray(image2)

size = len(data1)

print("Counting 1")
count = 0
for i in range(size**2 ):
    count += size**2 - i

pool1 = list()
pool2 = list()

pairs = list()

print("Pooling 1")
for x in range(len(data1)):
    for y in range(len(data1[0])):
        pool1.append([[x,y],data1[x][y]])
        
n_pool1 = list()
for i in range(len(pool1)):
    n_pool1.append(pool1.pop(np.random.randint(0,len(pool1))))
pool1 = n_pool1
        
print("Pooling 2") 
for x in range(len(data2)):
    for y in range(len(data2[0])):
        pool2.append([[x,y],data2[x][y]])
        
print("Pairing") # MOST IMPORTANT PART
percent = 0
for i,pixel1 in enumerate(pool1):
    print(f"{(percent * 100)/(count):.3f}")
    percent += len(pool2)
    
    compatibilities = list()
    for pixel2 in pool2:
        compatibilities.append([get_compatibility(pixel1,pixel2),pixel2])
    compatibilities.sort()
    pairs.append([pixel1,compatibilities[0][1]])
    del pool2[pool2.index(compatibilities[0][1])]
    
    #NAIVE APPRROACH ^^^ Noisey outputs
    #Better one: pair every pixel with its most opimal ones, deal with contestions recurisvly
    
    #pair every pixel with its most opimal one
    # all pairs that are uncontested are locked in
    # Three groups: Pairs already made, pixels in pool2 not paired with, pairs that are contestedf
    # Among contested pairs, loop through them and see which pixel is the best match
    # Make that pair and continue, lock in the pairs
    #There is now many unpaired pool1 pixels and pool2 pixels
    # assign them their most optimal pixel
    # repeat the algo untill all paires are made
    
    
    
print("Creating")
morph_data1 = np.empty((len(data1),len(data2),3),dtype=np.uint8)
morph_data1.fill(0)  
for pair in pairs:
    pixel1 = pair[0]
    pixel2 = pair[1]
    for i in range(3):
        morph_data1[pixel2[0][0]][pixel2[0][1]][i] = pixel1[1][i]

morph_data2 = np.empty((len(data1),len(data2),3),dtype=np.uint8)
morph_data2.fill(0)  
for pair in pairs:
    pixel1 = pair[0]
    pixel2 = pair[1]
    for i in range(3):
        morph_data2[pixel1[0][0]][pixel1[0][1]][i] = pixel2[1][i]
        
morph1 = Image.fromarray(morph_data1)
morph2 = Image.fromarray(morph_data2)
combined_img = Image.new('RGB', (len(morph_data1) * 3, len(morph_data1) * 2), (255, 255, 255)) 

combined_img.paste(image1, (0, 0)) # Paste img1 at top-left
combined_img.paste(morph1 , (len(morph_data1), 0)) # Paste img1 at top-left
combined_img.paste(image2, (len(morph_data1) * 2, 0)) # Paste img2 next to img1

combined_img.paste(image2, (0, len(morph_data1))) # Paste img1 at top-left
combined_img.paste(morph2 , (len(morph_data1), len(morph_data1))) # Paste img1 at top-left
combined_img.paste(image1, (len(morph_data1) * 2, len(morph_data1))) # Paste img2 next to img1


combined_img.show()
combined_img.save("ImageMorph/output.png")
    

        
        
