from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_name_price(hotel_card):
    name = ""
    data = hotel_card.text.splitlines()
    for text in data:
        if text.startswith("€"):
            price = text.split("€")[-1]

        if not name:
            for t in text.split(" "):
                if t == "Hotel" or t == "Apartment" or t == "Resort" or t == "Residence":
                    name = text
                    break
    print(f"Location: {name} - Price: €{price}")

# Create a Chrome WebDriver instance using the WebDriver manager
driver = webdriver.Chrome()
action_chains = ActionChains(driver)
wait = WebDriverWait(driver, 10) 

url = "https://www.booking.com/"
driver.get(url)
driver.maximize_window()

destination = driver.find_element("id", ":re:")
destination.send_keys("Accra")
destination.send_keys(Keys.RETURN)

currency_button = driver.find_element(By.XPATH,'//span/button[@aria-label="Prices in United States Dollar"]')

currency_button.click()

time.sleep(2)
buttons = driver.find_elements(By.XPATH, '//button[@data-testid="selection-item"]')
for button in buttons:
    text = button.find_element(By.XPATH, './/span').text
    if "Euro" in text:
        button.click()  
        break


checkin_button = driver.find_element(By.XPATH, '//button[text()="Check-in date"]')
checkin_button.click()

time.sleep(2)

checkin_date = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@data-date="2023-10-04"]')))
checkin_date.click()


checkin_date = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@data-date="2023-10-10"]')))
checkin_date.click()

occupancy_button = driver.find_element(By.XPATH,'//button[contains(text(), "2 adults · 0 children · 1 room")]')
occupancy_button.click()

adult_increase_button = driver.find_element(By.XPATH, '//div[@class="f4878764f1"]/label[@for="group_adults"]')
adult_increase_button.click()
action_chains = ActionChains(driver)
action_chains.key_down(Keys.ARROW_UP).key_up(Keys.ARROW_UP).perform()

time.sleep(2)  # Sleep for 2 seconds

room_increase_button = driver.find_element(By.XPATH, "//div[@class='f4878764f1']/label[@class='a984a491d9' and @for='no_rooms']")
room_increase_button.click()
action_chains = ActionChains(driver)
action_chains.key_down(Keys.ARROW_UP).key_up(Keys.ARROW_UP).key_down(Keys.ENTER).perform()

sort_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='sorters-dropdown-trigger']")))
sort_button.click()

# Find the 'Price (lowest first)' button using its data-testid
class_price_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-id='class_and_price']")))
class_price_button.click()

time.sleep(5)
 # Increase timeout if needed
container = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='search_results_table']/div[2]/div/div/div[3]")))
# Once the container is present, find all hotel cards with data-testid="property-card"
hotel_cards = container.find_elements(By.XPATH, "//div[@data-testid='property-card']")

print("These are the top 5 hotels for your specifications: ")
print()
for hotel_card in hotel_cards[:5]:
    scrape_name_price(hotel_card)


# Do not close the browser window immediately, add a delay or input to keep it open
input("Press Enter to close the browser...")

# Close the browser window when you're ready
driver.quit()
