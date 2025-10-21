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
        return ((255 - get_similarity_of_colors(pixel1[1],pixel2[1])))/(get_dist(pixel1[0],pixel2[0])) #squared
    else:
        return (255 - get_similarity_of_colors(pixel1[1],pixel2[1]))/0.5

image1 = Image.open("ImageMorph/fall_32.png")
image2 = Image.open("ImageMorph/night_32.png")

data1 =  np.asarray(image1)
data2 = np.asarray(image2)

size = len(data1)

print("Counting 1")

count = int((size**2)*((1+(size**2))//2))

pool1 = list()
pool2 = list()

pairs = list()

print("Pooling 1")
for x in range(len(data1)):
    for y in range(len(data1[0])):
        pool1.append([[x,y],data1[x][y]])
        
#Shuffle
# n_pool1 = list()
# for i in range(len(pool1)):
#     n_pool1.append(pool1.pop(np.random.randint(0,len(pool1))))
# pool1 = n_pool1
        
print("Pooling 2") 
for x in range(len(data2)):
    for y in range(len(data2[0])):
        pool2.append([[x,y],data2[x][y]])
        

print("Initial Pairing") 
percent = 0
max_dist = size//2

for i,pixel1 in enumerate(pool1):
    print(f"{(i * 100)/(len(pool1)):.3f}")
    
    best_compatibility = -1
    most_compatible_pixel = pool2[0]
    
    for x in range(pixel1[0][0] - (max_dist//2) + 1,pixel1[0][0] + (max_dist//2) - 1):
        if x < 0 or x >= size:
            continue
        for y in range(pixel1[0][1] - max_dist//2 + 1,pixel1[0][1] + max_dist//2 - 1):
            if y < 0 or y >= size:
                continue
            pixel2 = pool2[y + x * size]
            compatibility = get_compatibility(pixel1,pixel2)
            if compatibility > best_compatibility:
                most_compatible_pixel = pixel2
                best_compatibility = compatibility 
    pairs.append([pixel1,most_compatible_pixel])


print("Resvoling Conflicts") # MOST IMPORTANT PART
conflicts = list()
available_pool = list()

for pixel2 in pool2:
    contested = 0
    paired = False
    temp = None
    for pair in pairs:    
        if pair[1] == pixel2:
            paired = True
            if contested == 0:
                temp = pair
            if contested == 1:
                conflicts.append(temp)
                conflicts.append(pair)
            if contested > 1:
                conflicts.append(pair)
            contested += 1
    if not paired:
        available_pool.append(pixel2)
# conflicts should be in order like -> [0,0,0,0,1,1,2,2,2]

print(f"{100.0 - (len(conflicts)/(64**2))}f.2f")


to_review = list()

while(len(conflicts) != 0):
    i = 0
    print("Resvoling Conflicts 1", len(conflicts))
    while(i < len(conflicts)):
        c_pixel = conflicts[i][1]
        c_contestants = list()

        while i < len(conflicts) and conflicts[i][1] == c_pixel:
            c_contestants.append(conflicts[i])
            i += 1
        
        best_compatibility = -1
        most_compatible_contestant = c_contestants[0]
        
        #give the most deserving contestant c_pixel
            # c_contestants[0] is the pixel to be given best pair
            # c_contestants[1] is the pixel that they share
        for contestant in c_contestants:
            compatibility = get_compatibility(contestant[0],contestant[1])
            if compatibility > best_compatibility:
                best_compatibility = compatibility
                most_compatible_contestant = contestant
        #Remove locked in pairs
        del c_contestants[c_contestants.index(most_compatible_contestant)]
        #give the rest the optimal avaibale pixels
        for contestant in c_contestants:
            best_compatibility = -1
            most_compatible_pixel = None
            for a_pixel in available_pool:
                compatibility = get_compatibility(contestant[0],a_pixel)
                if compatibility > best_compatibility:
                    best_compatibility = compatibility
                    most_compatible_pixel = a_pixel
            to_review.append([c_contestants[0],most_compatible_pixel])
    
    #add none conlicts back to source
    #add any conflicts back to conlicts and redo
  
    print("Resvoling Conflicts 2", len(conflicts), len(to_review))

    conflicts = list()
    sucess = 0
    for pair1 in to_review:
        contested = 0
        for pair2 in to_review:  
            pixel2 = pair2[1]
            if pair1[1] == pixel2:
                if contested >= 1:
                    conflicts.append(pair)
                contested += 1
        if contested == 1: # if not contested
            sucess += 1
            for source_pair in pairs:
                if source_pair[0] == pair1:
                    source_pair = pair1 #add to source
                    del to_review[to_review.index(pair1)] #no need to review
                    del available_pool[available_pool.index(pair1[1])] # pixel is no longer available
                    break
    print("Resvoling Conflicts 3: shuld be less", len(conflicts),sucess)
    to_review = list()
        
            
    
    
        

        
        
    
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
    

        
        
