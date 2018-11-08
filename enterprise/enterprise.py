import time
from datetime import datetime
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from tabulate import tabulate
import pandas as pd
import re
import warnings
warnings.simplefilter(action='ignore')
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


car_data_headers = ['Date', 'pickup_date', 'return_date','Location', 'Airport name','selected_location', 'Location Code',
                    'className', 'vehicleName', 'payNowAmount', 'payNowAmountUnit',
                'payNowTotalAmount','payNowTotalUnit','payLaterAmount','payLaterAmountUnit','payLaterTotalAmount','payLaterTotalUnit','sitename']
car_data = []

startTime = time.time()


airport = [["location-1018611","ATL","Hartsfield–Jackson Atlanta International Airport","Atlanta, Georgia"],["location-1018840","ORD","Chicago O'Hare International Airport","Chicago, Illinois"],["location-1019178","lax","Los Angeles International Airport","Los Angeles, California"],["location-1018959","DFW","Dallas/Fort Worth International Airport","Dallas–Fort Worth Metroplex, Texas"],["location-1018781","JFK","John F. Kennedy International Airport","New York, New York"],["location-1018991","DEN","Denver International Airport","Denver, Colorado"],["location-1019129","SFO","San Francisco International Airport","San Francisco, California"],["location-1019084","LAS","McCarran International Airport","Las Vegas, Nevada"],["location-1018702","CLT","Charlotte Douglas International Airport","Charlotte, North Carolina"],["location-1018659","MIA","Miami International Airport","Miami, Florida"],["location-1018543","PHX","Phoenix Sky Harbor International Airport","Phoenix, Arizona"],["location-1018952","IAH","George Bush Intercontinental Airport","Houston, Texas"],["location-1019155","SEA","Seattle–Tacoma International Airport","SeaTac, Washington"],["location-1018631","MCO","Orlando International Airport","Orlando, Florida"],["location-1018780","EWR","Newark Liberty International Airport","Newark, New Jersey"],["location-1018849","MSP","Minneapolis–Saint Paul International Airport","Minneapolis–Saint Paul, Minnesota"],["location-1018717","BOS","Logan International Airport","Boston, Massachusetts"],["location-1018860","DTW","Detroit Metropolitan Airport","Romulus, Michigan"],["location-1018727","PHL","Philadelphia International Airport","Philadelphia, Pennsylvania"],["location-1018775","LGA","LaGuardia Airport","New York, New York"],["location-1018658","FLL","Fort Lauderdale–Hollywood International Airport","Fort Lauderdale, Florida"],["location-1018734","BWI","Baltimore–Washington International Airport","Linthicum, Maryland"],["location-1018724","DCA","Ronald Reagan Washington National Airport","Arlington, Virginia"],["location-1018838","MDW","Chicago Midway International Airport","Chicago, Illinois"],["location-1018893","SLC","Salt Lake City International Airport","Salt Lake City, Utah"],["location-1018719","IAD","Washington Dulles International Airport","Dulles, Virginia"],["location-1019129","SAN","San Diego International Airport","San Diego, California"],["location-1019091","HNL","Daniel K. Inouye International Airport","Honolulu, Hawaii"],["location-1018670","TPA","Tampa International Airport","Tampa, Florida"],["location-1019164","PDX","Portland International Airport","Portland, Oregon"]]
for i in airport:
    for k in [[15, 17], [15, 22]]:
        print(i[2])

        try:

            start_date = (datetime.now() + timedelta(days=k[0])).strftime('%Y%m%d')
            end_date = (datetime.now() + timedelta(days=k[1])).strftime('%Y%m%d')
            print(start_date, end_date)
            pickip_date = (datetime.now() + timedelta(days=k[0])).strftime('%m/%d/%Y')
            return_date = (datetime.now() + timedelta(days=k[1])).strftime('%m/%d/%Y')
            print('https://www.enterprise.com/en/home.html')
            browser = webdriver.Firefox()
            browser.maximize_window()
            browser.get('https://www.enterprise.com/en/home.html')
            time.sleep(8)
            # POPUP
            try:
                browser.find_element_by_css_selector('#acsMainInvite > a:nth-child(2)').click()
            except:
                pass
            try:
                browser.find_element_by_xpath('//*[@id="global-modal-content"]/div/div/button[2]').click()
            except:
                pass
            try:
                browser.find_element_by_css_selector('#acsMainInvite > a:nth-child(2)').click()
            except:
                pass
            try:
                browser.find_element_by_xpath('//*[@id="purposeNoAnswer"]').click()
                time.sleep(2)
                browser.find_element_by_xpath('/html/body/div[5]/div/div[2]/div[2]/div').click()
            except:
                pass
            try:
                browser.find_element_by_class_name('acsInviteButton acsDeclineButton').click()
            except:
                pass

            try:
                browser.find_element_by_xpath('//*[@id="defaultDomainCheckbox"]').click()
                browser.find_element_by_xpath('//*[@id="global-modal-content"]/div/div/button[2]').click()
            except:
                pass
            try:
                browser.find_element_by_xpath('//*[@id="purposeNoAnswer"]').click()
                time.sleep(2)
                browser.find_element_by_xpath('/html/body/div[5]/div/div[2]/div[2]/div').click()
            except:
                pass
            try:
                browser.find_element_by_class_name('acsInviteButton acsDeclineButton').click()
            except:
                pass

            try:
                browser.find_element_by_css_selector('#book > div > div.location-search > div > div.cf.pick-up-location > div > div > div > div.chicklet.location-chicklet-clear').click()
                time.sleep(2)
            except:
                pass
            try:
                browser.find_element_by_xpath('//*[@id="purposeNoAnswer"]').click()
                time.sleep(2)
                browser.find_element_by_xpath('/html/body/div[5]/div/div[2]/div[2]/div').click()
            except:
                pass
            time.sleep(4)
            try:
                browser.find_element_by_xpath('//*[@id="pickupLocationTextBox"]').clear()
            except:
                pass
            time.sleep(4)
            try:
                browser.find_element_by_css_selector('#acsMainInvite > a:nth-child(2)').click()
            except:
                pass
            try:
                browser.find_element_by_xpath('//*[@id="purposeNoAnswer"]').click()
                time.sleep(2)
                browser.find_element_by_xpath('/html/body/div[5]/div/div[2]/div[2]/div').click()
            except:
                pass
            try:
                browser.find_element_by_class_name('acsInviteButton acsDeclineButton').click()
            except:
                pass


            #LOCATION
            try:
                browser.find_element_by_xpath('//*[@id="pickupLocationTextBox"]').send_keys(i[1])
                time.sleep(8)
                element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, i[0])))
                element.click()
            except:
                pass
            # POPUP
            try:
                browser.find_element_by_css_selector('#acsMainInvite > a:nth-child(2)').click()
            except:
                pass
            try:
                browser.find_element_by_xpath('//*[@id="purposeNoAnswer"]').click()
                time.sleep(2)
                browser.find_element_by_xpath('/html/body/div[5]/div/div[2]/div[2]/div').click()
            except:
                pass
            try:
                browser.find_element_by_class_name('acsInviteButton acsDeclineButton').click()
            except:
                pass

            #PICKUP_DATE

            try:
                browser.find_element_by_xpath('//*[@id="pickupCalendarFocusable"]').click()
                browser.find_element_by_xpath("//tbody[contains(@class, 'days cf')]//span[contains(@class, 'day-number') and contains(@data-reactid,"+str(start_date)+")]").click()
                time.sleep(5)
            except:
                pass

            # POPUP
            try:
                browser.find_element_by_css_selector('#acsMainInvite > a:nth-child(2)').click()
            except:
                pass
            try:
                browser.find_element_by_xpath('//*[@id="purposeNoAnswer"]').click()
                time.sleep(2)
                browser.find_element_by_xpath('/html/body/div[5]/div/div[2]/div[2]/div').click()
            except:
                pass
            try:
                browser.find_element_by_class_name('acsInviteButton acsDeclineButton').click()
            except:
                pass

            #RETURN_DATE
            try:
                browser.find_element_by_xpath('//*[@id="dropoffCalendarFocusable"]').click()
                browser.find_element_by_xpath("//tbody[contains(@class, 'days cf')]//span[contains(@class, 'day-number') and contains(@data-reactid,"+str(end_date)+")]").click()
                time.sleep(5)
            except:
                pass

            # POPUP
            try:
                browser.find_element_by_css_selector('#acsMainInvite > a:nth-child(2)').click()
            except:
                pass
            try:
                browser.find_element_by_xpath('//*[@id="purposeNoAnswer"]').click()
                time.sleep(2)
                browser.find_element_by_xpath('/html/body/div[5]/div/div[2]/div[2]/div').click()
            except:
                pass
            try:
                browser.find_element_by_class_name('acsInviteButton acsDeclineButton').click()
            except:
                pass

            #SUBMIT_BUTTON
            try:
                browser.find_element_by_xpath('//*[@id="continueButton"]').click()
            except:
                pass

            # POPUP
            try:
                browser.find_element_by_class_name('acsInviteButton acsDeclineButton').click()
            except:
                pass
            try:
                browser.find_element_by_xpath('//*[@id="purposeNoAnswer"]').click()
                time.sleep(2)
                browser.find_element_by_xpath('/html/body/div[5]/div/div[2]/div[2]/div').click()
            except:
                pass
            try:
                browser.find_element_by_css_selector('#acsMainInvite > a:nth-child(2)').click()
            except:
                pass
            time.sleep(5)
            try:

                if 'no vehicles available'.lower() in browser.page_source.lower():
                    print('sold_out')
                    browser.close()
                    continue

            except:
                pass
            time.sleep(5)

            #PAGE_SOURCE
            jsoup = BeautifulSoup(browser.page_source)
            try:
                browser.find_element_by_css_selector('#acsMainInvite > a:nth-child(2)').click()
            except:
                pass
            try:
                browser.find_element_by_class_name('acsInviteButton acsDeclineButton').click()
            except:
                pass
            try:
                browser.find_element_by_xpath('//*[@id="purposeNoAnswer"]').click()
                time.sleep(2)
                browser.find_element_by_xpath('/html/body/div[5]/div/div[2]/div[2]/div').click()
            except:
                pass
            time.sleep(3)
            car_details = jsoup.find('div', attrs={'class':'cars-wrapper cf'})
            for cars in car_details.find_all('div',attrs = {'class':'car-container animated has-promotion','data-reactid':re.compile('\$car-\d')}):
                car_class = cars.find('h2')
                print(car_class.text)
                car_name = cars.find('div',attrs={'class':'car-header'}).find('span')
                print(car_name.text)
                pay_later_total = cars.find('div',attrs={'class':'rates cf '}) if cars is not None else None
                pay_later_total = pay_later_total.find('div',attrs = {'class':'total-rate rate-info'}) if pay_later_total is not None else None
                pay_later_total_unit = pay_later_total.find('div', attrs={'class': 'rate-subtext'}).find('span') if pay_later_total is not None else None
                pay_later_total_unit = re.search('[A-Za-z]+',pay_later_total_unit.text) if pay_later_total_unit is not None else None
                pay_later_total_unit = pay_later_total_unit.group(0) if pay_later_total_unit is not None else None
                print(pay_later_total_unit)
                pay_later_total = pay_later_total.find('div', attrs={'class':'block-separator'})if pay_later_total is not None else None
                pay_later_total = re.search('\$ [0-9\.,]+', pay_later_total.text) if pay_later_total is not None else None
                pay_later_total = pay_later_total.group(0) if pay_later_total is not None else None
                print(pay_later_total)


                per_day_later = cars.find('div',attrs={'class':'rates cf '}) if cars is not None else None
                per_day_later = per_day_later.find('div', attrs={'class': 'day-rate rate-info'})if per_day_later is not None else None
                per_day_later_unit = per_day_later.find('div', attrs={'class': 'rate-subtext'}) if per_day_later is not None else None
                per_day_later_unit = re.search('[A-Za-z ]+', per_day_later_unit.text) if per_day_later_unit is not None else None
                per_day_later_unit = per_day_later_unit.group(0) if per_day_later_unit is not None else None
                print(per_day_later_unit)
                per_day_later = per_day_later.find('div', attrs={'class': 'block-separator'}) if per_day_later is not None else None
                per_day_later = re.search('\$ [0-9\.,]+', per_day_later.text) if per_day_later is not None else None
                per_day_later = per_day_later.group(0) if per_day_later is not None else None
                print(per_day_later)
                data = [datetime.now().strftime('%m/%d/%Y'), pickip_date, return_date, i[3], i[2], i[2], i[1], car_class.text,
                        car_name.text,None, None, None, None, per_day_later, per_day_later_unit,
                        pay_later_total, pay_later_total_unit,'Enterprise']
                car_data.append(data)


            time.sleep(5)
            browser.close()


        except Exception as e:
            print(e)

        break
    break

print(tabulate(car_data))
df = pd.DataFrame(car_data,columns=car_data_headers)
print(df)
df.to_excel('Enterprise.xlsx', index=False)
print('Time = ', (time.time()-startTime)/60)