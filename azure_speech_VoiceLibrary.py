#Library for Voice Profile Presets


#Class for basic Voice Profiles
class vProfile():
    def __init__(self, name, voiceSetting, pitchSetting):
        self.name= name
        self.voiceSetting = voiceSetting
        self.pitchSetting = pitchSetting


#list of created profiles
Neuro = vProfile('Neuro', 'en-US-AshleyNeural', '+1.25st')
Aria = vProfile('Aria', 'en-US-AriaNeural', '+0st')


#Array to hold the multiple profiles
voiceLibrary = [Neuro, Aria]