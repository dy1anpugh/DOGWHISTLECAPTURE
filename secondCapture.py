import pytesseract
from PIL import ImageEnhance
import pandas as pd
import mss
from PIL import Image
# import keyboard
import numpy as np
import time
import networkx as nx
import matplotlib.pyplot as plt
import pygetwindow as gw

text_check=[]
visited_dogs=[]
dogs_amnt=[]
urlArray=[]
# DOGWHISTLE DATA SET
df = pd.read_parquet("hf://datasets/SALT-NLP/silent_signals/data/train-00000-of-00001.parquet")
dw=df['dog_whistle']
dw_root = df['dog_whistle_root']
dw_definition=df['definition']


extra_dog=["Red Pill","red pill","red-pilled","Blue-Pilled","blue-pilled","ldar","LDAR","Black Pill", "black pill", "chemtrails","1776"]
extra_dog_root=['From the 1999 movie "The Matrix','From the 1999 movie "The Matrix"','From the 1999 movie "The Matrix"','From the 1999 movie "The Matrix" as an alternative to the Red-Pill','From the 1999 movie "The Matrix" as an alternative to the Red-Pill',"Lay down and rot","Lay down and rot", "An extension of the incel concept of the 'Red Pill'", "An extension of the incel concept of the 'Red Pill'",'n/a','The year America gained independence from the British']
extra_dog_definition = ["The misogynistic belief that women run the world and yet don't take accountability for it","The misogynistic belief that women run the world and yet don't take accountability for it",
                        "The misogynistic belief that women run the world and yet don't take accountability for it","The misogynistic belief that women run the world and yet don't take accountability for it, "
                        "applied to so called 'normies'","The misogynistic belief that women run the world and yet don't take accountability for it, applied to so called 'normies'",
                        "Term used by incels believing the only way to deal with the world is bedrotting","Term used by incels believing the only way to deal with the world is bedrotting", 
                        "The misogynistic belief that women run the world and violence is a tool that should be used to counteract that", "The misogynistic belief that women run the world and violence is a tool that should be used to counteract that",'Not necessarily a DW, but conspiracy theory perpetuated by RW that the trails left by planes are chemical toxins in the air made by the government to control you ','Often used by American nationalists in their bios as a nod that they are for violent revolutionary behaviour to "take their country back"']
annoying_dogs=['EST', 'est', '41', 'Chicago']


dws=dw.tolist()





# SCREENSHOT
while True:
    # sct=mss()
    # filename = sct.shot()
    # print(type(filename))
    # READ TEXT

    with mss.mss() as sct:
    # The screen part to capture
        # PRIMARY SCREEN
        monitor = {"top": 174, "left": 366, "width": 600, "height": 906}
        # monitor2 = {"top": 0, "left": 0, "width": 278, "height": 43}
        output = "sct.png".format(**monitor)
        # output = "url.png".format(**monitor2)
        
        # # SECONDARY SCREEN
        # monitor_number = 2
        # mon = sct.monitors[monitor_number]
        # monitor = {"top": mon["top"] + 174, "left": mon["top"] +  750, "width": 600, "height": 906, "mon": monitor_number}
        # output = "sct.png".format(**monitor)
    # Grab the data
        sct_img = sct.grab(monitor)

    # Save to the picture file
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)


    text = pytesseract.image_to_string("sct.png")
    
    
    # print(text)


    # GET URL
    url=gw.getActiveWindowTitle()

    urlArray.append(url)



    print('NEW CAPTURE \n-------------')
    # FIND DOGWHISTLE + PRINT
    for n in range(16257):
        dog=dws[n]
        
        # print(dog)
        # dw=pd.DataFrame.drop_duplicates()
        if dog in text and dog not in visited_dogs and dog not in annoying_dogs:
            # and text!=text_check    
            context=text.split(dog)
            
        
            print("!!FOUND "+ dog + "!!")
            print('Context: "'+context[0][-10:]+dog +'"')
            print('Root of:')
            print(dw_root[n])
            print('Alt-Right Definition:')
            print(dw_definition[n])
            visited_dogs.append(dog)
            dogs_amnt.append(dog)
            outputs="!!FOUND "+ dog + '!!\nContext: ..."'+context[0][-10:]+dog +'"\nRoot of:\n'+dw_root[n]+'\nAlt-Right Definition:'+dw_definition[n]+"\n \n"

    for x in range (10):
        if extra_dog[x] in text and extra_dog[x] not in visited_dogs:
            
            extra_context=text.split(extra_dog[x])
            print("!!FOUND "+ extra_dog[x] + "!!")
            print('Context: "'+extra_context[0][-10:]+dog +'"')
            print('Root of:')
            print(extra_dog_root[x])
            print('Alt-Right Definition:')
            print(extra_dog_definition[x])
            visited_dogs.append(extra_dog[x])
            dogs_amnt.append(extra_dog[x])     
            extra_outputs="!!FOUND "+ extra_dog[x] + '!!\nContext: ..."'+context[0][-10:]+extra_dog[x] +'"\nRoot of:\n'+extra_dog_root[x]+'\nAlt-Right Definition:'+extra_dog_definition[x]+"\n \n"       
    
    text_check=[text]


    time.sleep(10)
    visited_dogs=[]
        
    if len(urlArray)==25:
            print('FOUND DOGWHISTLES IN SESSION :' + str(len(dogs_amnt)))
            break
    


urldata=pd.DataFrame(urlArray)

urldata.to_csv('ALLURLS.csv', index=False,mode='a', header=False)


Graph = nx.Graph()


# df = pd.DataFrame(urlArray)
# # Save the DataFrame to a CSV file
# df.to_csv('myarray.csv', index=False, header=False)


# Add nodes and edges (representing relationships)
for x in range((len(urlArray))-1):
        Graph.add_edge(urlArray[x][:20]+'..',urlArray[x+1][:20]+'..')
    
    # Draw the graph with matplotlib
nx.draw(Graph, with_labels=True)
plt.show()

    


# LIVE STREAM SCREEN
# bounding_box = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}

# sct = mss()

# while True:
#     sct_img = sct.grab(bounding_box)
#     cv2.imshow('screen', np.array(sct_img))

#     if (cv2.waitKey(1) & 0xFF) == ord('q'):
#         cv2.destroyAllWindows()
#         break