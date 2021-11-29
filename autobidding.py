#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading 
import time
from datetime import datetime
from selenium import webdriver

your_name = "Li, XXX XXX"
bidding_time = "2021-11-24 16:59:52.000"
reasonable_price = 560.0
bid_list = ["https://cnnkg04003.ad001.siemens.net:83/AOS/SubPages/Auction/Bidding.aspx?aiid=45",
            "https://cnnkg04003.ad001.siemens.net:83/AOS/SubPages/Auction/Bidding.aspx?aiid=43",
            "https://cnnkg04003.ad001.siemens.net:83/AOS/SubPages/Auction/Bidding.aspx?aiid=52",
            "https://cnnkg04003.ad001.siemens.net:83/AOS/SubPages/Auction/Bidding.aspx?aiid=54"]

#################################################################
def bid(strURL):
    option = webdriver.ChromeOptions()
    option.add_argument("headless")
    browser = webdriver.Chrome(options=option)
    # Should enter into main page first for login
    browser.get("https://cnnkg04003.ad001.siemens.net:83/AOS/")
    browser.get(strURL)

    high_price_by_name = browser.find_element_by_id("gvBiddingRecords_ctl02_lblBidderName")
    if(high_price_by_name.text == your_name):
        print("You have already bought it!")
        browser.quit
        return
    else:
        print("Current hold by", high_price_by_name.text)
    
    price = browser.find_element_by_id("lblAICurrentPrice")
    if float(price.text) < reasonable_price :
        print("Price OK, just buy it... at ", float(price.text) + 50.0)
        browser.find_element_by_id("tbAIAmount").send_keys("1")
        browser.find_element_by_id("tbBidPrice").send_keys(str(float(price.text) + 50.0))
        browser.find_element_by_id("iBtnBid").click()
    else:
        print("It is too expensive, do not buy it at", price.text)
        
    browser.quit
    return

# Wait-time
print('Wait for bidding time:%s', bidding_time)
now_time = datetime.now
while True:
    if now_time() >= datetime.strptime(bidding_time, "%Y-%m-%d %H:%M:%S.%f"):
        print('Now, start bidding……')
        break
    else:
        time.sleep(0.5)
    
# Multi-threads 
threads = []    
for i in range(0, len(bid_list)):
    threads.append(threading.Thread(target=bid, args=(bid_list[i],)))
    threads[i].start()
    
for t in threads:
    t.join()

print("End time...", now_time())
