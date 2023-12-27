import pyttsx3
import threading
import queue

class CSound:
    def __init__(self):
        self.speech_queue = queue.Queue()
        self.thread = threading.Thread(target=self.tts_thread, daemon=True)
        self.engine_initialized = False

    def tts_thread(self):
        self.engine = pyttsx3.init("nsss")
        self.engine_initialized = True

        #debug#print("start loop")
        while True:
            #debug#print("WAITING FOR TEXT")
            text, use_voice, lang = self.speech_queue.get()
            #debug#print(f"Got text: {text}")
            if text is None:
                break  # None is the signal to stop

            # Voice and language setup...

            self.engine.setProperty('rate', 150)  # Speed of the speech (words per minute)
            self.engine.setProperty('volume', 0.8)  # Volume (0.0 to 1.0)
            # Randomize a voice
            # 1 Italiian
            # 3 French
            # 4 German
            # 5 Hebrew
            # 10 En-scotland
            # Get list of voices
            voices = self.engine.getProperty('voices')
            if use_voice>=0 and use_voice<len(voices):
                print(f"Selecting voice {use_voice}")
                self.engine.setProperty('voice', voices[use_voice].id)
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
                                self.engine.setProperty('voice', voice.id)
                                break


            # Something not 100% right here
            # It does start saying the next thing if done, but if still speaking, it does stop speaking correctly but doesn't start the next thing
            # I think using callbacks may help but for now let's use it like this

            #debug#print("SAY NEW")
            self.engine.say(text)
            #debug#print("RUNANDWAIT NEW")
            # We should ideally probably use something like an 'interrupt_speech' variable to signal the engine to stop speaking, but for now we'll just stop the loop and start a new one
            if self.engine._inLoop:
                #debug#print("RUNANDWAIT NEW INLOOP")
                self.engine.endLoop()
            #else:
            self.engine.runAndWait()
            #debug#print("RUNANDWAIT NEW DONE")
            #time.sleep(1)

    def Init(self):
        self.thread.start()

    def text_to_speech(self, text, use_voice=-1, lang=''):
        if not self.engine_initialized:
            raise RuntimeError("Engine not initialized. Call Init() first.")

        self.speech_queue.put((text, use_voice, lang))

    def Cleanup(self):
        # Signal the TTS thread to stop and wait for it
        self.speech_queue.put((None, None, None))
        self.thread.join()

# Usage example
if __name__ == "__main__":
    sound = CSound()
    sound.Init()
    sound.text_to_speech("Hello, this is a test.")
    sound.Cleanup()
