import os
import random
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

load_dotenv()

class ScrapeData(webdriver.Chrome):
    def __init__(self):
        super(ScrapeData, self).__init__()

    def get_url(self):
        self.get(os.getenv("URL")) # Web page opening

    def get_all(self):
        # Getting all the data from the website (Last 30 Days)
        data = []
        next_page = True

        text_input = self.find_element(By.CLASS_NAME, "k-input") #Find text-input by class
        text_input.click()
        text_input.send_keys(Keys.COMMAND + "a") # Command + A to select all / Ctrl + A for windows. Dunno how to fix
        text_input.send_keys(Keys.DELETE) #Delete the text on text field
        text_input.send_keys("Last 30 Days", Keys.ENTER)
        next_page_button = self.find_element(By.XPATH, os.getenv("NEXT_PAGE_BUTTON")) # Find next-page-button by xpath
        try:
            while next_page:
                random_number = random.randint(1,3) #Getting random number through 1 and 3
                earthquake_table = self.find_element(By.XPATH, os.getenv("TABLE")) #Find table
                row_list = earthquake_table.find_elements(By.XPATH, '//tr') #Find rows

                for row in row_list:
                    row_values = [box.text for box in row.find_elements(By.XPATH, './/td')] #Get datas from each row
                    data.append(row_values)
                
                next_page_button = self.find_element(By.XPATH, os.getenv("NEXT_PAGE_BUTTON"))
                next_page_button.click() #Go next page
                
                time.sleep(random_number) #Sleep for random amount of time(1,3) to get datas from web page consistently
        except ElementClickInterceptedException: #If button is not clickable, we are at the end of the pages
            next_page = False # Ending the loop
        
        for i in data: #Print all the datas that are accesible
            print(i)

    def get_live(self):
        time.sleep(1)
        while True:
            self.refresh() #Refresh the page to go default
            time.sleep(1)
            temp = []
            current_data = []
            current_table = self.find_element(By.XPATH, os.getenv("TABLE")) #Find the data table that currently on the scren
            current_row_list = current_table.find_elements(By.XPATH, '//tr') #Find the rows on the table
            for row in current_row_list:
                values = [box.text for box in row.find_elements(By.XPATH, './/td')] #Get the values on each row
                current_data.append(values)
            current_data.pop(0) #There is empty array at index 0, we simply pop it

            try:
                flag = True
                #Check if the current data and previous data are same, we check by their eventID which is at index 7.
                for i in range(len(previous_data)):
                    if(previous_data[i][7] == current_data[i][7]):
                        pass
                    else:
                        flag = False
                        break
                if flag == True:
                    print("There is no new earthquake occured.")
                else:
                    for element in current_data:
                        if element not in previous_data:
                            temp.append(element)
                    for i in temp:
                        print(i)
            except UnboundLocalError: #In the first execution previous data is not initialized
                print("ERROR")
                pass
            #Assigning current data to previous data in order to store and compare in the next scrape
            previous_data = current_data
            time.sleep(45)
