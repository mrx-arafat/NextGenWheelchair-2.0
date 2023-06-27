import speech_recognition as sr
# sr.Microphone.list_microphone_names()
# sr.Microphone.list_working_microphones()

listening = True

while listening:
    with sr.Microphone(device_index=1) as source:
        recognizer = sr.Recognizer()
        recognizer.adjust_for_ambient_noise(source)
        recognizer.dynamic_energy_threshold = 1000

        try:
            print("Listening....")
            audio = recognizer.listen(source, timeout=1.5)
            response = recognizer.recognize_google(audio)
            print("Recognized: " + response)
            # print(response)

        except sr.UnknownValueError:
            print("Didn't recognize that.")