"""Web Scraping Task."""
import os

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium
from selenium.webdriver.support.ui import Select
from RPA.Excel.Files import Files
from RPA.HTTP import HTTP
from RPA.PDF import PDF
import csv
import re

browser = webdriver.Chrome(
    # ChromeDriver executable in Mac (download from https://chromedriver.chromium.org/downloads)
    executable_path="/Users/mac/Downloads/chromedriver"
    # windows in download folder
    # executable_path="C:\\Users\\gundo\\Downloads\\chromedriver.exe"
)

# Search
searchTerm = "Technology"


def openNewYorkTimes():
    '''Open the New York Times website.'''
    try:
        browser.get("https://www.nytimes.com/search")
        print("Page loaded")
        # browser.find_element(By.XPATH, value="//button[normalize-space()='Accept All']").click() //In case of cookies
    except selenium.common.exceptions.TimeoutException:
        print("Page load timeout")
    except selenium.common.exceptions.NoSuchElementException:
        print("No such element as 'searchTextField'")
    finally:
        print("New York Times opened")


def searchNews(searchPhrase):
    '''Search for a phrase on the New York Times website.'''
    try:
        print("Searching for: " + searchPhrase)
        browser.find_element(
            By.ID, value="searchTextField").send_keys(searchPhrase)
        browser.find_element(
            By.XPATH, value="//button[normalize-space()='Search']").click()
        # Handle some exceptions
    except selenium.common.exceptions.TimeoutException:
        print("Page load timeout")
    except selenium.common.exceptions.NoSuchElementException:
        print("No such element as 'searchTextField'")
    finally:
        print("Search Initiated")


def searchFilterTime():
    '''Filter the search results by time.'''
    try:
        print("Filtering results")
        # Click button with text "Refine results via Date Range"
        browser.find_element(
            By.XPATH, value="//button[normalize-space()='Refine results via Date Range']").click()
        # Click button with text "Past 24 hours"
        browser.find_element(
            # By.XPATH, value="//button[normalize-space()='Yesterday']").click()
            By.XPATH, value="//button[normalize-space()='Past Week']").click()
    except NoSuchElementException:
        print("No such element as 'Refine results via Date Range' or 'Yesterday'")
    finally:
        print("Filtering done")


def searchFilterSection():
    '''Filter the search results by section.'''
    try:
        print("Filtering results")
        # Click button with text "Refine results via Section"
        browser.find_element(
            By.XPATH, value="//button[normalize-space()='Refine results via Section']").click()
        browser.find_element(
            By.XPATH, value="//input[normalize-space()='Any']").click()
    except NoSuchElementException:
        print("No such element as 'Refine results via Section' or 'Any'")
    finally:
        print("Filtering done")


def paparazzi():
    '''Take a screenshot of the search results page.'''
    try:
        print("Taking a screenshot")
        os.makedirs("screenshot", exist_ok=True)
        browser.save_screenshot("screenshots/screenshot.png")
    except Exception as e:
        print("Error")
    finally:
        print("Done")


def numberOfNewsResult():
    '''Get the number of search results. 
    This function assumes that the search results page is already loaded.'''
    try:
        result_count_element = browser.find_element(By.XPATH,
                                                    value="//p[@data-testid='SearchForm-status']")
        result_count_text = result_count_element.text
        result_count = int(result_count_text.split(" ")[1].replace(",", ""))
        print("Search results:", result_count)
    except NoSuchElementException:
        print("No search results element found")
    finally:
        print("Done")


def initCSV():
    '''Create a CSV file to store the search results.'''
    try:
        if not os.path.isfile('news.csv'):
            with open('news.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Title", "Date", "Description",
                                "Picture filename", "Phrase count", "Money"])
                print("CSV file created")
        else:
            print("CSV file already exists")
    except Exception as e:
        print(e)
        print("Error in creating CSV file")
    finally:
        print("Done")


def storeToExcel(title, description):
    '''Store the search results to an Excel file.'''
    try:
        result = []
        result.append(title)
        result.append("date")
        result.append(description)
        result.append("picture")
        result.append(countNumberOfOccurence(title, description, searchTerm))
        result.append(has_money("description"))

        with open('news.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(result)
            print("Stored to CSV")
    except:
        print("Error in storing to CSV")
    finally:
        print("Done")


def getNews():
    '''Get the search results and store them to an Excel file.'''
    try:
        # Find the li element by its test ID
        search_results = browser.find_element(
            By.XPATH, '//ol[@data-testid="search-results"]')

        # Loop over each list element in the ol
        for result in search_results.find_elements(By.XPATH, './li[@data-testid="search-bodega-result"]'):
            # Extract the title and description from the a element
            title = result.find_element(By.XPATH, './div//a/h4').text
            description = result.find_element(By.XPATH, './div//a/p[1]').text
            # date = result.find_element(By.XPATH, './div//a/p[2]').text
            try:
                # Find the image element
                image_element = result.find_element(
                    By.XPATH, './li//a/span/img')

                # Extract the image URL
                image_url = image_element.get_attribute("src")

                # Download the image
                response = requests.get(image_url)
                image_file = io.BytesIO(response.content)
                image = Image.open(image_file).convert("RGB")

                # Save the image to disk
                image.save("images/" + title + ".jpg", "JPEG", quality=85)
            except NoSuchElementException:
                print(NoSuchElementException)
            finally:
                print(
                    "Warning::Could not find the suggested element in the page that is being read at the moment")

            print(title, "Title")
            print(description, "Description")
            # print(date, "Date")

            try:
                storeToExcel(title, description)
            except:
                print("Error Trying to store to excel")

    except NoSuchElementException:
        print("No search results element found")

    finally:
        print("Completed getting news")
        return


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


def nyCrawler():
    ''' Main Runner '''
    # initExcel()
    initCSV()
    openNewYorkTimes()
    paparazzi()
    searchNews(searchTerm)
    searchFilterSection()
    searchFilterTime()
    getNews()
    numberOfNewsResult()

    browser.quit()


if __name__ == "__main__":
    nyCrawler()
