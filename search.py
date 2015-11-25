import urllib2, google, bs4, re

def getAnswer(query):
    """
    Finds the answer to a given question.

    Args:
        query: A string representing the question to answer.

    Returns:
        The answer to the question as a string.
    """
    if query[:4].lower() == "who ":
        return findWho(query)
    elif query[:5].lower() == "when ":
        return findWhen(query)
    else:
        return "Unable to find answer"

def getRaw(query):
    """
    Gets the raw text from webpages that answer a question.

    Args:
        query: A string representing the question to answer.

    Returns:
        The text from webpages that answer the question as a string.
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

def findWho(query):
    """
    Finds the answer to a given "who" question.

    Args:
        query: A string representing the question to answer.

    Returns:
        The answer to the question as a string.
    """
    raw = getRaw(query)
    names = re.findall("[A-Z][a-z]+ [A-Z][a-z]+", raw)
    print names
    return ""

def findWhen(query):
    """
    Finds the answer to a given "when" question.

    Args:
        query: A string representing the question to answer.

    Returns:
        The answer to the question as a string.
    """
    raw = getRaw(query)
    return ""
