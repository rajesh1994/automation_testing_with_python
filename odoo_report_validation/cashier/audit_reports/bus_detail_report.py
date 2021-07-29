import unittest
import time
import pathlib
import inspect
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

path = pathlib.PosixPath('/home/rajesh/Documents/odoo_reports/audit_reports/bus_detail_report')
path.mkdir(parents=True, exist_ok=True)


class BusDetailReport(unittest.TestCase):
    driver = None

    def setUp(self):
        self.logPoint()
        # d = DesiredCapabilities.CHROME
        # d['loggingPrefs'] = {'browser': 'ALL'}

        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {
            "download.default_directory": "/home/rajesh/Documents/odoo_reports/audit_reports/bus_detail_report",
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
        username.send_keys("cashier1@pappaya.com")

        password = self.driver.find_element_by_id("password")
        password.clear()
        password.send_keys("pappaya")

        login = self.driver.find_element_by_xpath("//button[@type='submit']")
        login.submit()

    # Downloading the reports with All Grades, AY = 2020 - 2021, Student Type = Total, To Date =  31/05/2021 option
    def test_bus_detail_report(self):
        self.logPoint()
        driver = self.driver

        fees_mgmt = driver.find_element_by_xpath("/html//ul[@id='side-menu']/li[3]/"
                                                 "a[@class='nothas-childmenu']/span[1]")
        time.sleep(20)
        driver.execute_script("arguments[0].click();", fees_mgmt)
        time.sleep(5)

        audit_report = driver.find_element_by_xpath("//ul[@id='side-menu']/li[3]/ul/li[5]/a")
        driver.execute_script("arguments[0].click();", audit_report)
        time.sleep(5)

        bd_report = driver.find_element_by_xpath("//a[@href='/web#menu_id=423&action=606']")
        driver.execute_script("arguments[0].click();", bd_report)
        time.sleep(5)

        ay = driver.find_element_by_xpath("/html/body/div[@role='dialog']/div[@class='modal-dialog "
                                          "modal-lg']/div//div[@class='oe-view-manager-view-form']/div//div["
                                          "@class='oe_form_nosheet']/table[2]/tbody/tr["
                                          "@class='oe_form_group_row']/td["
                                          "@class='oe_form_group_cell']/table/tbody/tr[1]/td["
                                          "@class='oe_form_group_cell']//input[@type='text']")
        # check "Academic Year Field" is displayed & enabled in "Bus Detail Report"
        self.assertTrue(ay.is_displayed() and ay.is_enabled())
        ay.send_keys("2020")
        time.sleep(4)

        ay1 = driver.find_element_by_css_selector("ul:nth-of-type(2) > .ui-menu-item")
        ay1.click()
        time.sleep(5)

        to_date = driver.find_element_by_name("to_date")
        # check "To Date Field" is displayed & enabled in "Bus Detail Report"
        self.assertTrue(to_date.is_displayed() and to_date.is_enabled())
        to_date.clear()
        to_date.send_keys("31/05/2021")
        time.sleep(5)

        all_grade = driver.find_element_by_name("grade_all")
        all_grade.click()
        # check "All Grade Field" is displayed & enabled in "Bus Detail Report"
        # self.assertTrue(all_grade.is_displayed() and all_grade.is_selected())

        excel = driver.find_element_by_xpath("/html/body/div[@role='dialog']//footer/button[4]/span[.='Excel']")
        # Check "Excel Button" is displayed & enabled in "Bus Detail Report"
        self.assertTrue(excel.is_displayed() and excel.is_enabled())
        driver.execute_script("arguments[0].click();", excel)
        time.sleep(10)

        pdf = driver.find_element_by_xpath("/html/body/div[@role='dialog']//footer/button[3]/span[.='PDF']")
        # Check "PDF Button" is displayed & enabled in "Admission Detail Report"
        self.assertTrue(pdf.is_displayed() and pdf.is_enabled())
        driver.execute_script("arguments[0].click();", pdf)
        time.sleep(10)

        parent = driver.current_window_handle

        view = driver.find_element_by_xpath("/html/body/div[@role='dialog']//footer/button[2]/span[.='View']")
        # Check "View Button" is displayed & enabled in "Bus Detail Report"
        self.assertTrue(view.is_displayed() and view.is_enabled())
        driver.execute_script("arguments[0].click();", view)
        time.sleep(10)

        WebDriverWait(driver, 120).until(ec.number_of_windows_to_be(2))
        child = driver.window_handles

        new_window = [x for x in child if x != parent][0]
        driver.switch_to.window(new_window)

        WebDriverWait(driver, 20).until(ec.title_contains("Pappaya"))
        print("Page Title after second window switching is: %s" % driver.title)
        driver.close()

        driver.switch_to.window(parent)
        WebDriverWait(driver, 20).until(ec.title_contains("Dashboard"))
        print("Page Title after first window switching is: %s" % driver.title)

        all_grade = driver.find_element_by_name("grade_all")
        # check "All Grade Field" is displayed & selected in "Bus Detail Report"
        # self.assertTrue(all_grade.is_displayed() and all_grade.is_selected())
        all_grade.click()

        grade = driver.find_element_by_xpath("/html/body/div[@role='dialog']/div[@class='modal-dialog "
                                             "modal-lg']/div/div[@class='modal-body o_act_window']//div["
                                             "@class='oe-view-manager-view-form']/div//div["
                                             "@class='oe_form_nosheet']/table[2]/tbody/tr["
                                             "@class='oe_form_group_row']/td["
                                             "@class='oe_form_group_cell']/table/tbody/tr[3]/td["
                                             "@class='oe_form_group_cell']//input[@type='text']")

        # Check "Grade Field" is displayed & enabled in "Bus Detail Report"
        self.assertTrue(grade.is_displayed() and grade.is_enabled())
        grade.send_keys("I")
        time.sleep(4)

        grade1 = driver.find_element_by_partial_link_text("I")
        driver.execute_script("arguments[0].click();", grade1)

        excel = driver.find_element_by_xpath("/html/body/div[@role='dialog']//footer/button[4]/span[.='Excel']")
        # Check "Excel Button" is displayed & enabled in "Bus Detail Report"
        self.assertTrue(excel.is_displayed() and excel.is_enabled())
        driver.execute_script("arguments[0].click();", excel)
        time.sleep(10)

        pdf = driver.find_element_by_xpath("/html/body/div[@role='dialog']//footer/button[3]/span[.='PDF']")
        # Check "PDF Button" is displayed & enabled in "Bus Detail Report"
        self.assertTrue(pdf.is_displayed() and pdf.is_enabled())
        driver.execute_script("arguments[0].click();", pdf)
        time.sleep(10)

        parent = driver.current_window_handle

        view = driver.find_element_by_xpath("/html/body/div[@role='dialog']//footer/button[2]/span[.='View']")
        # Check "View Button" is displayed & enabled in "Bus Detail Report"
        self.assertTrue(view.is_displayed() and view.is_enabled())
        driver.execute_script("arguments[0].click();", view)
        time.sleep(10)

        WebDriverWait(driver, 120).until(ec.number_of_windows_to_be(2))
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
        # Check "Cancel Button" is displayed & enabled in "Bus Detail Report"
        self.assertTrue(cancel.is_displayed() and cancel.is_enabled())
        driver.execute_script("arguments[0].click();", cancel)
        time.sleep(10)

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
