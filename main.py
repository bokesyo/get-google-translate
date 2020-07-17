from selenium import webdriver
import pandas as pd
import time
import requests


def get_info(oral_url):
    browser = webdriver.Chrome()
    browser.get(oral_url)
    a = browser.find_element_by_class_name("res-tts")
    a.click()
    time.sleep(10)

    tar = browser.find_element_by_class_name("tlid-translation.translation")
    tar_text = tar.text

    pronounce = browser.find_element_by_class_name(
        "tlid-result-transliteration-container.result-transliteration-container.transliteration-container")
    pron_b = pronounce.find_element_by_class_name("tlid-transliteration-content.transliteration-content.full")
    pron_text = pron_b.get_attribute('innerHTML')

    browser.execute_script(
        "a = performance.getEntries(); for (i in a)"
        "{ if (a[i].initiatorType == 'audio'){ document.title = a[i].name; break;}}")
    this_url = browser.title
    browser.close()
    # print(this_url)

    return this_url, tar_text, pron_text


def download_file(url, filename):
    res = requests.get(url)
    res.raise_for_status()

    filename = 'AudioData/' + filename + '.mp3'
    down_file = open(filename, 'wb')

    for chunk in res.iter_content(100000):
        down_file.write(chunk)

    down_file.close()

    return


lang_list = ["zh-CN", "ar", "ko", "pt", "ru", "ja", "de", "fr", "en", "es"]
express_list = ["Hello!", "Bye!", "Thanks!", "You are welcome.", "Good!", "Sorry!"]
general = "https://translate.google.cn/#view=home&op=translate"


lang_result = []
audio_result = []

for lang in lang_list:

    express_result = []

    audio_data = []

    ethnic = lang

    express_result.append(ethnic)
    audio_data.append(ethnic)

    ct = 1
    for express in express_list:

        # Specify a the url for a word given target language
        specify = general + "&sl=" + "en" + "&tl=" + lang + "&text=" + express
        audio_file = ethnic + '_' + str(ct) + '.mp3'

        result = get_info(specify)
        audio = result[0]
        word = result[1]
        pron = result[2]

        # Export csv file
        express_result.append(word)
        express_result.append(pron)
        express_result.append(audio_file)

        # For downloading audio files
        audio_data.append(audio)
        download_file(audio, audio_file)

        ct += 1

    lang_result.append(express_result)
    audio_result.append(audio_data)

    print(lang_result)
    print(audio_data)


names = ["lang", "Express1", "Pron1", "Audio1", "Express2", "Pron2", "Audio2", "Express3", "Pron3", "Audio3",
         "Express4", "Pron4", "Audio4", "Express5", "Pron5", "Audio5", "Express6", "Pron6", "Audio6"]

test = pd.DataFrame(columns=names, data=lang_result)

test.to_csv("result.csv")
