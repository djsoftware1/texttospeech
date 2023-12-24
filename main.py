# Import the required library
import pyttsx3
import sys
#import objc
# If have error: NameError: name 'objc' is not defined etc.:
# https://stackoverflow.com/questions/77197398/error-running-pyttsx3-code-on-os-x-nameerror-name-objc-is-not-defined

engine = None

# Create a function for text to speech conversion
def text_to_speech(text, use_voice, lang=''):
    # Initialize the Text-to-Speech engine
    #engine = pyttsx3.init("nsss")
    # "supports three TTS engines"
    #sapi5 – SAPI5 on Windows
    #nsss – NSSpeechSynthesizer on Mac OS X
    #espeak – eSpeak on every other platform
    global engine
    if not engine:
        engine = pyttsx3.init("nsss")

    # Set the properties for the speech output
    engine.setProperty('rate', 150)  # Speed of the speech (words per minute)
    engine.setProperty('volume', 0.8)  # Volume (0.0 to 1.0)
    # Randomize a voice
    # 1 Italiian
    # 3 French
    # 4 German
    # 5 Hebrew
    # 10 En-scotland
    # Get list of voices
    voices = engine.getProperty('voices')
    if use_voice>=0 and use_voice<len(voices):
        print(f"Selecting voice {use_voice}")
        engine.setProperty('voice', voices[use_voice].id)
    elif lang!='':
        print(f"Selecting language {lang}")
        #engine.setProperty('voice', lang)
        # Try select by language code, though note there can be more than one language with that language code, so let's default to the first we find, later we can add maybe more options, or else user can use -v= to override:
        # Get list of voices
        #voices = engine.getProperty('voices')
        for voice in voices:
            if voice.languages:
                for l in voice.languages:
                    if l.lower().startswith(lang.lower()):
                        print(f"Selecting voice by language: {l}")
                        engine.setProperty('voice', voice.id)
                        break

    #engine.setProperty('voice', 1)

    # Convert the text to speech
    engine.say(text)
    engine.runAndWait()

# Check if a file passed as argument
# If yes, read the file and convert the text to speech
# If no, get input from the user and convert the text to speech
if __name__ == "__main__":
    print("Text to Speech")
    print("Parameters:")
    print("Pass --list as argument to list all the available voices")
    print("-t=TEXT to say")
    print("-v=VOICE to use (number starting from 0 up to number of voices, use --list to see them all)")
    print("--lang=LANGUAGE (or-l=language code) to use (en, it, fr, fr_FR, fr_CA, de, he, en-scotland)")

    lang=''
    use_voice=-1 # -1 use default
    say_text=''
    
    # Check if --list is passed as argument
    if len(sys.argv) > 1:
        for arg in sys.argv:
            #print(arg)
            if arg == "--list":
                #global engine
                engine = pyttsx3.init("nsss")
                # Get a list of voices and display them
                voices = engine.getProperty('voices')
                # For each voice, print the voice and its ID
                count=0
                for voice in voices:
                    print(f"{count} {voice.__dict__}")
                    count+=1
            # If starts with "--lang=", set the language
            elif arg.startswith("--lang=") or arg.startswith("-l="):
                lang = arg.split("=")[1]
                #engine.setProperty('voice', lang)
                print(f"Language set to {lang}")
            elif arg.startswith("-v="):
                # Convert from string to int
                use_voice = int(arg.split("=")[1])
                print(f"Voice {use_voice} selected")
            elif arg.startswith("-t="):
                # Convert from string to int
                say_text = arg.split("=")[1]
                print(f"Text to say: {say_text}")

    # Get input from the user
    do_exit = False
    while not do_exit:
        if say_text:
            input_text = say_text
            say_text = ''
        else:
            input_text = input("Enter the text to convert to speech (or /exit or Ctrl+C to exit): ")
        if input_text=="/quit" or input_text == "/exit" or input_text == "/bye":
            do_exit = True
            break

        # Call the text_to_speech function with the input text
        text_to_speech(input_text, use_voice, lang)

    print("Bye")
    #print("Speech generated successfully!"