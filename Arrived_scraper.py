from importlib.resources import path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager #ALWAYS USE THIS TO INSTALL CHROME DRIVER FOR FUTURE PROJECTS
import time
import pandas as pd
import datetime

url = "https://arrivedhomes.com/app/properties"
PATH = "/Users/grantarbuckle/chromedriver"
user_path = "/Users/grantarbuckle/Desktop/Data Analytics/Datasets/Arrived Homes Data.xlsx" # Change as needed

# SERVICE = Service(executable_path=PATH)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install())) #ALWAYS USE THIS TO INSTALL CHROME DRIVER FOR FUTURE PROJECTS
driver.maximize_window()
driver.get(url)

# Filter by vacation rentals
driver.find_element(By.XPATH, "*//div[2]/span/p").click() #Stale reference error AGAIN
vaca_properties_search=driver.find_elements(By.TAG_NAME, "a")

# Create list of only vacation rental property hyperlinks
vaca_hyperlink_list = []
for i in vaca_properties_search:
    hyperlink = i.get_attribute("href")
    if hyperlink[0:36] == "https://arrivedhomes.com/properties/":
        vaca_hyperlink_list.append(hyperlink)

# Remove property filters
driver.find_element(By.XPATH, "//p[text()='All']").click()
all_properties_search=driver.find_elements(By.TAG_NAME, "a")

# Create list of non-vacation rental property hyperlinks
non_vaca_rental_list = []
for i in all_properties_search:
    hyperlink = i.get_attribute("href")
    if hyperlink[0:36] == "https://arrivedhomes.com/properties/":
        non_vaca_rental_list.append(hyperlink)

# List comprehension to remove vaca rentals from all properties list
non_vaca_rental_list = [x for x in non_vaca_rental_list if x not in vaca_hyperlink_list]

# Read in existing data, or create new dataframe if scraping for the first time. Change path as needed
try:
    property_data = pd.read_excel(user_path)
except:
    property_data = pd.DataFrame(columns= [
    "Name", "Property Details", "Timestamp", "Percent Funded", "Address", "Purchase Price", "Ttl Prop. Amt", "Share $ Avail.", "Ttl Shares", "Investors", "Rent Ready Date", "Rental Status",
    "Mo. Rent", "Div Date", "1st Div Yield", "Ann. Equity Return", "Ann. Div Yield", "Hypoth. Ann. Return", "Prop. Leverage", "IPO Shareprice", "AirDNA Market Grade" #, "Description"
    ])

scraped_count = 0
checked_count = 0

# Create function to identify "Coming Soon" listings
def hasXpath(xpath):
    try:
        driver.find_element(By.XPATH, xpath)
        return True
    except:
        return False

for i in vaca_hyperlink_list:
    driver.get(i)
    time.sleep(5) # Increase time if "Stale Element" error message occurs
    prop_name = driver.find_element(By.XPATH, "//h3[@data-e2e]").text
    if hasXpath("//h6[contains(text(),'100%')]") == False and hasXpath("//*[contains(text(),' coming soon')]") == False: #filter out fully funded and "Coming Soon" listings
        property_data = property_data.append({
            'Name': prop_name
            ,'Property Details': (driver.find_element(By.XPATH, "*//p[@data-e2e='property-details-house-info-wrapper']").text)
            ,'Purchase Price': (driver.find_elements(By.XPATH, "*//li/p[2]")[1].text)
            ,"Rent Ready Date": (driver.find_elements(By.XPATH, "*//li/p[2]")[2].text)
            ,'Investors': (driver.find_elements(By.XPATH, "*//li/p[2]")[0].text)
            ,'Share $ Avail.': (driver.find_element(By.XPATH, "*//p/h4").text)
            ,"Percent Funded": driver.find_element(By.XPATH, "//h6[contains(text(),'%')]").text
            ,'Address': (driver.find_element(By.XPATH, "//*[contains(text(),'Address:')]").text)
            ,'Ann. Equity Return': (driver.find_element(By.XPATH, "*//div/span[@class='MuiTypography-root MuiTypography-h5 css-pzkpi9']").text)
            ,'Ann. Div Yield': (driver.find_element(By.XPATH, "*//div/span[@class='MuiTypography-root MuiTypography-h5 css-1r9rzgb']").text)
            ,'1-Yr Return Hist. Avg': (driver.find_element(By.XPATH, "*//div/span[@class='MuiTypography-root MuiTypography-h4 css-tgfgaq']").text)
            ,'Ttl Prop. Amt': (driver.find_elements(By.XPATH, "*//div/p[@class='MuiTypography-root MuiTypography-body1.semibold css-1okjomr']")[1].text)
            ,'IPO Shareprice': (driver.find_elements(By.XPATH, "*//ul/li/p[@class='MuiTypography-root MuiTypography-body1.semibold css-1okjomr']")[6].text)        
            ,'Ttl Shares': (driver.find_elements(By.XPATH, "*//ul/li/p[@class='MuiTypography-root MuiTypography-body1.semibold css-1okjomr']")[7].text)        
            ,'Prop. Leverage': (driver.find_element(By.XPATH, "*//div/p[@class='MuiTypography-root MuiTypography-body1 percent css-10wdd1m']").text)
            ,'AirDNA Market Grade': (driver.find_element(By.XPATH, "*//div/div[@class='MuiBox-root css-qwbho3']").get_attribute("src")) #pick up here
            ,'Timestamp': datetime.datetime.now()
            # ,'Description': (driver.find_element(By.XPATH, "//div[@class='MuiTypography-root MuiTypography-body2 css-7w8k4p']").text)
        }, ignore_index=True)

        # Div Date only available if you are a shareholder of the property and logged in on the webdriver Chrome session
        try:
            property_data.loc[property_data.Name == prop_name, 'Div Date'] = driver.find_element(By.XPATH, "//span[@class='MuiTypography-root MuiTypography-body2 css-1hog4co']").text
        except:
            property_data.loc[property_data.Name == prop_name, 'Div Date'] = ''

        # Track progress of data collection
        scraped_count += 1
    checked_count +=1
    print(f"Checked count: {checked_count}   Scraped count: {scraped_count}   Property checked: {prop_name}")

# Append data to dataframe for non vacation rental properties
for i in non_vaca_rental_list:
    driver.get(i)
    time.sleep(3) # Increase time if "Stale Element" error message occurs
    prop_name = driver.find_element(By.XPATH, "//h3[@data-e2e]").text
    percent_funded = driver.find_element(By.XPATH, "//h6[contains(text(),'%')]").text
    if hasXpath("//h6[contains(text(),'100%')]") == False and hasXpath("//*[contains(text(),' coming soon')]") == False: #filter out fully funded and "Coming Soon" listings:
        property_data = property_data.append({
            'Name': prop_name
            ,'Property Details': (driver.find_element(By.XPATH, "//p[contains(text(),'sq ft')]").text)
            ,'Purchase Price': (driver.find_elements(By.XPATH, "*//div/ul[1]/li[2]/p[2]")[0].text)
            ,'Mo. Rent': (driver.find_elements(By.XPATH, "*//div/ul[1]/li[3]/p[2]")[0].text)
            ,'Investors': (driver.find_elements(By.XPATH, "*//div/ul[1]/li[1]/p[2]")[0].text)
            ,'Share $ Avail.': (driver.find_element(By.XPATH, "*//div/span/p[contains(text(),'available')]").text)
            ,"Percent Funded": percent_funded
            ,'Address': (driver.find_element(By.XPATH, "//*[contains(text(),'Address:')]").text)
            ,'Rental Status': (driver.find_element(By.XPATH, "*//div[1]/li/p[2]").text)
            ,'Div Date': (driver.find_element(By.XPATH, "*//div[2]/li/p[2]").text)
            ,'1st Div Yield': (driver.find_element(By.XPATH, "*//div[3]/li/p[2]").text)
            ,'Ann. Equity Return': (driver.find_elements(By.XPATH, "//div[2]/div/span[1]")[1].text)
            ,'Ann. Div Yield': (driver.find_elements(By.XPATH, "//div[2]/div/span[1]")[2].text)
            ,'1-Yr Return Hist. Avg': (driver.find_elements(By.XPATH, "//div[5]/div/div/span[1]")[1].text)
            ,'Ttl Prop. Amt': (driver.find_element(By.XPATH, "//div[1]/div[1]/div[1]/p[2]").text)
            ,'IPO Shareprice': (driver.find_element(By.XPATH, "//ul[2]/li[1]/p[2]").text)        
            ,'Ttl Shares': (driver.find_element(By.XPATH, "//ul[2]/li[2]/p[2]").text)        
            ,'Prop. Leverage': (driver.find_elements(By.XPATH, "//div/div/div/div/div/div/div/div/div/div/div/div/div/p")[14].text)
            ,'Timestamp': datetime.datetime.now()
            # ,'Description': (driver.find_element(By.XPATH, "//div[@class='MuiTypography-root MuiTypography-body2 css-7w8k4p']").text)
        }, ignore_index=True)

        # Track progress of data collection
        scraped_count += 1
    checked_count +=1
    print(f"Checked count: {checked_count}   Scraped count: {scraped_count}   Property checked: {prop_name}")

driver.quit()

# Write output to specified file path
property_data = property_data.reset_index(drop=True)
property_data.to_excel(user_path, engine='xlsxwriter', index=False)