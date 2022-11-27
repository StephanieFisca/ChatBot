# ChatBot
This is a Chatbot i made using Python as a company project.
The chatbot utilises the microphone to take the users input, otherwise known as the speech recognition. Afterwards, the text-to-speech library's fucntions are used in order to decypher the users speech into words.

The bot is named Bella, and she is able to execute multiple commands, such as:
1. Playing a youtube video
2. Telling you the current time
3. Searching for a despired topic on the internet
4. Telling you a joke
5. Answering to a restricted set of questions. By utilizing a json file to store possible questions and answers, Bella will choose one of the inputed possible answers if a question from the json file is asked.

If Bella doesnt understand a command, she will ask you to repeat the question.
If you would like to teach bella how to respond to a given question, Bella takes the users inputed data and writes to the json file where all questions and answers are stored.



