import webbrowser
from youtube_search import YoutubeSearch


def youtube(what):
    '''search what on youtube, for steaming
    Args:
        what (str): what to search for
    '''
    while True:
        result = YoutubeSearch(what, max_results=10).to_dict()
        if result:
            break
    url = 'https://www.youtube.com' + result[0]['url_suffix']
    webbrowser.open(url)
    return True
