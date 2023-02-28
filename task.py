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
    # ChromeDriver executable path (download from https://chromedriver.chromium.org/downloads)
    executable_path="/Users/mac/Downloads/chromedriver"
    # windows in download folder
    # executable_path="C:\\Users\\gundo\\Downloads\\chromedriver.exe"
)

searchTerm = "South Africa"


def openNewYorkTimes():
    try:
        browser.get("https://www.nytimes.com/search")
        print("Page loaded")
        # browser.find_element(By.XPATH, value="//button[normalize-space()='Accept All']").click() //In case of cookies
    except selenium.common.exceptions.TimeoutException:
        print("Page load timeout")


def searchNews(searchPhrase):
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


def searchFilterTime():
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


def searchFilterSection():
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


# def getNews():
#     # Set the regular expression to match the date label
#     date_regex = r"^[A-Z][a-z]{2}\. \d{1,2}$"

#     # Find all the span elements with an aria-label attribute
#     all_spans = browser.find_elements(By.XPATH, "//span[@aria-label]")

#     # Loop through the span elements and find the one with the matching label   search-results
#     date_element = None
#     for span in all_spans:
#         label = span.get_attribute("aria-label")
#         if re.match(date_regex, label):
#             date_element = span
#             break

#     # Get the text of the element
#     if date_element is not None:
#         date = date_element.text
#         print(date)  # Output: Feb. 22
#     else:
#         print("No matching date found")


def paparazzi():
    try:
        print("Taking a screenshot")
        os.makedirs("screenshot", exist_ok=True)
        browser.save_screenshot("screenshots/screenshot.png")
    except:
        print("Error")


def numberOfNewsResult():
    try:
        # Find the element that contains the search result count
        result_count_element = browser.find_element(By.XPATH,
                                                    value="//p[@data-testid='SearchForm-status']")

        # Extract the search result count from the element's text content
        result_count_text = result_count_element.text
        result_count = int(result_count_text.split(" ")[1].replace(",", ""))

        # Print the search result count
        print("Search results:", result_count)
    except NoSuchElementException:
        print("No search results element found")
    finally:
        print("Done")


def initCSV():
    try:
        if not os.path.isfile('news.csv'):
            with open('news.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Title", "Date", "Description",
                                "Picture filename", "Phrase count", "Money"])
                print("CSV file created")
        else:
            print("CSV file already exists")
    except:
        print("Error in creating CSV file")
        # Create a new Excel file


# def initExcel():
#     try:
#         if not os.path.isfile('news.xlsx'):
#             excel = Files()
#             excel.create_workbook("news.xlsx")
#             excel.create_worksheet("Sheet1")
#             excel.save_workbook()
#             excel.close_workbook()
#             print("Excel file created")
#         else:
#             print("Excel file already exists")
#     except:
#         print("Error in creating Excel file")


def storeToExcel(title, description):
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


def getNews():
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
        print("Done")
        return


def countNumberOfOccurence(title, description, phrase):
    # combine the title and description into one string
    text = title + " " + description

    # use the count method to count how many times the phrase appears
    count = text.count(phrase)

    return count


def has_money(text):
    """
    Checks if the given text contains any amount of money.

    Possible formats: $11.1 | $111,111.11 | 11 dollars | 11 USD

    Returns:
    - True if the text contains any amount of money.
    - False otherwise.
    """
    # Check if the text contains a dollar sign followed by a number with optional decimal points and commas.
    if re.search(r'\$\d{1,3}(,\d{3})*(\.\d+)?', text):
        return True

    # Check if the text contains a number followed by the word 'dollars'.
    if re.search(r'\d+ dollars?', text):
        return True

    # Check if the text contains a number followed by 'USD'.
    if re.search(r'\d+ USD', text):
        return True

    return False
# NY Times Crawler


def nyCrawler():
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
