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
    dates = getDates(raw)
    answer = mostCommon(dates)
    if answer.find("/") != -1:
        answer = convert(answer)
    return answer

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

def getDates(text):
    """
    Gets a list of dates from a block of text.

    Args:
        text: The text to find the dates from as a string.

    Returns:
        A list of dates in various date formats.

    >>> getDates("January 1, 2015 something January 01, 2015 something December 31, 2015")
    ['January 1, 2015', 'January 01, 2015', 'December 31, 2015']
    >>> getDates("1/1/2015 something 01/01/2015 something 12/31/2015")
    ['1/1/2015', '01/01/2015', '12/31/2015']
    """
    exp = "((January|February|March|April|May|June|July|August|September|October|November|December) ([0-2]?[0-9]|3[01]), [0-9]+)"
    result = re.findall(exp, text)
    dates = []
    for r in result:
        dates.append(r[0])
    exp = "(((1[0-2])|(0?[1-9]))\/(3[01]|([0-2]?[0-9]))\/[0-9]+)"
    result = re.findall(exp, text)
    for r in result:
        dates.append(r[0])
    return dates

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

def convert(date):
    """
    Converts a date from mm/dd/yyyy format to month dd, yyyy format.

    Args:
        date: The date to convert as a string.

    Returns:
        The converted date as a string.
    """
    month = date[:date.find("/")]
    date = date[date.find("/") + 1:]
    day = date[:date.find("/")]
    year = date[date.find("/") + 1:]
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    return months[int(month) - 1] + " " + str(int(day)) + ", " + year
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
