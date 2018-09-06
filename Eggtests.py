from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import sched
import time
from datetime import datetime

class Eggtests:

    def setup(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://e.ggtimer.com/')
        self.driver.maximize_window()
        my_element = WebDriverWait(self.driver, 3).until(EC.visibility_of_all_elements_located((By.ID,'start_a_timer')))

    def test(self, interval):
        self.set_item(interval)
        self.click_go()
        first_display_value = self.get_first_display_number()
        self.check_timer(first_display_value)

    def set_item(self, interval):
        item_element = self.driver.find_element(By.ID, 'start_a_timer')
        item_element.clear()
        self.input_interval = int(interval)
        item_element.send_keys(interval)

    def click_go(self):
        go_button = self.driver.find_element(By.ID, 'timergo')
        #System time before the click button
        self.go_button_click_time = datetime.now()
        go_button.submit()

    def get_first_display_number(self):
        return self.get_display_number();

    def get_display_number(self):
        timer_element = self.driver.find_element(By.ID, 'progressText')
        string_value_read = timer_element.text
        #split on space and get 1st value
        string_array = string_value_read.split(" ")
        number_value_read = string_array[0]
        int_value_read = int(number_value_read)
        return int_value_read

    def get_time_elapesed_from_click_go(self):
        #current system time minus the time when go was clicked in seconds
        diff_in_float = (datetime.now() - self.go_button_click_time).total_seconds()
        diff_in_int = int(diff_in_float)
        #return input count minus the difference in seconds
        return self.input_interval - diff_in_int

    def check_timer(self, int_value):

        if int_value > 0:
            elapsed_time = self.get_time_elapesed_from_click_go()
            int_value_read = self.get_display_number()
            assert int_value_read == int_value

        if int_value >= 0:
            s = sched.scheduler(time.time, time.sleep)
            s.enter(1, 1, self.check_timer, argument=(int_value-1,))
            s.run()

        if int_value < 0:
            alert = self.driver.switch_to.alert
            alert.accept()

    def tear_down(self):
        self.driver.close()
        print 'Test finished'
