# Import the required library
import pyttsx3
#import objc
# If have error: NameError: name 'objc' is not defined etc.:
# https://stackoverflow.com/questions/77197398/error-running-pyttsx3-code-on-os-x-nameerror-name-objc-is-not-defined

# Create a function for text to speech conversion
def text_to_speech(text):
    # Initialize the Text-to-Speech engine
    engine = pyttsx3.init("nsss")

    # Set the properties for the speech output
    engine.setProperty('rate', 150)  # Speed of the speech (words per minute)
    engine.setProperty('volume', 0.8)  # Volume (0.0 to 1.0)

    # Convert the text to speech
    engine.say(text)
    engine.runAndWait()

# Get input from the user
input_text = input("Enter the text to convert to speech: ")

# Call the text_to_speech function with the input text
text_to_speech(input_text)

# Output success message
print("Speech generated successfully!")