#Warning: All code is running on a mac machine with an m1 chip, and has not been tested for applicability to other operating systems.

To install all the dependencies in requirments.txt, you can run the command pip install -r requirments.txt.


Run the txt_generater.py file to generate the sentences. You can get the sample text file with the command python txt_generater.py with the name "sample.txt". You can also specify the name of the output text file with python txt_generater.py -n "your name". The output text will be kept in the current directory.

Run tts.py to convert the sentences to speech. You can generate a sample voice with the command python tts.py (which reads "yes, prime minister."). You can type the string you want to use directly with the -t command, e.g. python tts.py -t "yes, prime minister. You can also specify a text file with the -f command to make the program generate speech by line, e.g. python tts.py -f "test.txt". The generated .wav file will be stored in the voice_output folder.
