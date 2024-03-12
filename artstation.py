# Import necessary modules
from undetected_chromedriver import Chrome
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
import time
import csv

# Initialize Chrome WebDriver
chrome = Chrome()

# Open the file containing the links to scrape
with open("D:\Work\Coding\Web Scraping\Selenium\Artsation\links.text", "r") as file:
    links = [line.strip() for line in file]

# Open CSV file to write results
csv_file = open("results.csv", "w", encoding="utf-8")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["name", "location", "contacts", "email", "summary", "link"])

# Iterate through each link
for link in links:

    # Open the link in Chrome
    chrome.get(link)
    time.sleep(5)  # Wait for the page to load

    # Try to find name
    try:
        name = chrome.find_element(By.XPATH, "/html/body/div[2]/app-root/profile-layout/div[1]/div[2]/profile-sidebar/ng-scrollbar/div/div/div/div/div/div[1]/h1").text
    except NoSuchElementException:
        name = "N/A"  # If not found, set to "N/A"

    # Try to find location
    try:
        location = chrome.find_element(By.XPATH, "/html/body/div[2]/app-root/profile-layout/div[1]/div[2]/profile-sidebar/ng-scrollbar/div/div/div/div/div/div[2]/ul/li[1]/span").text
    except NoSuchElementException:
        location = "N/A"  # If not found, set to "N/A"

    # Try to find contacts
    try:
        contacts = []
        contacts_list = chrome.find_elements(By.XPATH, "//social-links/ul/li/a")
        for contact in contacts_list:
            contacts.append(contact.get_attribute("href"))
        contacts = list(set(contacts))
    except NoSuchElementException:
        contacts = "N/A"  # If not found, set to "N/A"

    # Try to find email
    try:
        time.sleep(1)
        button = chrome.find_element(By.XPATH, "/html/body/div[2]/app-root/profile-layout/div[1]/div[1]/resume-page/div/div[4]/div/div/public-email/div/button")
        chrome.execute_script("arguments[0].click();", button)
        time.sleep(5)
        email = chrome.find_element(By.XPATH, "/html/body/div[2]/app-root/profile-layout/div[1]/div[1]/resume-page/div/div[4]/div/div/public-email/div/span").text
    except (NoSuchElementException, ElementClickInterceptedException):
        email = "N/A"  # If not found or unable to click, set to "N/A"

    # Try to find summary
    try:
        summary = chrome.find_element(By.XPATH, "/html/body/div[2]/app-root/profile-layout/div[1]/div[1]/resume-page/div/div[2]/div").text.replace("\n", " ")
    except NoSuchElementException:
        summary = "N/A"  # If not found, set to "N/A"

    # Write data to CSV
    csv_writer.writerow([name, location, contacts, email, summary, link])

# Close the Chrome WebDriver
chrome.quit()
