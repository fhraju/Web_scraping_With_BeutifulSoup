from selenium import webdriver
from bs4 import BeautifulSoup
import time

# Logging in to linkedin account
driver = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe")
# Opening linkedin login page
driver.get("https://linkedin.com/uas/login")
time.sleep(5)

user_name = driver.find_element_by_id("username")
user_name.send_keys("hamidulislam51593@gmail.com")
password = driver.find_element_by_id("password")
password.send_keys("159375")
# Clicking in the logging button
driver.find_element_by_xpath("//button[@type='submit']").click()

# Opening someones profiles
profile_url = "https://www.linkedin.com/in/kunalshah1/"
driver.get(profile_url) # Opening the profile

## Code block for Scrolling to the bottom
start = time.time()
# will be used in the while loop
initial_scroll = 0
final_scroll = 1000

while True:
    # This command scrolls the window from the scroll value i set
    driver.execute_script(f"window.scrollTo({initial_scroll},{final_scroll})")
    initial_scroll = final_scroll
    final_scroll += 1000

    # Stoping the script for data load
    time.sleep(3)
    end = time.time()

    # We will scroll for 20 seconds
    if round(end - start) > 20:
        break


## Extracting Data from the Profile
src_code = driver.page_source
soup = BeautifulSoup(src_code, 'lxml')
    
# Extracting profile introduction:
# Extracting the HTML of the complete introduction box
intro = soup.find('div',{'class': 'pv-text-details__left-panel'})

# Extracting the name
name_loc = intro.find('h1')
name = name_loc.get_text().strip() # strip is used for removing any extra blank space

# Extracting the Company Name
work_at_loc = intro.find('div', {'class': 'text-body-medium break-words'}) # html tag for company name
works_at = work_at_loc.get_text().strip()

# Extracting the location
location_loc = intro.find_next('div', {'class': 'pb2 pv-text-details__left-panel'}) # html
location = location_loc.get_text().strip()

print("Name ------>", name,
    "\nWorks At ---->", works_at,
    "\nLocation ---->", location)

# Extracting data from the experience sections
experience = soup.find('div', {'id': 'pvs-list__outer-container'}).find('ul')
print(experience)