#Adaugarea package-urilor
import nltk
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import json
import random
import sys

path = './'
fileName='database'

#Deschidere fisierului de tip json pentru extragerea si utilizarea datelor
dataset = json.loads(open('database.json').read())

#Functia care permite scrierea in fisier
def writeToJSONFile(data,fileName="database.json"):
    with open(fileName,'w') as fp:
        json.dump(data,fp, indent = 4)



#Prelucrarea datelor din fisierul json si generarea raspunsurilor
def append_topics(dataset):

    i = 0
    y = []
    for x in dataset['intents']:
        y.append(dataset['intents'][i]['tag'])
        i = i+1
    return y


# Functie care stocheaza intr-un array raspunsurile corespunzatoare index-ului unui anume tag
def append_responses(index):
    y = []
    for x in dataset['intents'][index]['responses']:
        y.append(x)
    return y


# Functie care verifica daca o anume propozitie poate fi incadrata intr-un tag si care retuneaza True daca acest lucru este posibil, respectiv False, in caz contrar
def topic(prop):

    a = []
    z = prop.split()
    topics = append_topics(dataset)
    for i in z:
        for j in topics:
            if i == j:
                return True
    return False

#Completare a functiei topic(prop), definita anterior ,care returneaza si topicul ,in situatia in care propozitia preluata ca input poate fi incadrata intr-un astfel de tag
def get_topic(prop):
    if(topic(prop) == True):

        a = []
        z = prop.split()
        topics = append_topics(dataset)
        for i in z:
            for j in topics:
                if i == j:
                    return i
                    break


# Functie responsabila pentru returnarea unei valori numerice, reprezentand numarul curent al valorii extrase din sir(index):
def get_index(prop):
    ind = 0
    a = get_topic(prop)
    b = append_topics(dataset)
    for i in b:
        if i == a:
            return ind
        else:
            ind = ind+1


#Functie care verifica daca propozitia curenta se poate incadra intr-un anume topic, si care returnaza un raspuns aleatoriu, pe baza topicului,dar si a indexului acestuia
def get_response(prop):
    if (topic(prop) == False):
        print('Unable to find this sentence in the dataset!')
    else:
        index = get_index(prop)
        resp = append_responses(index)
        x=random.choice(resp)
        return x


listener = sr.Recognizer()
engine = pyttsx3.init()

#Setarea vocii chatbot-ului;
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

#Functie care permite chatbot-ului sa vorbeasca
def talk(text):
    engine.say(text)
    engine.runAndWait()

#Utilizarea 'text-to-speech' pentru a face chatbot-ul sa pronunte urmatorul string
print('Hi, i\'m your chatbot Bella. What can i do for you?')
talk('Hi, i\'m your chatbot Bella. What can i do for you?')

#Functie care preia input-ul de la utilizator
def take_command():
    #Un 'try except' este folosit pentru detectarea posibilelor erori ce pot aparea cu microfonul
    try:
        with sr.Microphone() as source:
            print('listening...')
            #Utilizarea microfonului pentru a detecta input-ul dumneavoastra
            voice = listener.listen(source, 10,3.5)
            #Executarea convertirii 'speech-to-text' utilizand Google API
            command = listener.recognize_google(voice)
            #Transformarea inputului in minuscule
            command = command.lower()
            if 'bella' in command:
                # Scoatem numele chatbotului din string
                command = command.replace('bella', '')
                #Afisarea inputului ca si text in terminal daca exista numele chatbotului in input
                print(command)
    except:
        #programul nu executa nimic in cazul unei exceptii
        pass
    return command

#Runtime-ul programului
def run_bella():
    #Rularea functiei urmatoare
    command = take_command()
    print(command)
    if 'play' in command:
        #Scoaterea cuvantului 'play' din string
        song = command.replace('play', '')
        talk('playing ' + song)
        print('playing...')
        #Accesarea youtube-ului si pornirea melodiei
        pywhatkit.playonyt(song, use_api=True)
        sys.exit()
    elif 'time' in command:
        #Determinarea orei in momentul actual
        time = datetime.datetime.now().strftime('%H:%M')
        print('The time is ' + time)
        talk('The time is ' + time)
    elif 'search for' in command:
        search = command.replace('search for','')
        #Cautarea pe wikipedia pentru topic-ul ales
        info = wikipedia.summary(search,1)
        print(info)
        talk(info)
    elif 'joke' in command:
        #Generarea automata a glumei
        joke=pyjokes.get_joke()
        print(joke)
        talk(joke)
    elif 'exit' in command:
        #Incheierea programului
        sys.exit()
    elif topic(command)==True:
        #Aflam daca inputul contine un tag din fisierul json
        x=command
        #Extragem aleator unul din raspunsurile specifice tag-urilor
        answer=get_response(command)
        print(answer)
        talk(answer)
        if x=='goodbye':
            sys.exit()
    else:
        print('I dont think i have that question in my database. Would you like to help me remember this question?(YES/NO)')
        talk('I dont think i have that question in my database. Would you like to help me remember this question?')
        response = take_command()
        if response=='yes':
            print('Great! Could you give me a keyword that sums up this question?')
            talk('Great! Could you give me a keyword that sums up this question?')
            #Determinarea tag-ului nou
            word=take_command()
            print(word)
            print('Lovely. Now could i get an answer to your question?')
            talk('Lovely. Now could i get an answer to your question?')
            #Determinarea raspunsului nou
            answer=take_command()
            print(answer)
            with open ("database.json") as json_file:
                data=json.load(json_file)
                temp=data["intents"]
                y={"tag":""+word,"responses":[""+answer+""]}
                #Scrierea in fisier a datelor noi
                temp.append(y)
            writeToJSONFile(data)
            print('Operation Successful. I have added everything to my database. Do you have anymore questions?')
            talk('Operation Successful. I have added everything to my database. Do you have anymore questions?')
            question=take_command()
            if question=='no':
                print('Have a nice day!')
                talk('Have a nice day!')
                sys.exit()
        else:
            print('No problem.')
            talk('No problem.')

while True:
    run_bella()