import pytesseract
import pandas as pd
import mss
from PIL import Image
import time
import networkx as nx
import matplotlib.pyplot as plt
import pygetwindow as gw
import win32print
import win32ui 
from PIL import Image, ImageWin
import customtkinter

text_check=[]
visited_dogs=[]
dogs_amnt=[]
urlArray=[]
annoying_dogs=['EST', 'est', '41']
# DOGWHISTLE DATA SET
df = pd.read_parquet("hf://datasets/SALT-NLP/silent_signals/data/train-00000-of-00001.parquet")
dw=df['dog_whistle']
dw_root = df['dog_whistle_root']
dw_definition=df['definition']
dws=dw.tolist()
# EXTRA DOGWHISTLES
extra_dog=["Red Pill","red pill","red-pilled","Blue-Pilled","blue-pilled","ldar","LDAR","Black Pill", "black pill", "chemtrails","1776","Jabbed","jabbed", "woke", "Woke", "wokeness"]
extra_dog_root=['From the 1999 movie "The Matrix"','From the 1999 movie "The Matrix"','From the 1999 movie "The Matrix"','From the 1999 movie "The Matrix" as an alternative to the Red-Pill','From the 1999 movie "The Matrix" as an alternative to the Red-Pill',
                "Lay down and rot","Lay down and rot", "An extension of the incel concept of the 'Red Pill'", "An extension of the incel concept of the 'Red Pill'",'n/a','The year America gained independence from the British','Vaccinated','Vaccinated', 
                "Past tense of awake, originally used as terminology of the left to 'stay woke' to social and economic discrimination", "An extension of the incel concept of the 'Red Pill'", "An extension of the incel concept of the 'Red Pill'",'n/a',
                'The year America gained independence from the British','Vaccinated','Vaccinated', "Past tense of awake, originally used as terminology of the left to 'stay woke' to social and economic discrimination", 
                "Past tense of awake, originally used as terminology of the left to 'stay woke' to social and economic discrimination", "Past tense of awake, originally used as terminology of the left to 'stay woke' to social and economic discrimination"]
extra_dog_definition = ["The misogynistic belief that women run the world and yet don't take accountability for it","The misogynistic belief that women run the world and yet don't take accountability for it",
                        "The misogynistic belief that women run the world and yet don't take accountability for it","The misogynistic belief that women run the world and yet don't take accountability for it, "
                        "applied to so called 'normies'","The misogynistic belief that women run the world and yet don't take accountability for it, applied to so called 'normies'",
                        "Term used by incels believing the only way to deal with the world is bedrotting","Term used by incels believing the only way to deal with the world is bedrotting", 
                        "The misogynistic belief that women run the world and violence is a tool that should be used to counteract that", "The misogynistic belief that women run the world and violence is a tool that should be used to counteract that",
                        'Not necessarily a DW, but conspiracy theory perpetuated by RW that the trails left by planes are chemical toxins in the air made by the government to control you ','Often used by American nationalists in their bios as a nod that they are for violent revolutionary behaviour to "take their country back"', 
                        'Using violent language to imply the COVID vaccine was unnecessary and an act of state violence', 'Using violent language to imply the COVID vaccine was unnecessary and an act of state violence', 
                        'Whilst originally being Left-Wing terminology, now is used by right wingers to brand anything vaguely progressive as "Woke nonsense", a sort of spiritual successor to the Anti-SJW terminology - "Blue haired libs" etc. implying people on the left shouldnt be outraged about anything and should just take the discrimination', 
                        'Whilst originally being Left-Wing terminology, now is used by right wingers to brand anything vaguely progressive as "Woke nonsense", a sort of spiritual successor to the Anti-SJW terminology - "Blue haired libs" etc. implying people on the left shouldnt be outraged about anything and should just take the discrimination',
                         'Whilst originally being Left-Wing terminology, now is used by right wingers to brand anything vaguely progressive as "Woke nonsense", a sort of spiritual successor to the Anti-SJW terminology - "Blue haired libs" etc. implying people on the left shouldnt be outraged about anything and should just take the discrimination' ]

# PRINTER SETUP
# Get the default printer
printer_name = win32print.GetDefaultPrinter()
# Open a handle to the printer
printer = win32print.OpenPrinter(printer_name)
# Start a print job
job = win32print.StartDocPrinter(printer, 1, ("Test Print", None, "RAW"))

def print_image(image_path):
    # Open the image
    image = Image.open(image_path)

    # Get the default printer
    printer_name = win32print.GetDefaultPrinter()

    # Get printer device context
    hprinter = win32ui.CreateDC()
    hprinter.CreatePrinterDC(printer_name)

    # Set up the printable area (adjust as necessary for your printer)
    printable_area = hprinter.GetDeviceCaps(8), hprinter.GetDeviceCaps(10)  # HORZRES, VERTRES
    print_resolution = hprinter.GetDeviceCaps(88), hprinter.GetDeviceCaps(90)  # LOGPIXELSX, LOGPIXELSY

    # Resize the image to fit within the printable area
    image_width, image_height = image.size
    scaled_width = int(image_width * print_resolution[0] / 96)  # Assuming original DPI is 96
    scaled_height = int(image_height * print_resolution[1] / 96)
    scaled_image = image.resize((scaled_width, scaled_height))

    # Start the print job
    hprinter.StartDoc("Printing Image")
    hprinter.StartPage()

    # Render the image to the printer's device context
    dib = ImageWin.Dib(scaled_image)
    dib.draw(hprinter.GetHandleOutput(), (0, 0, printable_area[0], int(printable_area[1]/3.5)))

    # End the print job
    hprinter.EndPage()
    hprinter.EndDoc()
    hprinter.DeleteDC()

def button_press():
    # SCREENSHOT
    global urlArray
    urlArray=[]
    printer_name = win32print.GetDefaultPrinter()
# Open a handle to the printer
    printer = win32print.OpenPrinter(printer_name)
    # Start a print job
    job = win32print.StartDocPrinter(printer, 1, ("Test Print", None, "RAW"))
    win32print.WritePrinter(printer, opening_string.encode("UTF-16LE"))
    win32print.EndPagePrinter(printer)
    win32print.EndDocPrinter(printer)
    
    printer = win32print.OpenPrinter(printer_name)
    # Start a print job
    job = win32print.StartDocPrinter(printer, 1, ("Test Print", None, "RAW"))
    # start_session.configure(state='disabled')
    while True:

        with mss.mss() as sct:
        # The screen part to capture
            # PRIMARY SCREEN
            monitor = {"top": 174, "left": 600, "width": 600, "height": 906}
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


        # TEXT RECOGNITION
        text = pytesseract.image_to_string("sct.png")
        print(text)


        # GET URL
        url=gw.getActiveWindowTitle()
        urlArray.append(url)



        print('NEW CAPTURE \n-------------')
        # FIND DOGWHISTLE + PRINT
        for n in range(16257):
            dog=dws[n]
            global visited_dogs
            # print(dog)
            # dw=pd.DataFrame.drop_duplicates()
            if dog in text and dog not in visited_dogs and dog not in annoying_dogs:
                #  and text!=text_check:
                context=text.split(dog)
                
            
                print("!!FOUND "+ dog + "!!")
                print('Context: "'+context[0][-10:]+dog +'"')
                print('Root of:')
                print(dw_root[n])
                print('Alt-Right Definition:')
                print(dw_definition[n])
                visited_dogs.append(dog)
                dogs_amnt.append(dog)
                outputs="!!FOUND "+ dog + '!!\nContext: "...'+context[0][-10:]+dog +'"\nRoot of:\n'+dw_root[n]+'\nAlt-Right Definition: '+dw_definition[n]+"\n \n"
                try:
                    win32print.StartPagePrinter(printer)    
                    win32print.WritePrinter(printer, outputs.encode("UTF-16LE"))
                    win32print.EndPagePrinter(printer)
                except:
                    print("Something went wrong")
                    
        for x in range (12):
            if extra_dog[x] in text and extra_dog[x] not in visited_dogs: 
            # and text!=text_check:
                
                extra_context=text.split(extra_dog[x])
                print("!!FOUND "+ extra_dog[x] + "!!")
                print('Context: "'+extra_context[0][-10:]+dog +'"')
                print('Root of:')
                print(extra_dog_root[x])
                print('Alt-Right Definition:')
                print(extra_dog_definition[x])
                visited_dogs.append(extra_dog[x])
                dogs_amnt.append(extra_dog[x])     
                extra_outputs="!!FOUND "+ extra_dog[x] + '!!\nContext: "...'+extra_context[0][-10:]+extra_dog[x] +'"\nRoot of:\n'+extra_dog_root[x]+'\nAlt-Right Definition: '+extra_dog_definition[x]+"\n \n"       
                
                try:
                    win32print.StartPagePrinter(printer)    
                    win32print.WritePrinter(printer, extra_outputs.encode("UTF-16LE"))
                    win32print.EndPagePrinter(printer)
                except:
                    print("Something went wrong")
        
        text_check=[text]


        time.sleep(5)
        visited_dogs=[]
            
        if len(urlArray)==8:
                print('FOUND DOGWHISTLES IN SESSION :' + str(len(dogs_amnt)))
                break
        
    win32print.EndDocPrinter(printer)
    win32print.ClosePrinter(printer)

    urldata=pd.DataFrame(urlArray)
    urldata.to_csv('ALLURLS.csv', index=False,mode='a', header=False)

    Graph = nx.Graph()


    # Add nodes and edges (representing relationships)
    for x in range((len(urlArray))-1):
            if urlArray[x] not in urlArray[x+1]:
                Graph.add_edge(urlArray[x][:20]+'..',urlArray[x+1][:20]+'..')
        
        # Draw the graph with matplotlib
    nx.draw(Graph, with_labels=True,  node_size=0, style=':', linewidths=0, edge_color='gray', arrows=True, node_color="white", font_size=8, alpha=1)
    plt.savefig('testplot.png')
    # plt.show()

    # Image.open('testplot.png').save('testplot.jpg','JPEG')

        

    # Path to the image file


    # Print the image
    print_image("testplot.png")
    # start_session.configure(status='normal')
    






opening_string="            |`-.__     I CAME HERE \n" + "            / ' _/     FOR FUNNY   \n" + "           ****`       CAT VIDEOS, \n" + "          /    }       NOW I'M     \n" + "         /  \ /        WATCHING    \n" + "     \ /`   \\\        SOMEONE GET \n" + "      `\    /_\\       BLOWN UP    \n" + "       `~~~~~``~`                  \n" + 'The Alt-Right Pipeline is a vicious mechanism, manipulating people into reactionary, racist, anti-LGBTQ and misogynistic beliefs. They act through "dogwhistles", words that signify their allegiance to the Alt-Right, but would seem innocuous to those not in the know. Here, you can look through these fake Alt-Right accounts, made from thispersondoesnotexist.com and FAKER.py, and how the Alt-Right interacts with each other whilst the printer defines these dog whistles plus their roots. You can also print a map of the RW architecture you looked at to try and visualise this systemic radicalisation. Feel free to take your reciept if you want.\n \n TW: YOU ARE LIKELY TO COME ACROSS ANTI-LGBTQ+, RACIST AND XENOPHOBIC SPEECH\nFurthermore, my code is not perfect, It will see some dogwhistles that are not intended as dogwhistles, the aim of this project is not to make a perfect hate speech detector but rather to educate on what dogwhistles are and try to explore the Right Wing ecosystem online and how it is emboldened by Social Media algorithms to radicalise people to hateful beliefs.\n \n \n'





customtkinter.set_appearance_mode('dark')
window = customtkinter.CTk()
window.configure(fg_color='black')
window.title('WINDOW')
window.minsize(400,400)


header_label = customtkinter.CTkLabel(master=window, text=  "____________________________\n" +
                                                            "[            |`-.__     I CAME HERE        ]\n" +
                                                            "[            / '   _/     FOR FUNNY          ]\n" +
                                                            "[           ****`       CAT VIDEOS,         ]\n" +
                                                            "[          /      }       NOW I'M                 ]\n" +
                                                            "[         /    \ /        WATCHING            ]\n" +
                                                            "[     \ /`     \ \        SOMEONE GET    ]\n" +
                                                            "[      `\     /_ \       BLOWN UP            ]\n" +
                                                            "[__`~~~~~`~`_________________]\n", justify='left', font=('Helvetica',30), anchor='w')
header_label.pack(pady=20)

# photo_image = customtkinter.CTkImage(Image.open('BUTTON.jpg'))

start_session = customtkinter.CTkButton(
    master=window,
    text='START SESSION',
    command=button_press,
    hover=True,
    fg_color=('white'),
    text_color=('black'),
    hover_color=('gray')
    # image=photo_image
)


start_session.pack(pady=10)
im=Image.open('output.png')

my_image = customtkinter.CTkImage(light_image=Image.open('output.png'),
	dark_image=Image.open('output.png'),
    
	size=(int(im.size[0]/3),int(im.size[1]/3))) # WidthxHeight
my_label = customtkinter.CTkLabel(window, text="", image=my_image)
my_label.pack(pady=10)

window.mainloop()


    

