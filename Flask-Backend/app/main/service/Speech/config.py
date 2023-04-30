import azure.cognitiveservices.speech as speechsdk


class config:
    # token keys
    speech_key = "8fef2f6c1ac445369bf27c1ef31ed8b8"
    service_region = "eastus"

    # Set the voice we want to use
    voice_name = "en-US-JennyNeural"

    S3_PATH_TEXT = "speechaudio"
    S3_PATH_AUDIO = "speechaudio"



class inputs:
    speakers = {
        "Jen Jone",
        "Davis",
        "Tony",
        "Sara"
    }
    speakers_map = {
        "Jen Jone": "en-US-JennyNeural",
        "Davis": "en-US-DavisNeural",
        "Tony": "en-US-TonyNeural",
        "Sara": "en-US-SaraNeural"
    }
    length = [
        "1",
        "3",
        "5"
    ]
    tunes = [
        "Cheerful",
        "Friendly",
        "Hopeful",
        "Angry",
        "Sad",
        "Unfriendly"
    ]