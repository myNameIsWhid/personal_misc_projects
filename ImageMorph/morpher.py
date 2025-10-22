from PIL import Image
import numpy as np
import math
from progress.bar import Bar 
import cv2

def get_similarity_of_colors(color1,color2):
    avg = 0.0
    for i in range(3):
        avg += abs(float(color1[i])-float(color2[i])) 
    return int(avg/3.0)

def get_dist(point1,point2):
   return (((point2[0]-point1[0])**2) + ((point2[1]-point1[1])**2))**(1/2)

def get_compatibility(pixel1,pixel2):
    color_weight = 1
    if get_dist(pixel1[0],pixel2[0]) != 0:
        return (color_weight * ((255 - get_similarity_of_colors(pixel1[1],pixel2[1]))))#/get_dist(pixel1[0],pixel2[0])
    else:
        return (color_weight * (255 - get_similarity_of_colors(pixel1[1],pixel2[1])))

image1 = Image.open("ImageMorph/fall_1024.png")
image2 = Image.open("ImageMorph/night_1024.png")



data1 =  np.asarray(image1)
data2 = np.asarray(image2)

size = len(data1)

video = cv2.VideoWriter("ImageMorph/output.avi", cv2.VideoWriter_fourcc(*'DIVX'), 120, (size * 2 , size))

print("Counting 1")

count = int((16**2)*((1+(16**2))//2))
print(count, "count")

pool1 = list()
pool2 = list()

pairs = list()

print("Pooling 1")
for x in range(len(data1)):
    for y in range(len(data1[0])):
        pool1.append([[x,y],data1[x][y]])
        

        
print("Pooling 2") 
for x in range(len(data2)):
    for y in range(len(data2[0])):
        pool2.append([[x,y],data2[x][y]])
        

print("Initial Pairing") 

max_dist = 4

def video_add_frame():
    morph_data1 = np.empty((len(data1),len(data2),3),dtype=np.uint8)
    morph_data1.fill(0)  
    for pair in pairs:
        pixel1 = pair[0]
        pixel2 = pair[1]
        for i in range(3):
            morph_data1[pixel2[0][0]][pixel2[0][1]][i] = pixel1[1][2 - i]

    morph_data2 = np.empty((len(data1),len(data2),3),dtype=np.uint8)
    morph_data2.fill(0)  
    for pair in pairs:
        pixel1 = pair[0]
        pixel2 = pair[1]
        for i in range(3):
            morph_data2[pixel1[0][0]][pixel1[0][1]][i] = pixel2[1][2 - i]
            
    morph1 = Image.fromarray(morph_data1)
    morph2 = Image.fromarray(morph_data2)
    combined_img = Image.new('RGB', (len(morph_data1) * 2, len(morph_data1)), (255, 255, 255)) 
    combined_img.paste(morph1, (0, 0)) # Paste img1 at top-left
    combined_img.paste(morph2 , (len(morph_data1), 0)) # Paste img1 at top-left
    video.write(np.asarray(combined_img))
    

def make_image(kind = 2):
    print("Creating")
    morph_data1 = np.empty((len(data1),len(data2),3),dtype=np.uint8)
    morph_data1.fill(255)  
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
    if(kind == 2):
        combined_img = Image.new('RGB', (len(morph_data1) * 3, len(morph_data1) * 2), (255, 255, 255)) 

        combined_img.paste(image1, (0, 0)) # Paste img1 at top-left
        combined_img.paste(morph1 , (len(morph_data1), 0)) # Paste img1 at top-left
        combined_img.paste(image2, (len(morph_data1) * 2, 0)) # Paste img2 next to img1

        combined_img.paste(image2, (0, len(morph_data1))) # Paste img1 at top-left
        combined_img.paste(morph2 , (len(morph_data1), len(morph_data1))) # Paste img1 at top-left
        combined_img.paste(image1, (len(morph_data1) * 2, len(morph_data1))) # Paste img2 next to img1

        combined_img.show()
        
        combined_img.save("ImageMorph/output.png")
    elif kind == 1:
        morph1.save("ImageMorph/morph1.png")
        morph1.show()
    else:
        morph2.save("ImageMorph/morph2.png")
        

    
def pair_opimtmally_and_resolve_conflicts(pool1,pool2,pairs):
    # compatibility_avg = 0
    # for i,pixel1 in enumerate(pool1):
    #     print(f"{(i * 100)/(len(pool1)):.3f}")
        
    #     best_compatibility = -1
    #     most_compatible_pixel = pool2[0]

    #     for x in range(pixel1[0][0] - (max_dist//2),pixel1[0][0] + (max_dist//2)):
    #         if x < 0:
    #             continue
    #         if x >= size:
    #             break
    #         for y in range(pixel1[0][1] - (max_dist//2),pixel1[0][1] + (max_dist//2)):
    #             if y < 0:
    #                 continue
    #             if y >= size:
    #                 break

    #             if(not ((y + x * size) in taken)):
    #                 pixel2 = pool2[y + x * size]
    #                 compatibility = get_compatibility(pixel1,pixel2)
    #                 if compatibility > best_compatibility:
    #                     most_compatible_pixel = pixel2
    #                     best_compatibility = compatibility 
    #     compatibility_avg += best_compatibility
    #     taken.append(most_compatible_pixel[0][1] + most_compatible_pixel[0][0] * size)
    #     pairs.append([pixel1,most_compatible_pixel])
    
    compatibility_avg = 0
    for i,pixel1 in enumerate(pool1):
        print(f"{(i * 100)/(len(pool1)):.3f}")
        
        best_compatibility = -1
        most_compatible_pixel = pool2[0]
        
        for x in range(pixel1[0][0] - (max_dist//2),pixel1[0][0] + (max_dist//2)):
            if x < 0:
                continue
            if x >= size:
                break
            for y in range(pixel1[0][1] - max_dist//2,pixel1[0][1] + max_dist//2):
                if y < 0:
                    continue
                if y >= size:
                    break
                
                pixel2 = pool2[y + x * size]
                compatibility = get_compatibility(pixel1,pixel2)
                if compatibility > best_compatibility:
                    most_compatible_pixel = pixel2
                    best_compatibility = compatibility 
        
        pairs.append([pixel1,most_compatible_pixel])
    compatibility_avg = compatibility_avg/len(pool1)



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

    print(f"{((len(conflicts) * 100)/(size**2)):.2f}")

    print(f"{len((conflicts))} conflcits are left to review, with {len(available_pool)} pixels to be matched")

    print(f"{compatibility_avg} compatibility average" )
    suffient_compatibility = 255 #compatibility_avg * 0.9

    while(len(conflicts) != 0):
        i = 0
        to_review = list()
        to_review_values = list()
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
            to_review.append(most_compatible_contestant)
            to_review_values.append(most_compatible_contestant[1])
            
            if most_compatible_contestant[1] in available_pool:
                del available_pool[available_pool.index(most_compatible_contestant[1])]
                
            del c_contestants[c_contestants.index(most_compatible_contestant)]
            #give the rest the optimal avaibale pixels
            for contestant in c_contestants:
                best_compatibility = -1
                most_compatible_pixel = available_pool[0]
                for a_pixel in available_pool:
                    compatibility = get_compatibility(contestant[0],a_pixel)
                    if compatibility > suffient_compatibility:
                        most_compatible_pixel = a_pixel
                        best_compatibility = compatibility
                        break
                    if compatibility > best_compatibility:
                        best_compatibility = compatibility
                        most_compatible_pixel = a_pixel
                to_review.append([contestant[0],most_compatible_pixel])
                to_review_values.append(most_compatible_pixel)
                # if best_compatibility > suffient_compatibility:
                #       del available_pool[available_pool.index(most_compatible_pixel)] # pixel is no longer available
        #add none conlicts back to source
        #add any conflicts back to conlicts and redo


        conflicts = list()
        sucess = 0

        for pair1 in to_review:
            if pair1 in conflicts:
                continue
            if to_review_values.count(pair1[1]) == 1:
                sucess += 1
                for j,source_pair in enumerate(pairs):
                    if source_pair[0] == pair1[0]:
                        pairs[j] = pair1 #add to source
                        if pair1[1] in available_pool:
                            del available_pool[available_pool.index(pair1[1])] # pixel is no longer available
                        break
            else:
                temp = None
                contested = 0
                for pair2 in to_review:  
                    if pair2 in conflicts:
                        continue
                    pixel2 = pair2[1]
                    if pair1[1] == pixel2:
                        
                        if contested == 0:
                            temp = pair2
                        if contested == 1:
                            conflicts.append(temp)
                            conflicts.append(pair2)
                        if contested > 1:
                            conflicts.append(pair2)
                        contested += 1

                
        print(f"{sucess} were resloved, {len(conflicts)} are left, and {len(available_pool)} pixels remain unmatched")

def opimize_pairs_iterativly(pool1,pool2,pairs):
    
    
    # Shuffle
  
    # n_pool1 = list()
    # for i in range(len(pool1)):
    #     n_pool1.append(pool1.pop(np.random.randint(0,len(pool1))))
    # pool1 = n_pool1
    
    compatibilites = list()
    
    min_dist = size//2
    # taken = list()
   
    # for i in range(len(pool1)):
    #     taken.append(False)
        
    # with Bar('Processing...') as bar:  
    #     bar.max = len(pool1)
    #     for pixel1 in pool1:
    #         bar.next()
    #         c_min_dist = min_dist
            
    #         best_compatibility = -1
    #         most_compatible_pixel = pool2[0]
    #         c_min_dist_min = 0
            
    #         while(best_compatibility == -1):
    #             for j in range(c_min_dist_min,c_min_dist + 1):
    #                 x_bounds = [pixel1[0][0] - (j),pixel1[0][0] + (j)]
    #                 y_bounds = [pixel1[0][1] - (j),pixel1[0][1] + (j)]
    #                 for x in range(x_bounds[0],x_bounds[1] + 1):
    #                     if x < 0:
    #                         continue
    #                     if x >= size:
    #                         break
    #                     for y in range(y_bounds[0],y_bounds[1] + 1):
    #                         if y < 0:
    #                             continue
    #                         if y >= size:
    #                             break
    #                         if not(x == x_bounds[0] or x == x_bounds[1] or y == y_bounds[0] or y == y_bounds[1]):
    #                             continue
    #                         if taken[y + x * size]:
    #                             continue
    #                         pixel2 = pool2[y + x * size]
    #                         compatibility = get_compatibility(pixel1,pixel2)
    #                         if compatibility > best_compatibility:
    #                             most_compatible_pixel = pixel2
    #                             best_compatibility = compatibility 
    #             if best_compatibility == -1:
    #                 c_min_dist_min = c_min_dist 
    #                 c_min_dist += 1
                    
    #                 continue
    #             compatibilites.append(best_compatibility)
    #             taken[most_compatible_pixel[0][1] + most_compatible_pixel[0][0] * size] = True
    #             pairs.append([pixel1,most_compatible_pixel])
    for i in range(size**2):
        pairs.append([pool1[i],pool2[i]])
    
    frame_chance = 20
    score = sum(compatibilites)
    swaps = list()
    with Bar('Processing...') as bar:  
        max = 2000000
        
        bar.max = max
        interval = 0
        while(True):
            bar.next()
            interval += 1
            if interval % max == 0:
        
                bar.index = 0
                new_score = 0
                i = 0
                # video.release()
                for i in range(len(pairs)):
                    new_score += get_compatibility(pairs[i][0],pairs[i][1])
                print("Improved by",(100 * (new_score - score))/(score + 1))
                score = new_score
                make_image()
                
            swap_size = np.random.randint(1,5 + 1)
            indexs = [[np.random.randint(0,size - swap_size + 1),np.random.randint(0,size - swap_size + 1)]
                      ,[np.random.randint(0,size - swap_size + 1),np.random.randint(0,size - swap_size + 1)]]
            
            while indexs[0] == indexs[1]:
                indexs[1] = [np.random.randint(0,size - swap_size + 1),np.random.randint(0,size - swap_size + 1)] # no swapimg same item
                
            swaped_pairs = list()
            old_compatibilities = list()
            new_compatibilities = list()
            
            for x in range(swap_size):
                for y in range(swap_size):
                 #print((indexs[0]), x,(indexs[0]) + y)
                 pos = [[(indexs[0][0]) + x,(indexs[0][1]) + y],[(indexs[1][0]) + x,(indexs[1][1]) + y]] #
                 
                 pairs_to_swap = [pairs[pos[0][1] + pos[0][0] * size],pairs[pos[1][1] + pos[1][0] * size]]
                 
                 swaped_pairs.append([[pairs_to_swap[0][0],pairs_to_swap[1][1]],[pairs_to_swap[1][0],pairs_to_swap[0][1]]])
                 
                 old_compatibilities.append(get_compatibility(pairs_to_swap[0][0],pairs_to_swap[0][1]))
                 old_compatibilities.append(get_compatibility(pairs_to_swap[1][0],pairs_to_swap[1][1]))
                 
                 new_compatibilities.append(get_compatibility(pairs_to_swap[0][0],pairs_to_swap[1][1]))
                 new_compatibilities.append(get_compatibility(pairs_to_swap[1][0],pairs_to_swap[0][1]))
            if sum(new_compatibilities) > sum(old_compatibilities):
                #  if interval % frame_chance == 0:
                #     video_add_frame()
                 for x in range(swap_size):
                    for y in range(swap_size):
                        pos = [[(indexs[0][0]) + x,(indexs[0][1]) + y],[(indexs[1][0]) + x,(indexs[1][1]) + y]]
                        #print(x,y*size,len(swaped_pairs))
                        pairs[pos[0][1] + pos[0][0] * size] = swaped_pairs[(x + y * swap_size)][0]
                        pairs[pos[1][1] + pos[1][0] * size] = swaped_pairs[(x + y * swap_size)][1]
                        
    
    
    make_image()
        
        
    
    
    #Make intial paring
    #Swap two pairs and check new score
    # if new score is better than old score, make it the default one.
    # repeat as desried
    
    
  
# pair_opimtmally_and_resolve_conflicts(pool1,pool2,pairs)

opimize_pairs_iterativly(pool1,pool2,pairs)
    
        

        
        
    
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
    
    

        

        
        
