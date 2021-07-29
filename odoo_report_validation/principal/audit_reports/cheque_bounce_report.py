import unittest
import time
import pathlib
import inspect
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

path = pathlib.PosixPath('/home/rajesh/Documents/odoo_reports/audit_reports/cheque_bounce_report')
path.mkdir(parents=True, exist_ok=True)


class ChequeBounceReport(unittest.TestCase):
    driver = None

    def setUp(self):
        self.logPoint()
        # d = DesiredCapabilities.CHROME
        # d['loggingPrefs'] = {'browser': 'ALL'}

        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {
            "download.default_directory": "/home/rajesh/Documents/odoo_reports/audit_reports/cheque_bounce_report",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False,
            'profile.default_content_setting_values.automatic_downloads': 1})

        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()

        url = "https://uattestnisa.pappayalite.com/web/login"
        self.driver.get(url)

        username = self.driver.find_element_by_id("login")
        username.clear()
        username.send_keys("principal1@pappaya.com")

        password = self.driver.find_element_by_id("password")
        password.clear()
        password.send_keys("pappaya")

        login = self.driver.find_element_by_xpath("//button[@type='submit']")
        login.submit()

    # Downloading the reports with All Grades, AY = 2020 - 2021, Student Type = Total, To Date =  31/05/2021 option
    def test_cheque_bounce_report(self):
        driver = self.driver

        fees_mgmt = driver.find_element_by_xpath("/html//ul[@id='side-menu']/li[3]/"
                                                 "a[@class='nothas-childmenu']/span[1]")
        time.sleep(10)
        driver.execute_script("arguments[0].click();", fees_mgmt)
        time.sleep(5)

        audit_report = driver.find_element_by_xpath("//ul[@id='side-menu']/li[3]/ul/li[5]/a")
        driver.execute_script("arguments[0].click();", audit_report)
        time.sleep(5)

        cb_report = driver.find_element_by_xpath("//a[@href='/web#menu_id=340&action=445']")
        driver.execute_script("arguments[0].click();", cb_report)
        time.sleep(5)

        ay = driver.find_element_by_xpath("/html/body/div[@role='dialog']/div[@class='modal-dialog "
                                          "modal-lg']/div//div[@class='oe-view-manager-view-form']/div//div["
                                          "@class='oe_form_nosheet']/table/tbody/tr[@class='oe_form_group_row']/td["
                                          "@class='oe_form_group_cell']/table//td["
                                          "@class='oe_form_group_cell']//input[@type='text']")
        # check "Academic Year Field" is displayed & enabled in "Cheque Bounce Report"
        self.assertTrue(ay.is_displayed() and ay.is_enabled())
        ay.send_keys("2020 - 2021")
        time.sleep(4)

        ay1 = driver.find_element_by_css_selector("ul:nth-of-type(2) > .ui-menu-item")
        ay1.click()

        date_from = driver.find_element_by_xpath(
            "/html/body/div[@role='dialog']/div[@class='modal-dialog modal-lg']/div//div[@class='oe-view-manager-view-form']/div//div[@class='oe_form_nosheet']/table//td[@class='oe_form_group_cell oe_group_right']/table/tbody/tr[1]/td[@class='oe_form_group_cell']//input[@name='from_date']")
        # check "From Date Field" is displayed & enabled in "Cheque Bounce Report"
        self.assertTrue(date_from.is_displayed() and date_from.is_enabled())
        date_from.send_keys("01/06/2020")

        dummy_click = driver.find_element_by_xpath("/html/body/div[@role='dialog']//footer")
        dummy_click.click()

        date_to = driver.find_element_by_xpath(
            "/html/body/div[@role='dialog']/div[@class='modal-dialog modal-lg']/div//div[@class='oe-view-manager-view-form']/div//div[@class='oe_form_nosheet']/table//td[@class='oe_form_group_cell oe_group_right']/table/tbody/tr[2]/td[@class='oe_form_group_cell']//input[@name='to_date']")
        # check "To Date Field" is displayed & enabled in "Cheque Bounce Report"
        self.assertTrue(date_to.is_displayed() and date_to.is_enabled())
        date_to.send_keys("01/06/2021")

        dummy_click = driver.find_element_by_xpath("/html/body/div[@role='dialog']//footer")
        dummy_click.click()

        excel = driver.find_element_by_xpath("/html/body/div[@role='dialog']//footer/button[1]/span[.='Excel']")
        # Check "Excel Button" is displayed & enabled in "Cheque Bounce Report"
        self.assertTrue(excel.is_displayed() and excel.is_enabled())
        driver.execute_script("arguments[0].click();", excel)
        time.sleep(10)
        driver.close()

    def tearDown(self):
        self.logPoint()
        if self.driver is not None:
            self.driver.quit()
            print("Test Environment Destroyed")

    def logPoint(self):
        current_test = self.id().split('.')[-1]
        calling_function = inspect.stack()[1][3]
        print('in %s - %s()' % (current_test, calling_function))


if __name__ == "__main__":
    unittest.main(exit=False, warnings='ignore', verbosity=2)
