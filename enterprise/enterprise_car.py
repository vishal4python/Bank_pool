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
import os

startTime = time.time()
def get_eneterpricecar_data(row, car_data):
    dir = os.getcwd() + '\\' + datetime.today().strftime('%d-%m-%Y')
    if not os.path.isdir(dir):
        os.mkdir(dir)
    browser = webdriver.Firefox()
    browser.maximize_window()
    carData = []
    count = 0
    check_count = 0
    check_days = [[15, 17], [15, 22]]
    for k in check_days:
        try:

            start_date = (datetime.now() + timedelta(days=k[0])).strftime('%Y%m%d')
            end_date = (datetime.now() + timedelta(days=k[1])).strftime('%Y%m%d')
            print(start_date, end_date)
            pickip_date = (datetime.now() + timedelta(days=k[0])).strftime('%m/%d/%Y')
            return_date = (datetime.now() + timedelta(days=k[1])).strftime('%m/%d/%Y')
            print('https://www.enterprise.com/en/home.html')

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
                browser.find_element_by_xpath('//*[@id="pickupLocationTextBox"]').send_keys(row['Code'])
                time.sleep(8)
                element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, row['loc_code'])))
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
            
            print(jsoup)
            car_details = jsoup.find('div', attrs={'class':'cars-wrapper cf'})
            
            # for cars in car_details.find_all('div',attrs = {'class':'car-container animated has-promotion','data-reactid':re.compile('\$car-\d')}):
            #     car_class = cars.find('h2')
            #     print(car_class.text)
            #     car_name = cars.find('div',attrs={'class':'car-header'}).find('span')
            #     print(car_name.text)
            #     pay_later_total = cars.find('div',attrs={'class':'rates cf '}) if cars is not None else None
            #     pay_later_total = pay_later_total.find('div',attrs = {'class':'total-rate rate-info'}) if pay_later_total is not None else None
            #     pay_later_total_unit = pay_later_total.find('div', attrs={'class': 'rate-subtext'}).find('span') if pay_later_total is not None else None
            #     pay_later_total_unit = re.search('[A-Za-z]+',pay_later_total_unit.text) if pay_later_total_unit is not None else None
            #     pay_later_total_unit = pay_later_total_unit.group(0) if pay_later_total_unit is not None else None
            #     print(pay_later_total_unit)
            #     pay_later_total = pay_later_total.find('div', attrs={'class':'block-separator'})if pay_later_total is not None else None
            #     pay_later_total = re.search('\$ [0-9\.,]+', pay_later_total.text) if pay_later_total is not None else None
            #     pay_later_total = pay_later_total.group(0) if pay_later_total is not None else None
            #     print(pay_later_total)
            #
            #
            #     per_day_later = cars.find('div',attrs={'class':'rates cf '}) if cars is not None else None
            #     per_day_later = per_day_later.find('div', attrs={'class': 'day-rate rate-info'})if per_day_later is not None else None
            #     per_day_later_unit = per_day_later.find('div', attrs={'class': 'rate-subtext'}) if per_day_later is not None else None
            #     per_day_later_unit = re.search('[A-Za-z ]+', per_day_later_unit.text) if per_day_later_unit is not None else None
            #     per_day_later_unit = per_day_later_unit.group(0) if per_day_later_unit is not None else None
            #     print(per_day_later_unit)
            #     per_day_later = per_day_later.find('div', attrs={'class': 'block-separator'}) if per_day_later is not None else None
            #     per_day_later = re.search('\$ [0-9\.,]+', per_day_later.text) if per_day_later is not None else None
            #     per_day_later = per_day_later.group(0) if per_day_later is not None else None
            #     print(per_day_later)
            #     if pay_later_total is not None:
            #         data = [datetime.now().strftime('%m/%d/%Y'), pickip_date, return_date, row['Location'], row['Airport name'], row['Airport name'], row['Code'], car_class.text,
            #                 car_name.text,None, None, None, None, per_day_later, per_day_later_unit,
            #                 pay_later_total, pay_later_total_unit,'Enterprise']
            #         carData.append(data)
            car_details = jsoup.find('ul', attrs={'class': 'vehicle-list'})
            for cars in car_details.find_all('li', attrs={'class': 'vehicle-list__item'}):
                print('.'.center(100, '.'))
                print(cars)
                car_class = cars.find('h2')
                print(car_class.text)
                car_name = cars.find('p', attrs={'class': 'vehicle-item__models'})
                print(car_name.text)

                pay = cars.find_all('div', attrs={'class': "price-tile"})
                pay_later_total = None
                per_day_later = None
                for k in pay:
                    if 'total' in k.text:
                        pay_later_total = k.text
                    else:
                        per_day_later = k.text
                pay_later_total = (re.search('\$[0-9,\.]+', pay_later_total).group(0) if re.search('\$[0-9,\.]+',
                                                                                                   pay_later_total) else None) if pay_later_total else None
                per_day_later = (re.search('\$[0-9,\.]+', per_day_later).group(0) if re.search('\$[0-9,\.]+',
                                                                                               per_day_later) else None) if per_day_later else None
                print('pay_later_total = ', pay_later_total)
                print('per_day_later = ', per_day_later)
                if pay_later_total is not None:
                    data = [datetime.now().strftime('%m/%d/%Y'), pickip_date, return_date, row['Location'], row['Airport name'], row['Airport name'], row['Code'], car_class.text,
                            car_name.text,None, None, None, None, per_day_later, None,
                            pay_later_total, None,'Enterprise']
                    carData.append(data)

            count += 1


        except Exception as e:
            browser.save_screenshot(dir+'\\'+row['Code'] + datetime.today().strftime('%d-%m-%Y') + ".png")
            if check_count == 2:
                break
            check_count += 1
            check_days.append(k)
            print(e, row)
            print(e)
        
    browser.close()
    if len(carData) != 0:
        car_data[row['Code']] = carData
        return car_data