import os
import azure.cognitiveservices.speech as speechsdk
import azure_speech_VoiceLibrary as library
#Hunter
# This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
#Selection for default input and output
audio_output_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
audio_input_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
speech_config.speech_recognition_language="en-US"
# Trying to set the output to a virtual audio cable
#audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=False, , device_name='AI Voice') 

# # The language of the voice that speaks.
# voiceSetting = 'en-US-AshleyNeural'
# #pitch for the voice
# pitchSetting = '+1.25st'

voiceProfile = library.Neuro()

speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input_config)
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output_config)

# Saying the text
def speaktext(text):
    ssml_string = f"""
    <speak version='1.0' xmlns='https://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
        <voice name= '{voiceProfile.voiceSetting}'>
            <prosody pitch = '{voiceProfile.pitchSetting}'>
                {text}
            </prosody>
        </voice>
    </speak>
    """

    #printing the text for a transcript
    print(text) 
    #This should utilize the ssml_string instead of just grabbing the inputted text (Ragland)
    speech_synthesis_result = speech_synthesizer.speak_ssml_async(ssml_string).get()
    

    #Debug error checks
    # if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    #     print("Speech synthesized for text [{}]".format(text))
    if speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")



#print('Ready? y or n')
#start = input()
while True:
    #if start == 'y':

        #DEBUG: Checking beginning of program tic
        #print("start")

        # Print for indication the script has started and Input is active
        print("Speak into your microphone.")
        speech_recognition_result = speech_recognizer.recognize_once_async().get()

        if "SYSTEM CALL" in speech_recognition_result.text.upper():
            if "STOP PROCESS" in speech_recognition_result.text.upper() or "STOP APPLICATION" in speech_recognition_result.text.upper():
                print(speech_recognition_result.text)
                speaktext("Understood, Stopping application.")
                break
            elif "SET VOICE" in speech_recognition_result.text.upper():
                #Check for the voice spoken if it exists in the library
                for i in range(len(library.voiceLibrary)):
                    if library.voiceLibrary[i] in speech_recognition_result.text.upper():
                        speaktext("Changing voice to profile " + library.voiceLibrary[i] + ".")
                        
                        #voiceProfile = 
                #TODO Trying to set voices via voice command 
                #speaktext("No voice profile found")
                continue

        
        #Save the text from microphone for processing 
        text = speech_recognition_result.text

        # # Debug: Checking to make sure everything went through correctly
        # if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        #     print("Recognized: {}".format(speech_recognition_result.text))
        # elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        #     print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
        # elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        #     cancellation_details = speech_recognition_result.cancellation_details
        #     print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        #     if cancellation_details.reason == speechsdk.CancellationReason.Error:
        #         print("Error details: {}".format(cancellation_details.error_details))
        #         print("Did you set the speech resource key and region values?")
    

        # Get text from the console and synthesize to the default speaker.
        # text input method (Hunter/Nep)
        # print("Enter some text that you want to speak >")
        #text - input()


        #Old Debug check
        # if text == 'Debug Exit':
        #     break

        speaktext(text)

    #else:
    #    break

print('Code Breach (End of Code Stream)')