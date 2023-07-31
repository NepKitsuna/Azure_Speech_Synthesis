import os
import azure.cognitiveservices.speech as speechsdk

# This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
#audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=False, , device_name='AI Voice') 

# The language of the voice that speaks.
voiceSetting = 'en-US-AshleyNeural'
#pitch for the voice
pitchSetting = '+1.25st'

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

while True:
    # Get text from the console and synthesize to the default speaker.
    print("Enter some text that you want to speak >")
    text = input()

    if text == 'Debug Exit':
        break

    # Here's where you define the pitch. The "+0st" is the change in pitch. You can adjust this value to your needs.
    ssml_string = f"""
    <speak version='1.0' xmlns='https://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
        <voice name= '{voiceSetting}'>
            <prosody pitch = '{pitchSetting}'>
                {text}
            </prosody>
        </voice>
    </speak>
    """

    #This should utilize the ssml_string instead of just grabbing the inputted text
    speech_synthesis_result = speech_synthesizer.speak_ssml_async(ssml_string).get()

    #speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")