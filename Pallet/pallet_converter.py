from PIL import Image
import numpy as np
import math
image = Image.open("balloon.png")


data = np.asarray(image)

num_colors = 32
max_ajustment = 255
smaple_res = 20 # Bigger number is contrast

pallet = list()
possible_pallets = list()
pallet_timeline = list()

# for i in range(num_colors):
#     x = np.random.randint(0,image.size[1] - 1)
#     y = np.random.randint(0,image.size[0] - 1)
#     pallet.append([int(data[x][y][0]), int(data[x][y][1]),int(data[x][y][2])])
    

for i in range(num_colors):
    pallet.append([255/(num_colors - 1) * i, 255/(num_colors - 1) * i,255/(num_colors - 1) * i])


def reset_possible_pallets(temp_pallet): # GOOD
    global pallet
    possible_pallets.clear()
    for i in range(num_colors * 3 * 2):
        possible_pallets.append(temp_pallet)

def clamp(n):
    if n < 0:
        return 0
    elif n > 255:
        return 255
    else:
        return n
    
def ajust_possible_pallets(ajustment):
    global possible_pallets
    temp_possible_pallets = list()
    for k in range(3):
        for j in range(2):
            for i in range(num_colors): 
                temp_pallet = list()  
                c_possible_pallet = possible_pallets[(k * (num_colors * 2)) + (j * num_colors) + i]
                for b in range(i): # keep before the same
                    temp_pallet.append([c_possible_pallet[b][0], c_possible_pallet[b][1], c_possible_pallet[b][2]])          
                if k == 0: # ajust one one
                    temp_pallet.append([clamp(c_possible_pallet[i][0] + (ajustment * (j * 2 - 1))), c_possible_pallet[i][1], c_possible_pallet[i][2]])
                if k == 1:
                    temp_pallet.append([c_possible_pallet[i][0], clamp(c_possible_pallet[i][1] + (ajustment * (j * 2 - 1))),c_possible_pallet[i][2]])
                if k == 2:
                    temp_pallet.append([c_possible_pallet[i][0], c_possible_pallet[i][1], clamp(c_possible_pallet[i][2] + (ajustment * (j * 2 - 1)))])
                for a in range(i + 1, num_colors): # keep after the same
                    temp_pallet.append([c_possible_pallet[a][0], c_possible_pallet[a][1], c_possible_pallet[a][2]])
                temp_possible_pallets.append(temp_pallet)
    possible_pallets = temp_possible_pallets

def get_similarity_of_colors(color1,color2):
    avg = 0.0
    for i in range(3):
        avg += abs(color1[i]-color2[i]) 
    return int(avg/3.0)
#0 -> Indenitcal 

reset_possible_pallets(pallet)
ajust_possible_pallets(0)






past_min_possible_score = 99999999999999999999999999999
min_possible_score = 99999999999999999999
temp_min_possible_score = 99999999999
temp_min_possible_pallet = pallet
ajustment = 1

while(True): # local minmiua
    
    min_score_of_pass = 9999999999999 # reset

    
    reset_possible_pallets(temp_min_possible_pallet)
    ajust_possible_pallets(ajustment)
    
    for c_pallet in possible_pallets: 
        possible_pallet_score = 0
        for x in range(int(len(data)/smaple_res)):
            for y in range(int(len(data[0])/smaple_res)):
                pixel = [int(data[x*smaple_res][y*smaple_res][0]),int(data[x*smaple_res][y*smaple_res][1]),int(data[x*smaple_res][y*smaple_res][2])]
                minScore = 9999999999999999999
                for pallet_color in c_pallet:
                    pallet_score = get_similarity_of_colors(pixel,pallet_color)
                    if pallet_score < minScore:   
                        minScore = pallet_score
                possible_pallet_score += minScore
        if possible_pallet_score < min_possible_score:
            min_score_of_pass = possible_pallet_score
            temp_min_possible_pallet = c_pallet
            pallet_timeline.append(temp_min_possible_pallet)
            
    if min_score_of_pass < min_possible_score:
        print(min_score_of_pass, min_possible_score - min_score_of_pass, ajustment)
        min_possible_score = min_score_of_pass
        ajustment += 1
    else:
        if ajustment < max_ajustment:
            pallet = temp_min_possible_pallet
            if past_min_possible_score <= min_possible_score:
                ajustment += 1
            else:
                print(min_possible_score, past_min_possible_score - min_possible_score, ajustment)
                ajustment = 1
            past_min_possible_score = min_possible_score
        else:
             if past_min_possible_score <= min_possible_score:
                break
             else:
                 ajustment = 1
            
        
        
        
print(min_possible_score, past_min_possible_score - min_possible_score, ajustment)
        

new_image_data = np.empty((image.size[1],image.size[0],3),dtype=np.uint8)
new_image_data.fill(0)


for x in range(int(len(data))):
    print(f"{(x * int(len(data[0])))/(int(len(data)) * int(len(data[0]))):.3f}")
    for y in range(int(len(data[0]))):
        pixel = [int(data[x][y][0]),int(data[x][y][1]),int(data[x][y][2])]
        minScore1 = 99999999999999999999999
        for pallet_color in pallet:
            pallet_score = get_similarity_of_colors(pixel,pallet_color)
            if pallet_score < minScore1:   
                minScore1 = pallet_score
                min_pallet_color = pallet_color
        for i in range(3):
            new_image_data[x][y][i] = min_pallet_color[i]
            
            
        
            
pallet_width = 15
            
pallet_timeline_array = np.empty((image.size[1],num_colors * pallet_width,3),dtype=np.uint8)
pallet_timeline_array.fill(0)



for i in range(image.size[1]//2):
    for j in range(num_colors):
        for w in range(pallet_width):
            y = int(((len(pallet_timeline) * i * 2)/len(pallet_timeline_array)))
            pallet_timeline_array[i][(w + (pallet_width * j))] = pallet_timeline[y][j]
            
            
for i in range(image.size[1]//2,image.size[1]):
    for j in range(num_colors):
         for w in range(pallet_width):
            pallet_timeline_array[i][(w + (pallet_width * j))] = pallet_timeline[len(pallet_timeline)-1][j]


new_image = Image.fromarray(new_image_data)
old_image = Image.fromarray(data)
timeline_image = Image.fromarray(pallet_timeline_array)

combined_img = Image.new('RGB', (image.size[0] * 2 + num_colors * pallet_width, image.size[1]), (255, 255, 255)) 

combined_img.paste(new_image , (0, 0)) # Paste img1 at top-left
combined_img.paste(timeline_image , (new_image.width, 0)) # Paste img1 at top-left
combined_img.paste(image, (new_image.width + num_colors * pallet_width, 0)) # Paste img2 next to img1

combined_img.show()
combined_img.save('compare.png')
new_image.save('new_image.png')

print("Complete!")