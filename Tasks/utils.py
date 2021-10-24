from google_trans_new import google_translator as Translator
import re
import googlesearch
import webbrowser


def get_expression(text):
    '''extract slot and value form string of text with regex
    Args:
        text ([str]): ex: let play the <song:B-object_type> <Hello:B-track> <aldele:I-track> for me
    Returns:
        dict: dict["B-object_type"] = song ,...
    '''
    pair = {}
    for slot_and_value in re.findall("<(.+?)>", text):
        value, slot = slot_and_value.split(":")
        pair[slot] = value
    return pair
    pass


def gg_search(key, max_results=5):
    """to use google to search about something
    Args:
        key (str): keyword for searching
        max_results (int, optional): number of result to display. Defaults to 5.
    Raises:
        Exception: [description]
    Returns:
        list: list of link to search result
    """
    try:
        for i, url in enumerate(
                googlesearch.search(key,
                                    num=max_results,
                                    stop=max_results,
                                    pause=1)):
            print(f"{i + 1}-> {url}")
            webbrowser.open(str(url))
        return True
    except Exception as e:
        raise e


def convert_languages(txt, src='auto', dest='en'):
    """to convert between languages
    Args:
        txt (str): text string need to convert
        src (str, optional): source language. Defaults to 'vi'.
        dest (str, optional): destination language. Defaults to 'en'.
    Raises:
        Exception: [description]
    Returns:
        str: string after convert if able
    """
    script = txt
    try:
        translator = Translator()
        script = translator.translate(txt, lang_tgt=dest, lang_src=src)
        # script = translator.translate(txt)
        # script = script.text
        print(script)
    except Exception as e:
        print(e)
    return script
