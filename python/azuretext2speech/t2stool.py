import time
import json
import argparse
import re
import pathlib

try:
    import azure.cognitiveservices.speech as speechsdk
except ImportError:
    print("""
    Importing the Speech SDK for Python failed.
    Please install it first
    $ pip install azure-cognitiveservices-speech

    """)
    import sys
    sys.exit(1)

default_language = 'en-US'


#read env param from command line options
parser = argparse.ArgumentParser(description='text to English speech, from a file')

parser.add_argument('-f', '--file', metavar='filename', required=True,
                    dest='filename', help='text file to be transformed to speech, sentence seperated by dot')
parser.add_argument('-k', '--key', metavar='subscriptionkey', required=True,
                    dest='subkey', help='azure subscription key')
parser.add_argument('-r', '--region', metavar='azure region', required=False,
                    dest='region', help='azure host region, default eastus', default='eastus')
parser.add_argument('-p', '--voiceprofile', metavar='voice profile', required=False,
                    dest='voiceprofile', help='voice profile, default en-US-ChristopherNeural', default='en-US-ChristopherNeural')

args = parser.parse_args()

input_file = args.filename
speech_key = args.subkey 
service_region = args.region 
voice_profile = args.voiceprofile


def speech_synthesis_to_file(input_text: str, output_file_name: str, language: str = 'en-US'):
    """performs speech synthesis with input_text, and output to the file"""
    # Creates an instance of a speech config with specified subscription key and service region.
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    # Sets the synthesis language.
    # The full list of supported languages can be found here:
    # https://docs.microsoft.com/azure/cognitive-services/speech-service/language-support#text-to-speech
    speech_config.speech_synthesis_language = language
    # specify the profile of voice
    speech_config.speech_synthesis_voice_name=voice_profile
    # specify the output filename, format can be mp3 or wav
    file_config = speechsdk.audio.AudioOutputConfig(filename=output_file_name)
    # Creates a speech synthesizer for the specified language,
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=file_config)


    # Receives a text from param and synthesizes it to speaker.
    
    result = speech_synthesizer.speak_text_async(input_text).get()
    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized to speaker for text [{}] with language [{}]".format(input_text, language))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

def generate_speech_from_file(input_file: str, output_filename_prefix: str = None):
    sentence_no = 0
    if not output_filename_prefix:
        filename = pathlib.Path(input_file).name
        filenamepure = filename.split('.')[0]
        output_filename_prefix = filenamepure
    with open(input_file, 'r') as f:
        for line in f.readlines():
            sentences = re.split('(?<=[.!?]) +', line)
            for sentence in sentences:
                sentence_no += 1
                output_filename = output_filename_prefix+'_'+str(sentence_no)+'_'+sentence.strip('.?!').rstrip().replace(' ','_')+'.wav'
                speech_synthesis_to_file(sentence, output_filename)


if __name__ == '__main__':
    generate_speech_from_file(input_file)
