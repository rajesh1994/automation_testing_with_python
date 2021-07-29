import pathlib
import time
import unittest
import inspect
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

path = pathlib.PosixPath('/home/rajesh/Documents/odoo_reports/audit_reports/admission_detail_report')
path.mkdir(parents=True, exist_ok=True)


class AdmissionDetailReport(unittest.TestCase):

    driver = None

    def setUp(self):
        self.logPoint()
        # d = DesiredCapabilities.CHROME
        # d['loggingPrefs'] = {'browser': 'ALL'}

        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {
            "download.default_directory": "/home/rajesh/Documents/odoo_reports/audit_reports/admission_detail_report",
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

    # Downloading the reports with AY = 2020 - 2021 option
    def test_admission_detail_report(self):
        self.logPoint()
        driver = self.driver

        fees_mgmt = driver.find_element_by_xpath("/html//ul[@id='side-menu']/li[3]/"
                                                 "a[@class='nothas-childmenu']/span[1]")
        time.sleep(10)
        driver.execute_script("arguments[0].click();", fees_mgmt)
        time.sleep(5)

        audit_report = driver.find_element_by_xpath("//ul[@id='side-menu']/li[3]/ul/li[5]/a")
        driver.execute_script("arguments[0].click();", audit_report)
        time.sleep(5)

        ad_report = driver.find_element_by_xpath("//a[@href='/web#menu_id=425&action=643']")
        driver.execute_script("arguments[0].click();", ad_report)
        time.sleep(5)

        ay = driver.find_element_by_xpath("/html/body/div[@role='dialog']/div[@class='modal-dialog "
                                          "modal-lg']/div//div[@class='oe-view-manager-view-form']/div//div["
                                          "@class='oe_form_nosheet']/table/tbody/tr[@class='oe_form_group_row']/td["
                                          "@class='oe_form_group_cell']/table//td["
                                          "@class='oe_form_group_cell']//input[@type='text']")
        ay.send_keys("2020")
        time.sleep(4)

        ay1 = driver.find_element_by_css_selector("ul:nth-of-type(2) > .ui-menu-item")
        ay1.click()

        # Check "Academic Year Field" is displayed & enabled in "Admission Detail Report"
        self.assertTrue(ay.is_displayed() and ay.is_enabled())

        excel = driver.find_element_by_xpath("/html/body/div[@role='dialog']//footer/button[4]/span[.='EXCEL']")

        # Check "Excel Button" is displayed & enabled in "Admission Detail Report"
        self.assertTrue(excel.is_displayed() and excel.is_enabled())

        driver.execute_script("arguments[0].click();", excel)
        time.sleep(5)

        pdf = driver.find_element_by_xpath("/html/body/div[@role='dialog']//footer/button[3]/span[.='PDF']")

        # Check "PDF Button" is displayed & enabled in "Admission Detail Report"
        self.assertTrue(pdf.is_displayed() and pdf.is_enabled())

        driver.execute_script("arguments[0].click();", pdf)
        time.sleep(5)

        parent = driver.current_window_handle

        view = driver.find_element_by_xpath("/html/body/div[@role='dialog']//footer/button[2]/span[.='VIEW']")

        # Check "View Button" is displayed & enabled in "Admission Detail Report"
        self.assertTrue(view.is_displayed() and view.is_enabled())

        driver.execute_script("arguments[0].click();", view)

        WebDriverWait(driver, 20).until(ec.number_of_windows_to_be(2))
        child = driver.window_handles

        new_window = [x for x in child if x != parent][0]
        driver.switch_to.window(new_window)

        WebDriverWait(driver, 20).until(ec.title_contains("Pappaya"))
        print("Page Title after second window switching is: %s" % driver.title)
        driver.close()

        driver.switch_to.window(parent)
        WebDriverWait(driver, 20).until(ec.title_contains("Dashboard"))
        print("Page Title after first window switching is: %s" % driver.title)

        cancel = driver.find_element_by_xpath("/html/body/div[@role='dialog']//footer/button[5]/span[.='Cancel']")

        # Check "Cancel Button" is displayed & enabled in "Admission Summary Report"
        self.assertTrue(cancel.is_displayed() and cancel.is_enabled())

        driver.execute_script("arguments[0].click();", cancel)

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
