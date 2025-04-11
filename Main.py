from tkinter import *
from tkinter.ttk import *
import speech_recognition as sr
from google_trans_new import google_translator
import pyttsx3
from gtts import gTTS
import os
from datetime import datetime

languages={"English":"en","Telugu":"te",
           "Hindi":"hi","Tamil":"ta",
           "Kannada":"kn","Malayalam":"ml"
            }

master = Tk()

title = Label(master, text = "Speech Project",font= ("Helvetica 20"), justify= CENTER)
l1 = Label(master, text = "Source Language:",font= ("Helvetica 16"))
l2 = Label(master, text = "Destination Language:",font= ("Helvetica 16"))
l3 = Label(master, text = "Click on Speak Now Button",font= ("Helvetica 16"), justify= CENTER)
src = Combobox(master)
dest = Combobox(master)

t1 = Text(master, height = 20, width = 52)

lang=list(languages.keys())
src['values']=lang
src.set(lang[0])

dest['values']=lang
dest.set(lang[2])


style = Style()


def trans(msg,in_lang,out_lang):
    from googletrans import Translator
    
    translator = Translator()
    translate_text_1 = translator.translate(msg, src=in_lang, dest=in_lang)
    print(translate_text_1.text)

    translate_text = translator.translate(msg, src=in_lang, dest=out_lang)
    print(translate_text.text)

    final_msg = "{} ({})\n".format(translate_text_1.text,translate_text.text)
    t1.insert(END,final_msg)
    print("END")

    date_string = datetime.now().strftime("%d%m%Y%H%M%S")
    fname="voices/Voice_"+date_string+".mp3"
    myobj = gTTS(text=translate_text.text, lang=out_lang, slow=False)
    myobj.save(fname)

    from playsound import playsound
    playsound(fname)
    
    
    print(translate_text)
    

    
    
def recog():
    recognizer=sr.Recognizer()
    engine = pyttsx3.init()
    global l3
    with sr.Microphone() as source:
        
        print('Clearing background noise...')
        
        recognizer.adjust_for_ambient_noise(source,duration=0)
        print('Waiting for message..')
        
        
        audio = recognizer.listen(source,timeout=8)
        l3["text"] = 'Recording Completed..'
        print('Done recording..')
        
    try:
        print('Recognizing..')
        result = recognizer.recognize_google(audio)
        print("Message:",result)
        print("Destination Language:",dest.get())
        trans(result,languages[src.get()],languages[dest.get()])
        
    except Exception as ex:
        print(ex)

def swap():
    a=src.get()
    b=dest.get()
    src.set(b)
    dest.set(a)


style.configure('big.TButton', font=("Helvetica", 20), foreground="blue4")

b2 = Button(master,text=u"\u21c5",command=swap, width=2, style="big.TButton")

b1 = Button(master,text="Speak Now",command=recog, style="big.TButton")




title.grid(row = 0, column = 0, pady = 2,columnspan = 2)
l1.grid(row = 1, column = 0, sticky = W, pady = 2)
l2.grid(row = 2, column = 0, sticky = W, pady = 2)

src.grid(row = 1, column = 1, pady = 2)
dest.grid(row = 2, column = 1, pady = 2)

b2.grid(row = 1, column = 2, pady = 2,rowspan=2)

b1.grid(row = 3, column = 1, pady = 2)

l3.grid(row = 4, column = 0, pady = 2,columnspan=2)

t1.grid(row = 5, column = 0, pady = 2,columnspan = 2)



master.geometry('500x550')
mainloop()
