from flask import Flask, render_template, request, jsonify, send_file
from googletrans import Translator
import speech_recognition as sr
from gtts import gTTS
from langdetect import detect
import os
import time

app = Flask(__name__)

# Complete list of languages
LANGUAGES = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'he': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'or': 'odia',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'ug': 'uyghur',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu'
}

@app.route('/')
def index():
    return render_template('index.html', languages=LANGUAGES)

@app.route('/translate', methods=['POST'])
def translate():
    input_language = request.form['input_language']
    target_language = request.form['target_language']

    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        
        try:
            print("Listening...")
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("Recognizing...")
            text = r.recognize_google(audio, language=input_language)
            print(f"Recognized text: {text}")

            detected_language = detect(text)
            print(f"Detected language: {detected_language}")

            translator = Translator()
            translation = translator.translate(text, src=detected_language, dest=target_language)
            translated_text = translation.text
            print(f"Translated text ({target_language}): {translated_text}")

            timestamp = int(time.time())
            audio_filename = f"static/translated_audio_{timestamp}.mp3"
            
            tts = gTTS(text=translated_text, lang=target_language)
            tts.save(audio_filename)

            # Write original and translated text to a file
            with open('translations.txt', 'a', encoding='utf-8') as f:
                f.write(f"Original ({detected_language}): {text}\n")
                f.write(f"Translated ({target_language}): {translated_text}\n\n")

            return jsonify({
                'original_text': text,
                'detected_language': detected_language,
                'translated_text': translated_text,
                'audio_file': audio_filename
            })

        except sr.WaitTimeoutError:
            return jsonify({'error': 'Listening timed out while waiting for phrase to start, please try again.'}), 400
        except sr.UnknownValueError:
            return jsonify({'error': 'Speech recognition failed. Please try again.'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/audio/<filename>')
def get_audio(filename):
    return send_file(os.path.join('static', filename))

if __name__ == "__main__":
    app.run(debug=True)
