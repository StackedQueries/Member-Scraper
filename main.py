

from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import time
from selenium.webdriver.firefox.options import Options
import sqlite3
import config


conn = sqlite3.connect(config._DB)

c = conn.cursor()

options = Options()
options.set_headless(True)
driver = webdriver.Firefox(options=options,executable_path=config._GECKO)

for i in range(232):
    print("page " +str(i+1))

    list1 = []
    while True:
        driver.get(config._URL + str(i + 1))
        try:
            driver.refresh()

            wait = WebDriverWait(driver, 10)
            driver.execute_script("return document.body.innerHTML")

            i = driver.page_source.find('iframe id="membee')
            id=driver.page_source[i+11:i+22]
            html = driver.switch_to.frame(id)
            break
        except:
            driver.refresh()
            pass

    elems = driver.find_elements_by_tag_name('a')

    for elem in elems:
        href = elem.get_attribute('href')
        if href is not None and href.find("https://memberservices.membee.com/feeds/directory/directory/action/Listing/value") != -1 and href not in list1:
            print(str(len(list1))+" "+href)
            list1.append(href)

    time.sleep(5)

    for link in list1:
        driver.get(link)
        while True:
            try:
                wait = WebDriverWait(driver, 10)
                driver.execute_script("return document.body.innerHTML")

                i = driver.page_source.find('iframe id="membee')
                id = driver.page_source[i + 11:i + 22]
                html = driver.switch_to.frame(id)
                break
            except:
                print("failed to find info")
                driver.refresh()
                pass

        Bname = driver.find_elements_by_xpath('//*[@id="ucDirectory_UcListing_lblOwner"]')[0].text
        print(Bname)
        try:
            website = driver.find_elements_by_xpath('//*[@id="ucDirectory_UcListing_hlWebsite"]')[0].text
            print(driver.find_elements_by_xpath('//*[@id="ucDirectory_UcListing_hlWebsite"]')[0].text)

        except:
            website = None
        try:
            phone = driver.find_elements_by_xpath('//*[@id="ucDirectory_UcListing_lblPhone1"]')[0].text
            print(phone)
        except:
            phone = None
        try:
            contact = driver.find_elements_by_xpath('//*[@id="ucDirectory_UcListing_rptOurPeople_ctl00_hlEmployeeName"]')[0].text
            print(contact)
        except:
            contact = None
        try:
            cnumber = driver.find_elements_by_xpath('//*[@id="ucDirectory_UcListing_rptOurPeople_ctl00_lblPhone"]')[0].text
            print(cnumber)
        except:
            cnumber = None


        c.execute("INSERT INTO users VALUES (:Bname, :web, :number, :contact, :cnumber)", (Bname,website,phone,contact,cnumber))
        conn.commit()
c.close()

driver.quit()