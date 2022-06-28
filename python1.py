#to get current user username
import getpass

#for cmd
import os
import os.path
import subprocess
#for chrome
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities #import to do pageLoadStrategy
import time #to wait
from selenium.webdriver.common.by import By #for element finding

options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
#to not wait for page to load to run rest of script (click the download button)
caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "eager"
#get current user's username to use for download dir
username = getpass.getuser()
#create downloads dir using current user username
downloadDir = "C:\\Users\\{}\\Downloads".format(username)
#to ignore "this file may harm your computer" & to download into custom dir. Get current user name and go to their downloads folder.
prefs = {"safebrowsing.enabled":"false", "download.default_directory":downloadDir}

options.add_experimental_option("prefs",prefs)

driver = webdriver.Remote(command_executor="http://127.0.0.1:4444/wd/hub", options=options,desired_capabilities=caps)
#go to website
driver.get('https://www.citrix.com/downloads/sharefile/clients-and-plug-ins/citrix-files-for-windows.html')
#find download button by xpath
downloadFile = driver.find_element(By.XPATH, '//*[@id="downloadcomponent_co_1747009400"]/span[2]')
#click download button
downloadFile.click()
#open new tab and go to chrome downloads page
driver.switch_to.new_window('')
driver.get('chrome://downloads')
#get name of most recent downloading file
#use javascript to be able to name shadow DOM elements
shadowScript = 'return document.querySelector("body > downloads-manager").shadowRoot.querySelector("#frb0").shadowRoot.querySelector("#name").innerHTML' #just copied element's JS Path and put .innerHTML at end
downloadFileName = driver.execute_script(shadowScript)
#create download dir with file name
downloadDirAndName = downloadDir + "\\" + downloadFileName
#wait until file is downloaded to close chrome and continue script
#as long as file has not yet been downloaded, wait
while not os.path.exists(downloadDirAndName):
    time.sleep(1)
#once file is downloaded, close chrome and continue script
if os.path.isfile(downloadDirAndName):
    driver.quit()
#run downloaded file. /i means normal installation, /passive means run unattended with progress bar
command = "msiexec.exe /i {} /passive".format(downloadDirAndName) 
subprocess.Popen(command)
