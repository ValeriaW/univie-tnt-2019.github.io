from bs4 import BeautifulSoup
import re
import os

newPathToFolder = "Users/valeriawidler/Documents/TNT/Lesson13/"
source = "/Users/valeriawidler/Documents/XMLCode/"
listOfFiles = os.listdir(os.path.expanduser(source))

# function with one argument filter to define a specific date which will use values of the dispatch only if the date is true
def generate(filter):

    placeNames = []
    dicFreq = {}
    resultsCSV = []

    # for loop to access all files
    for f in listOfFiles:
        soup = BeautifulSoup (open(source+f, "r"), features="html.parser")
        # searches for list items of "date" and return maximum two elemens
        issue_date = soup.find_all("date", limit=2)[1] # only returns the second match
        issue_date = issue_date.get("value")
        # searches for all tags with "div3" and stores it in variable "articles"
        articles = soup.find_all("div3", type = True)
        if issue_date.startswith(filter):
            for a, item in enumerate(articles):
                counter = str(a) + "-" + str(issue_date)                        # for loop that counts each article and combines it wit the date in the dispatch
                places = item.find_all("placename", key = True)                 # continues to find all placenames with an attribute
                article = "article-" + counter                                  # variable that holds the issue date of the dispatch a string and an article counter
                print(article)
                for a, item in enumerate(places):
                    counter2 = str(a) + "-" + counter                           # counter2 will be the unique identifier ID for each row
                    place = item.get_text()                                     # for loop to retrieve all placenames as value from the placename tag
                    key = item["key"].split(";")                                # variable that holds the tgn number
                    print(str(place))

                    for k in key:
                        key = [d for d in k if d.isdigit()]                     # for loop to clean tgn numbers digits only
                        tag_id = ''.join(key)
                        placeList = "\t".join([counter2,issue_date,article,place,tag_id])        # creating a variable that holds each result article, place, tag_id
                        placeNames.append(placeList)                            # appending the variable to a list

    for i in placeNames:                                                        # creating a frequency with a for loop for all placenames
        if i in dicFreq:
            dicFreq[i] += 1
        else:
            dicFreq[i]  = 1

    for key, value in dicFreq.items():                                          # removes all placenames that are mention once only
        if value < 2: # this will exclude items with frequency higher than 1 - we want unique rows
            newVal = "%09d\t%s" % (value, key)
            # newVal will looks like: `000005486 TAB Richmond`
            resultsCSV.append(newVal)

    resultsCSV = sorted(resultsCSV, reverse=True)                               # sorting the results variable
    print(len(resultsCSV)) # will print out the number of items in the list
    resultsToSave = "\n".join(resultsCSV)                                       # joining the results line by line

    # creates a new file in a target folder with name + article counter + name + issue_date + txt file
    newfile = newPathToFolder  + "placesFull_3.3.csv"
    # creating a header for the final file
    header = "freq\tid\tdate\tsource\ttarget\ttgn\n"
    # opens the newfile and writes each article into a sperate file
    with open(newfile, "w", encoding="utf8") as f8:
        f8.write(header+"".join(resultsToSave))

# how to use the function
generate("1860-11")