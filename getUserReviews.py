import csv
import requests
import csv
import re
import time
from selenium import webdriver


# import the webdriver, chrome driver is recommended
driver = webdriver.Chrome()
driver.set_page_load_timeout(2)
filename = ""
maxcount = 100
i=0

   
# function to check if the button is on the page, to avoid miss-click problem
def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True
    time.sleep(2)

def writecsv(c1,c2,c3,c4,c5):
    with open(filename, mode='a',newline='') as f:
        #keys = ['name', 'age', 'job', 'city']
        writer = csv.writer(f)
        writer.writerow([str(c1),str(c2),str(c3),str(c4),str(c5)])
       
 

# In[329]:

def allreviews(URL,endcount):

    
    reveiwstab= driver.find_element_by_xpath('//a[@data-tab-name="Reviews"]')
    reveiwstab.click()
    time.sleep(2)   

    if (check_exists_by_xpath("//div[@id='content']")):
        # to expand the review 
        showmorebutton= driver.find_element_by_xpath("//span[@class='_1ogwMK0l']")
        showmorebutton.click()
        time.sleep(30)

    while driver.find_elements_by_xpath("//div[@style='position:relative']/div"):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        review = driver.find_elements_by_xpath("//div[@style='position:relative']/div")
        elementCount = len(review)       
        if (elementCount is endcount):
            print ('end')
            break
        else:
            continue
    

    for j in range(elementCount):

        try:

            name = review[j].find_element_by_xpath(".//div[contains(@class, '_2fxQ4TOx')]").text            
            reviewTitle = review[j].find_element_by_xpath(".//div[contains(@class, '_3IEJ3tAK _2K4zZcBv')]").text                   
            reviewDate = review[j].find_element_by_xpath(".//div[contains(@class, '_3Coh9OJA')]").text          
            reviewFor = review[j].find_element_by_xpath(".//div[contains(@class, '_2ys8zX0p ui_link')]").text
            reviewsummary = review[j].find_element_by_xpath(".//div[contains(@class, '_1kKLd-3D')]/a").get_attribute("href")
            
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(reviewsummary)
            time.sleep(2)
            

            if (check_exists_by_xpath("//span[@class='fullText hidden']")):
                
                readMore = driver.find_elements_by_xpath("//div[@class='reviewSelector']/div/div[2]/div[3]/div/p/span")
                readMore[2].click()
                reviewText = readMore[1].text

            elif (check_exists_by_xpath("//span[@class='fullText ']")):
                
                readMore = driver.find_elements_by_xpath("//div[@class='reviewSelector']/div/div[2]/div[3]/div/p/span")
                reviewText = readMore[0].text
    
            else:
                reviewdetails = driver.find_elements_by_xpath("//div[@class='reviewSelector']/div/div[2]/div/div/div[3]/div/p")
                reviewText = reviewdetails[0].text
                
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            writecsv(name,reviewTitle,reviewText,reviewDate,reviewFor)
            
            

        except:
            print('review not found')
            break
           
# In[330]:


def getallReviewsBymainUrl(URL):

 #get the name of place for csv file name
 global filename 

 driver.get(URL) 
 driver.maximize_window()


 #get element count
 count = driver.find_element_by_class_name("_1q4H5LOk").text.replace (",", "")
 
 #username as the filename
 username = driver.find_element_by_class_name("gf69u3Nd").text

 filename = username+".csv"
 print('start to fill '+filename)

 #open csv file and add titles
 with open(filename, mode='w') as f:
    writer = csv.writer(f)
    writer.writerow([str('user name'),str('reviewTitle'),str('reviewDetails'),str('reviewDate'),str('reviewFor')])

 endcount = int(maxcount) if int(count) > int(maxcount) else int(count)         

 allreviews(URL,endcount)
 print('save reviews in page = ',str(endcount),' user = ',filename)
 print()

# In[331]:

URLs = ['https://www.tripadvisor.com/Profile/JenAzz']
            
         
for url in URLs:
    try:
        getallReviewsBymainUrl(url)
    except:
        print('There is an issue, check again '+url)
            
    print()  

    print('program is complete')    
driver.close()