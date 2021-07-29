import unittest
import time
import pathlib
import inspect
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

path = pathlib.PosixPath('/home/rajesh/Documents/odoo_reports/daily_reports/fee_transaction_summary_report')
path.mkdir(parents=True, exist_ok=True)


class FeeTransactionSummaryReport(unittest.TestCase):
    driver = None

    def setUp(self):
        self.logPoint()
        # d = DesiredCapabilities.CHROME
        # d['loggingPrefs'] = {'browser': 'ALL'}

        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {
            "download.default_directory": "/home/rajesh/Documents/odoo_reports/daily_reports/fee_transaction_summary_report",
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

    def test_fee_transaction_summary_report(self):
        self.logPoint()
        driver = self.driver

        fees_mgmt = driver.find_element_by_xpath("/html//ul[@id='side-menu']/li[3]/"
                                                 "a[@class='nothas-childmenu']/span[1]")
        time.sleep(10)
        driver.execute_script("arguments[0].click();", fees_mgmt)
        time.sleep(5)

        daily_report = driver.find_element_by_xpath("//ul[@id='side-menu']/li[3]/ul/li[4]/a")
        driver.execute_script("arguments[0].click();", daily_report)
        time.sleep(5)

        fts_report = driver.find_element_by_xpath("//a[@href='/web#menu_id=413&action=634']")
        driver.execute_script("arguments[0].click();", fts_report)
        time.sleep(5)

        """Downloading "FTS Report" with Fee = School Fee, Section Masters = All, Start Date = 01/01/2020 & 
        End Date = 30/06/2021 parameters"""

        section_master = driver.find_element_by_xpath("/html/body/div[@role='dialog']/div[@class='modal-dialog modal-lg']/div//div[@class='oe-view-manager-view-form']/div//table/tbody/tr[3]/td[@class='oe_form_group_cell']//span[@class='oe_form_field oe_form_field_many2one oe_form_field_with_button oe_form_required']//input[@type='text']")
        # check "Section Master Field" is displayed & enabled in "Fee Transaction Summary Report"
        self.assertTrue(section_master.is_displayed() and section_master.is_enabled())
        section_master.send_keys("Pri-Primary")
        time.sleep(4)

        section_master1 = driver.find_element_by_link_text("Pri-Primary")
        section_master1.click()

        section_master.send_keys("Primary")
        time.sleep(4)

        section_master2 = driver.find_element_by_link_text("Primary")
        section_master2.click()

        section_master.send_keys("Secondary")
        time.sleep(4)

        section_master3 = driver.find_element_by_link_text("Secondary")
        section_master3.click()

        date_from = driver.find_element_by_xpath("/html/body/div[@role='dialog']/div[@class='modal-dialog modal-lg']/div//div[@class='oe-view-manager-view-form']/div//div[@class='oe_form_nosheet']/table/tbody/tr[@class='oe_form_group_row']/td[@class='oe_form_group_cell']/table/tbody/tr[3]/td[@class='oe_form_group_cell']//input[@name='from_date']")
        # check "From Date Field" is displayed & enabled in "Fee Transaction Summary Report"
        self.assertTrue(date_from.is_displayed() and date_from.is_enabled())
        date_from.send_keys("01/01/2020")

        dummy_click = driver.find_element_by_xpath("/html/body/div[@role='dialog']//footer")
        dummy_click.click()

        date_to = driver.find_element_by_xpath("/html/body/div[@role='dialog']/div[@class='modal-dialog modal-lg']/div//div[@class='oe-view-manager-view-form']/div//div[@class='oe_form_nosheet']/table/tbody/tr[@class='oe_form_group_row']/td[@class='oe_form_group_cell']/table/tbody/tr[4]/td[@class='oe_form_group_cell']//input[@name='to_date']")
        # check "To Date Field" is displayed & enabled in "Fee Transaction Summary Report"
        self.assertTrue(date_to.is_displayed() and date_to.is_enabled())
        date_to.send_keys("30/06/2021")

        dummy_click = driver.find_element_by_xpath("/html/body/div[@role='dialog']//footer")
        dummy_click.click()

        school_fee = driver.find_element_by_name("is_school_fee")
        school_fee.click()

        excel = driver.find_element_by_xpath("/html/body/div[@role='dialog']//footer/button[4]/span[.='Excel']")
        # Check "Excel Button" is displayed & enabled in "Fee Transaction Summary Report"
        self.assertTrue(excel.is_displayed() and excel.is_enabled())
        driver.execute_script("arguments[0].click();", excel)
        time.sleep(10)

        pdf = driver.find_element_by_xpath("/html/body/div[@role='dialog']//footer/button[3]/span[.='PDF']")
        # Check "PDF Button" is displayed & enabled in "Fee Transaction Summary Report"
        self.assertTrue(pdf.is_displayed() and pdf.is_enabled())
        driver.execute_script("arguments[0].click();", pdf)
        time.sleep(10)

        parent = driver.current_window_handle

        view = driver.find_element_by_xpath("/html/body/div[@role='dialog']//footer/button[2]/span[.='View']")
        # Check "View Button" is displayed & enabled in "Fee Transaction Summary Report"
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

        """Downloading "FTS Report" with Fee = Bus Fee, Section Masters = All, Start Date = 01/01/2020 & 
        End Date = 30/06/2021 parameters"""

        school_fee.click()
        bus_fee = driver.find_element_by_name("is_bus_fee")
        bus_fee.click()

        excel = driver.find_element_by_xpath("/html/body/div[@role='dialog']//footer/button[4]/span[.='Excel']")
        # Check "Excel Button" is displayed & enabled in "Fee Transaction Summary Report"
        self.assertTrue(excel.is_displayed() and excel.is_enabled())
        driver.execute_script("arguments[0].click();", excel)
        time.sleep(10)

        pdf = driver.find_element_by_xpath("/html/body/div[@role='dialog']//footer/button[3]/span[.='PDF']")
        # Check "PDF Button" is displayed & enabled in "Fee Transaction Summary Report"
        self.assertTrue(pdf.is_displayed() and pdf.is_enabled())
        driver.execute_script("arguments[0].click();", pdf)
        time.sleep(10)

        parent = driver.current_window_handle

        view = driver.find_element_by_xpath("/html/body/div[@role='dialog']//footer/button[2]/span[.='View']")
        # Check "View Button" is displayed & enabled in "Fee Transaction Summary Report"
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

        """Downloading "FTS Report" with Fee = Both Fee, Section Masters = All, Start Date = 01/01/2020 & 
        End Date = 30/06/2021 parameters"""

        bus_fee.click()
        both_fee = driver.find_element_by_name("is_both_fee")
        both_fee.click()

        excel = driver.find_element_by_xpath("/html/body/div[@role='dialog']//footer/button[4]/span[.='Excel']")
        # Check "Excel Button" is displayed & enabled in "Fee Transaction Summary Report"
        self.assertTrue(excel.is_displayed() and excel.is_enabled())
        driver.execute_script("arguments[0].click();", excel)
        time.sleep(10)

        pdf = driver.find_element_by_xpath("/html/body/div[@role='dialog']//footer/button[3]/span[.='PDF']")
        # Check "PDF Button" is displayed & enabled in "Fee Transaction Summary Report"
        self.assertTrue(pdf.is_displayed() and pdf.is_enabled())
        driver.execute_script("arguments[0].click();", pdf)
        time.sleep(10)

        parent = driver.current_window_handle

        view = driver.find_element_by_xpath("/html/body/div[@role='dialog']//footer/button[2]/span[.='View']")
        # Check "View Button" is displayed & enabled in "Fee Transaction Summary Report"
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
        # Check "Cancel Button" is displayed & enabled in "Fee Transaction Summary Report"
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
