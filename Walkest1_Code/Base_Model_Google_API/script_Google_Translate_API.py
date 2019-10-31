#!/usr/bin/env python3

import io
import os
import argparse

# Imports the Google Cloud client library
from google.cloud import translate

# Instantiates a client
translate_client = translate.Client()

parser = argparse.ArgumentParser(description='Uploads and gets provided text file to/from Google translate API')
parser.add_argument('input', help="Text file, with one sentence per line")
args = parser.parse_args()

translated_file = os.path.dirname(args.input) + "/" + os.path.splitext(os.path.basename(args.input))[0] + "_translated.txt"
text = args.input



with open(translated_file, 'w') as newFile, open(text, 'r') as inputText:
    for i, line in enumerate(inputText):

        # Translates some text
        translation = translate_client.translate(line, target_language='fr')  # 'de' for German, 'fr' for French

        print("-------")
        print(u"Text {}: {}".format(i, line))
        print(u"Translation: {}".format(translation['translatedText']))
        print("-------")

        newFile.writelines(translation['translatedText'] + "\n")

    print("\n%s Lines were sent to Google for translation\n" % i)

