"""Web Scraping Task."""
# INSTRUCTIONS
# You must have 3 configured variables (you can save them in the configuration file, but it is better to put them to the Robocorp Cloud work items):

# - search phrase
# - news category or section
# - number of months for which you need to receive news

#     > Example of how this should work: 0 or 1 - only the current month, 2 - current and previous month, 3 - current and two previous months, and so on
#     >

# The main steps:

# 1. Open the site by following the link
# 2. Enter a phrase in the search field
# 3. On the result page, apply the following filters:
#     - select a news category or section
#     - choose the latest news
# 4. Get the values: title, date, and description.
# 5. Store in an excel file:
#     - title
#     - date
#     - description (if available)
#     - picture filename
#     - count of search phrases in the title and description
#     - True or False, depending on whether the title or description contains any amount of money

#         > Possible formats: $11.1 | $111,111.11 | 11 dollars | 11 USD
#         >
# 6. Download the news picture and specify the file name in the excel file
# 7. Follow the steps 4-6 for all news that fall within the required time period

# Specifically, we will be looking for the following in your submission:

# 1. Quality code
# Your code is clean, maintainable, and well-architected. The use of an object-oriented model is preferred.
# 2. Resiliency
# Your architecture is fault-tolerant and can handle failures both at the application level and website level.
# 3. Best practices
# Your implementation follows best RPA practices.
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

browser = webdriver.Chrome(
    # ChromeDriver executable path (download from https://chromedriver.chromium.org/downloads)
    executable_path="/Users/mac/Downloads/chromedriver"
    # windows in download folder
    # executable_path="C:\\Users\\gundo\\Downloads\\chromedriver.exe"
)


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


def getNews():
    # Set the regular expression to match the date label
    date_regex = r"^[A-Z][a-z]{2}\. \d{1,2}$"

    # Find all the span elements with an aria-label attribute
    all_spans = browser.find_elements(By.XPATH, "//span[@aria-label]")

    # Loop through the span elements and find the one with the matching label   search-results
    date_element = None
    for span in all_spans:
        label = span.get_attribute("aria-label")
        if re.match(date_regex, label):
            date_element = span
            break

    # Get the text of the element
    if date_element is not None:
        date = date_element.text
        print(date)  # Output: Feb. 22
    else:
        print("No matching date found")


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


def getNews():
    try:
        # Find the search results container
        results_container = browser.find_element(By.XPATH,
                                                 value="//ol[@data-testid='search-results']")

        # Find all the search result items
        results_items = results_container.find_elements(By.XPATH,
                                                        value=".//li[@data-testid='search-bodega-result']")

        # Loop through each search result item
        for result_item in results_items:
            # Extract the title
            title_element = result_item.find_element(By.XPATH, value=".//h4")
            title = title_element.text

            # Extract the date
            date_element = result_item.find_element(By.XPATH,
                                                    value=".//span[@data-testid='todays-date']")
            date = date_element.text

            # Extract the description
            description_element = result_item.find_element(
                by="xpath", value=".//p")
            description = description_element.text

            # Check if the description is long enough to be the article description
            if len(description) > 50:
                # Check if the description contains a currency symbol
                if '$' in description:
                    print("Article title:", title)
                    print("Article date:", date)
                    print("Article description:", description)
                    print("Article contains currency symbol")
                else:
                    print("Article title:", title)
                    print("Article date:", date)
                    print("Article description:", description)
                    print("Article does not contain currency symbol")
    except NoSuchElementException:
        print("No search results element found")


def nyCrawler():
    openNewYorkTimes()
    paparazzi()
    searchNews("Nasa")
    searchFilterTime()
    searchFilterSection()
    # getNews()
    numberOfNewsResult()


if __name__ == "__main__":
    nyCrawler()
