from RPA.HTTP import HTTP
from RPA.Browser.Selenium import Selenium
from RPA.FileSystem import FileSystem
from RPA.Excel.Files import Files
from RPA.Tables import Tables
from RPA.Browser.Selenium import By
import os
import re
import csv

browser = Selenium()

searchTerm = "Artificial"
url = "https://www.nytimes.com/search"


def openNewYorkTimes():
    try:
        browser.open_available_browser(url)
        print("Page loaded")
    except Exception as e:
        print("Page load timeout")
    except Exception as e:
        print("No such element as 'searchTextField'")
    finally:
        print("New York Times opened")


def searchNews(searchPhrase):
    try:
        print("Searching for: " + searchPhrase)
        browser.input_text("searchTextField", searchPhrase)
        browser.click_button("Search")
    except Exception as e:
        print("Page load timeout")
    except Exception as e:
        print("No such element as 'searchTextField'")
    finally:
        print("Search Initiated")


def searchFilterTime():
    try:
        print("Filtering results")
        browser.click_button("Refine results via Date Range")
        browser.click_button("Past Week")
    except Exception as e:
        print("Page load timeout")
    except Exception as e:
        print("No such element as 'searchTextField'")
    finally:
        print("Search Initiated")


def searchFilterSection():
    try:
        print("Filtering results")
        browser.click_button("Refine results via Section")
        browser.click_button("World")
    except Exception as e:
        print("Page load timeout")
    except Exception as e:
        print("No such element as 'searchTextField'")
    finally:
        print("Search Initiated")


def paparazzi():
    try:
        print("Taking a screenshot")
        searchScreenShot = browser.find_element(
            By.XPATH, '//ol[@data-testid="search-results"]')
        browser.save_screenshot(
            filename=f"{os.getcwd()}/output/sales_summary.png",
            elemena=searchScreenShot)
    except Exception as e:
        print("Page load timeout")
    except Exception as e:
        print("No such element as 'searchTextField'")
    finally:
        print("Screenshot taken")


def countNumberOfOccurence(title, description, phrase):
    ''' Combines the title and description into one string and counts how many times the phrase appears in the string. '''
    count = 0
    try:
        text = title + " " + description
        count = text.count(phrase)
    except Exception as e:
        print(e)
        print("Error in counting number of occurence")
    finally:
        print("Done")
    return count


def has_money(text):
    """
    Checks if the given text contains any amount of money.

    Possible formats: $11.1 | $111,111.11 | 11 dollars | 11 USD

    Returns:
    - True if the text contains any amount of money.
    - False otherwise.
    """
    try:
        # Check if the text contains a dollar sign followed by a number with optional decimal points and commas.
        if re.search(r'\$\d{1,3}(,\d{3})*(\.\d+)?', text):
            return True

        # Check if the text contains a number followed by the word 'dollars'.
        if re.search(r'\d+ dollars?', text):
            return True

        # Check if the text contains a number followed by 'USD'.
        if re.search(r'\d+ USD', text):
            return True
    except Exception as e:
        print(e)
        print("Error in checking if text contains money")
    finally:
        print("Search for money done")

    return False


def downloadImage(url, filename):
    ''' Downloads the image from the given url and saves it as the given filename. '''
    try:
        connector = HTTP()
        theImage = "output/" + filename
        connector.download(url, theImage, overwrite=True)
        return theImage
    except Exception as e:
        print("Page load timeout")
    except Exception as e:
        print("No such element as 'searchTextField'")
    finally:
        print("Image downloaded and saved as " + theImage)


def loadWorkBook():
    ''' Initializes the CSV file. '''
    headers = ["Title", "Date", "Description",
               "Picture filename", "Phrase count", "Money"]

    try:
        # Create CSV File And Write Table Headers
        with open("output/news.csv", "w") as file:
            file.write(",".join(headers) + "\n")
            print("Created CSV file and wrote headers \n")
    except Exception as e:
        print(e)
        print("Error in loading workbook")
    finally:
        print("Done loading workbook")


def storeToExcel(title, description, date, picture, phrase_count, money):
    '''Store the search results to an Excel file.'''
    print("Storing to Excel", title, description,
          date, picture, phrase_count, money)
    try:
        result = []
        result.append(title)
        result.append(date)
        result.append(description)
        result.append(picture)
        result.append(phrase_count)
        result.append(money)

        with open('output/news.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(result)
            print("Stored to CSV")
    except:
        print("Error in storing to CSV")
    finally:
        print("Done")


def getNews():
    try:
        print("Getting news")
        news = browser.get_webelement("//ol[@data-testid='search-results']")
        for newsResult in news.find_elements(By.XPATH, './li[@data-testid="search-bodega-result"]'):

            title = newsResult.find_element(By.XPATH, './div//a/h4').text

            description = newsResult.find_element(
                By.XPATH, './div//a/p[1]').text
            date = newsResult.find_element(
                By.CSS_SELECTOR, 'span[data-testid="todays-date"]').text
            try:
                image = newsResult.find_element(By.CSS_SELECTOR, 'img[src]')
                image_url = image.get_attribute('src')
                le = title.lower()
                le = re.sub(r'[^\w\s]', '', le)
                le = re.sub(r'\s+', '-', le)

                fileLocation = le + ".jpg"
                pathToImage = downloadImage(image_url, fileLocation)
            except Exception as e:
                print(e)
            finally:
                print("Done with image \n")

            try:

                storeToExcel(title, description, date, pathToImage,
                             countNumberOfOccurence(title, description, searchTerm), has_money(description))

            except Exception as e:
                print(e)

    except Exception as e:
        print(e)
        print("Error in getting news \n")
    finally:
        print("Done with news \n")


def numberOfNewsResult():
    try:

        print("Getting number of news results")
        totalNewsResult = browser.get_webelement(
            "//p[@data-testid='SearchForm-status']")

        # print("Total number of news results: " + totalNewsResult.text)
        result_count_text = totalNewsResult.text
        result_count = int(result_count_text.split(" ")[1].replace(",", ""))
        print("Search results:", result_count)

    except Exception as e:
        print(e)
        print("Error in getting number of news results \n")
    finally:
        print("Done with number of news results")


def cleanUp():
    ''' Deletes the image files. '''
    try:
        print("Cleaning up")
        for file in os.listdir("output"):
            if file.endswith(".jpg"):
                os.remove(os.path.join("output", file))
    except Exception as e:
        print(e)
        print("Error in cleaning up")
    finally:
        print("Done cleaning up")


def nyCrawler():
    try:
        loadWorkBook()
        openNewYorkTimes()
        searchNews(searchTerm)
        searchFilterSection()
        searchFilterTime()
        getNews()
        # paparazzi()
        # numberOfNewsResult()
        # cleanUp()
    except Exception as e:
        print(e)
        print("Error in NY Crawler")
    finally:
        browser.close_browser()
        print("Browser closed")


if __name__ == "__main__":
    nyCrawler()
