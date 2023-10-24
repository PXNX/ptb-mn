import os
import shutil

from dotenv import load_dotenv
from orjson import orjson

from util.helper import sanitize_hashtag

load_dotenv()

from data.lang import languages, GERMAN
from util.translation import translate


def split_to_json():
    output_directory = '../res/countries/'
    if os.path.isdir(output_directory):
        shutil.rmtree(output_directory)
    os.mkdir(output_directory)

    input_languages = [GERMAN] + languages
    for lang in input_languages:
        input_filename = f"flag_{lang.lang_key}.json"

        with open(input_filename, 'rb') as input_file:
            print(input_filename, lang.lang_key)
            content = orjson.loads(input_file.read())

        for flag_key, hashtag in content.items():
            print(flag_key, hashtag)
            output_filename = f"{output_directory}{flag_key}.json"

            text = ""

            if lang.lang_key == GERMAN.lang_key:
                text += f"{{\"{lang.lang_key}\":\"{sanitize_hashtag(lang.lang_key, hashtag)}\""
            else:
                text += f",\"{lang.lang_key}\":\"{sanitize_hashtag(lang.lang_key, hashtag)}\""

            if lang.lang_key == languages[-1].lang_key:
                text += "}"

            with open(output_filename, 'a', encoding="utf-8") as output_file:
                output_file.write(text)


def translate_json():
    filename = f"flag_de.json"

    with open(filename, 'rb') as f:
        content = orjson.loads(f.read())
        print(content)

        for lang in languages:
            with open(f"flag_{lang.lang_key}.json", 'w') as f:

                text = ""

                first = True

                for flag_key, country_name in content.items():

                    hashtag = translate(lang.lang_key, country_name, lang.lang_key_deepl)
                    print("-- translated hashtag:: ", hashtag)

                    if first:
                        text += f"{{\"{flag_key}\":\"{hashtag}\""
                        first = False
                        continue

                    text += f",\"{flag_key}\":\"{hashtag}\""

                text += "}"
                f.write(text)


if __name__ == "__main__":
    # translate_json()
    split_to_json()
