import urllib2, google, bs4, re

def getAnswer(query):
    """
    Finds the answer to a qiven question.

    Args:
        query: A string representing the question to answer.

    Returns:
        The answer to the question as a string.
    """
    r = google.search(query, num = 10, start = 0, stop = 10)
    raw = ""
    for result in r:
        try:
            u = urllib2.urlopen(result)
            page = u.read()
            soup = bs4.BeautifulSoup(page, "html")
            raw += soup.get_text()
        except:
            pass
    return raw
