import os
import time
import re
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Get the base directory of the script
base_dir = os.path.dirname(os.path.abspath(__file__))

# Configure the download directory within the base directory
download_dir = os.path.join(base_dir, "downloads")

# Ensure the download directory exists
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

chrome_options = Options()
prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True
}
chrome_options.add_experimental_option("prefs", prefs)

# Debug: Print the download directory to verify
print(f"Download directory: {download_dir}")

# Set up the WebDriver (make sure the driver executable is in your PATH)
driver = webdriver.Chrome(options=chrome_options)

# Dictionary of company names
company_names = {
    1: "Reliance",
    2: "Tata Consultancy Services",
    3: "HDFC Bank Limited",
    4: "ICICI Bank Limited",
    5: "Bharti Airtel Limited"
}

# Dork query
dork = "csr doc filetype:pdf"

def sanitize_filename(filename):
    """Sanitize a string to be used as a safe filename."""
    filename = re.sub(r'\s+', '_', filename)  # Replace spaces with underscores
    filename = re.sub(r'[^a-zA-Z0-9_.-]', '', filename)  # Remove non-alphanumeric characters except -_. 
    return filename

def get_newest_file(directory):
    files = os.listdir(directory)
    paths = [os.path.join(directory, basename) for basename in files if basename.endswith('.pdf')]
    if not paths:
        return None
    return max(paths, key=os.path.getctime)

# Loop through each company name in the dictionary
for company_id, company_name in company_names.items():
    # Open Google
    driver.get("https://www.google.com")

    # Concatenate the company name with the dork
    search_query = f"{company_name} {dork}"

    # Find the search box using its name attribute value
    search_box = driver.find_element(By.NAME, "q")

    # Clear the search box if needed
    search_box.clear()

    # Enter the search query and send it
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.RETURN)

    # Wait for the results to load
    time.sleep(2)

    try:
        # Find the first search result link that points to a PDF
        first_pdf_result = driver.find_element(By.XPATH, '//a[contains(@href, ".pdf")]')
        first_pdf_result_url = first_pdf_result.get_attribute("href")

        # Debug: Print the first PDF result URL
        print(f"First PDF result URL for {company_name}: {first_pdf_result_url}")

        # Check if the URL is not None
        if first_pdf_result_url:
            # Extract the file name from the URL
            file_name = first_pdf_result_url.split("/")[-1]
            file_path = os.path.join(download_dir, file_name)

            # Check if the file already exists
            if not os.path.exists(file_path):
                # Get the current newest file before download
                before_download = get_newest_file(download_dir)
                
                # Click the first PDF result link
                first_pdf_result.click()

                # Wait for the page to load and initiate download if PDF
                time.sleep(10)  # Adjust this as needed for download completion

                # Get the new file after download
                after_download = get_newest_file(download_dir)

                if before_download != after_download:
                    sanitized_company_name = sanitize_filename(company_name)
                    new_file_path = os.path.join(download_dir, f"{sanitized_company_name}.pdf")
                    os.rename(after_download, new_file_path)
                    print(f"Renamed {after_download} to {new_file_path}")
                else:
                    print(f"No new file downloaded for {company_name}")

            else:
                print(f"File {file_name} already exists, skipping download.")
        else:
            print(f"No valid URL found for the first PDF result of {company_name}")

    except Exception as e:
        print(f"Error processing {company_name}: {e}")

    # Wait for a few seconds before the next iteration
    time.sleep(5)

# Close the browser
driver.quit()
