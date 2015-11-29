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
    names = getNames(raw)
    return mostCommon(names)

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

def getNames(text):
    """
    Gets a list of names from a block of text.

    Args:
        text: The text to find the names from as a string.

    Returns:
        A list of names.

    >>> getNames("John Smith something John John Smith")
    ['John Smith', 'John John Smith']
    >>> getNames("Mr. John Smith something Mr.John Smith something Mrs. John Smith")
    ['Mr. John Smith', 'John Smith', 'Mrs. John Smith']
    >>> getNames("John Smith-smith something John Smith-Smith")
    ['John Smith', 'John Smith-Smith']
    >>> getNames("A. B. Smith something John A. Smith something John A. B. Smith")
    ['A. B. Smith', 'John A. Smith', 'John A. B. Smith']
    """
    exp = "(((Dr.|Mr.|Mrs.|Ms.) )?((([A-Z][a-z]+ )+([A-Z]. )*)|([A-Z]. )+)[A-Z][a-z]+(\-[A-Z][a-z]+)?)"
    result = re.findall(exp, text)
    names = []
    for r in result:
        names.append(r[0])
    return names

def mostCommon(L):
    """
    Returns the most common element in a list.

    Args:
        L: The list.

    Returns:
        The most common element.
    """
    count = {}
    maxCount = 0
    maxItem = None
    for item in L:
        if count.has_key(item):
            count[item] += 1
        else:
            count[item] = 1
        if count[item] > maxCount:
            maxCount = count[item]
            maxItem = item
    return maxItem
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
