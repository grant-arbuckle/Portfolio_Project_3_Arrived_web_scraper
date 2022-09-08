from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import datetime
from IPython.core.display import HTML

url = "https://arrivedhomes.com/app/properties"
PATH = "/Users/grantarbuckle/chromedriver"

driver = webdriver.Chrome(PATH)
# driver.maximize_window()
driver.get(url)

# Filter by vacation rentals
driver.find_element(By.XPATH, "//div[text()='Vacation Rentals']").click()
vaca_properties_search=driver.find_elements(By.TAG_NAME, "a")

# Create list of only vacation rental property hyperlinks
vaca_hyperlink_list = []
for i in vaca_properties_search:
    hyperlink = i.get_attribute("href")
    if hyperlink[0:36] == "https://arrivedhomes.com/properties/":
        vaca_hyperlink_list.append(hyperlink)

# Remove property filters
driver.find_element(By.XPATH, "//div[text()='All']").click()
# driver.find_element(By.XPATH, "//span[text()='Filters']").click()
# driver.find_element(By.XPATH, "//span[text()='For Sale']").click()
all_properties_search=driver.find_elements(By.TAG_NAME, "a")

# Create list of non-vacation rental property hyperlinks
non_vaca_rental_list = []
for i in all_properties_search:
    hyperlink = i.get_attribute("href")
    if hyperlink[0:36] == "https://arrivedhomes.com/properties/":
        non_vaca_rental_list.append(hyperlink)

# List comprehension to remove vaca rentals from all properties list
non_vaca_rental_list = [x for x in non_vaca_rental_list if x not in vaca_hyperlink_list]

# Read in existing data
# property_data = pd.read_excel("/Users/grantarbuckle/Desktop/Data Analytics/Datasets/Arrived Homes - All Data.xlsx")

# Create dataframe for property data
property_data = pd.DataFrame(columns= [
    "Name", "Property Details", "Purchase Price", "Percent Funded", "Share $ Avail.", "Investors", "Mo. Rent", "Rent Ready Date", "Address", "Rental Status", "Div Date", "1st Div Yield",
    "Ann. Equity Return", "Ann. Div Yield", "Hypoth. Ann. Return", "Ttl Prop. Amt", "Ttl Shares", "Prop. Leverage", "Timestamp", "IPO Shareprice", "AirDNA Market Grade" #, "Description"
])

complete_count = 0

for i in vaca_hyperlink_list:
    driver.get(i)
    time.sleep(4.7) # Increase time if "Stale Element" error message occurs
    prop_name = driver.find_element(By.XPATH, "//h3[@data-e2e='property-details-header-property-name']").text
    property_data = property_data.append({
        'Name': prop_name
        ,'Property Details': (driver.find_element(By.XPATH, "//span[@class='MuiTypography-root MuiTypography-stats1Medium css-yjnp7i']").text)
        ,'Purchase Price': (driver.find_elements(By.XPATH, "//span[@class='MuiTypography-root MuiTypography-stats1Bold css-18c84du']")[1].text)
        ,"Rent Ready Date": (driver.find_elements(By.XPATH, "//span[@class='MuiTypography-root MuiTypography-stats1Bold css-18c84du']")[2].text)
        ,'Investors': (driver.find_elements(By.XPATH, "//span[@class='MuiTypography-root MuiTypography-stats1Bold css-18c84du']")[0].text)
        ,'Share $ Avail.': (driver.find_element(By.XPATH, "//h3[@class='MuiTypography-root MuiTypography-h3 property-monetary-availability-info-money css-npc00f']").text)
        ,"Percent Funded": (driver.find_element(By.XPATH, "//h5[@class='MuiTypography-root MuiTypography-h5 css-zkf7tm']").text)
        ,'Address': (driver.find_element(By.XPATH, "//*[contains(text(),'Address:')]").text)
        ,'Ann. Equity Return': (driver.find_elements(By.XPATH, "//span[@class='percentage emphasize']")[0].text)
        ,'Ann. Div Yield': (driver.find_elements(By.XPATH, "//span[@class='percentage emphasize']")[1].text)
        ,'Hypoth. Ann. Return': (driver.find_elements(By.XPATH, "//span[@class='percentage emphasize']")[2].text)
        ,'Ttl Prop. Amt': (driver.find_element(By.XPATH, "//div[@class='MuiTypography-root MuiTypography-body1Subheader css-quexwl']").text)
        ,'IPO Shareprice': (driver.find_elements(By.XPATH, "//div[@class='MuiTypography-root MuiTypography-body1Subheader css-sbao0b']")[4].text)        
        ,'Ttl Shares': (driver.find_elements(By.XPATH, "//div[@class='MuiTypography-root MuiTypography-body1Subheader css-sbao0b']")[5].text)        
        ,'Prop. Leverage': (driver.find_element(By.XPATH, "//span[@class='MuiTypography-root MuiTypography-stats1Bold percent css-18c84du']").text)
        ,'AirDNA Market Grade': (driver.find_element(By.XPATH, "//img[contains(@src, 'https://cdn.arrivedhomes.com/images/strContent/airdna-grade')]").get_attribute("src"))
        ,'Timestamp': datetime.datetime.now()
        # ,'Description': (driver.find_element(By.XPATH, "//div[@class='MuiTypography-root MuiTypography-body2 css-7w8k4p']").text)
    }, ignore_index=True)

    # Div Date only available if you are a shareholder of the property and logged in on the webdriver Chrome session
    try:
        property_data.loc[property_data.Name == prop_name, 'Div Date'] = driver.find_element(By.XPATH, "//span[@class='MuiTypography-root MuiTypography-body2 css-1hog4co']").text
    except:
        property_data.loc[property_data.Name == prop_name, 'Div Date'] = ''

    # Track progress of data collection
    complete_count += 1
    print(f"Listings scraped count: {complete_count}   Property scraped: {prop_name}")

property_data.to_excel("/Users/grantarbuckle/Desktop/Data Analytics/Datasets/Arrived Homes - Vaca Rentals Only.xlsx", engine='xlsxwriter')

# Append data to dataframe for non vacation rental properties
for i in non_vaca_rental_list:
    driver.get(i)
    time.sleep(1.5) # Increase time if "Stale Element" error message occurs
    prop_name = driver.find_element(By.XPATH, "//h3[@data-e2e='property-details-header-property-name']").text
    property_data = property_data.append({
        'Name': prop_name
        ,'Property Details': (driver.find_element(By.XPATH, "//span[@class='MuiTypography-root MuiTypography-stats1Medium css-yjnp7i']").text)
        ,'Purchase Price': (driver.find_elements(By.XPATH, "//span[@class='MuiTypography-root MuiTypography-stats1Bold css-18c84du']")[1].text)
        ,'Mo. Rent': (driver.find_elements(By.XPATH, "//span[@class='MuiTypography-root MuiTypography-stats1Bold css-18c84du']")[2].text)
        ,'Investors': (driver.find_elements(By.XPATH, "//span[@class='MuiTypography-root MuiTypography-stats1Bold css-18c84du']")[0].text)
        ,'Share $ Avail.': (driver.find_element(By.XPATH, "//h3[@class='MuiTypography-root MuiTypography-h3 property-monetary-availability-info-money css-npc00f']").text)
        ,"Percent Funded": (driver.find_element(By.XPATH, "//h5[@class='MuiTypography-root MuiTypography-h5 css-zkf7tm']").text)
        ,'Address': (driver.find_element(By.XPATH, "//*[contains(text(),'Address:')]").text)
        ,'Rental Status': (driver.find_elements(By.XPATH, "//span[@class='MuiTypography-root MuiTypography-stats1Bold css-18c84du']")[3].text)
        ,'Div Date': (driver.find_elements(By.XPATH, "//span[@class='MuiTypography-root MuiTypography-stats1Bold css-18c84du']")[4].text)
        ,'1st Div Yield': (driver.find_elements(By.XPATH, "//span[@class='MuiTypography-root MuiTypography-stats1Bold css-18c84du']")[5].text)
        ,'Ann. Equity Return': (driver.find_elements(By.XPATH, "//span[@class='percentage emphasize']")[0].text)
        ,'Ann. Div Yield': (driver.find_elements(By.XPATH, "//span[@class='percentage emphasize']")[1].text)
        ,'Hypoth. Ann. Return': (driver.find_elements(By.XPATH, "//span[@class='percentage emphasize']")[2].text)
        ,'Ttl Prop. Amt': (driver.find_element(By.XPATH, "//div[@class='MuiTypography-root MuiTypography-body1Subheader css-quexwl']").text)
        ,'IPO Shareprice': (driver.find_elements(By.XPATH, "//div[@class='MuiTypography-root MuiTypography-body1Subheader css-sbao0b']")[4].text)        
        ,'Ttl Shares': (driver.find_elements(By.XPATH, "//div[@class='MuiTypography-root MuiTypography-body1Subheader css-sbao0b']")[5].text)        
        ,'Prop. Leverage': (driver.find_element(By.XPATH, "//span[@class='MuiTypography-root MuiTypography-stats1Bold percent css-18c84du']").text)
        ,'Timestamp': datetime.datetime.now()
        # ,'Description': (driver.find_element(By.XPATH, "//div[@class='MuiTypography-root MuiTypography-body2 css-7w8k4p']").text)
    }, ignore_index=True)

    # Track progress of data collection
    complete_count += 1
    print(f"Scraped count: {complete_count}   Property scraped: The {i[40:]}")

driver.quit()

property_data.to_excel("/Users/grantarbuckle/Desktop/Data Analytics/Datasets/Arrived Homes - All Data.xlsx", engine='xlsxwriter')