import unittest, sys, os
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

#Start the server

#Open browser, connect and login first
os.environ["PATH"] += ";"+os.path.dirname(__file__)
cd = webdriver.Chrome()
cd.implicitly_wait(10)
cd.get('localhost:9000/')
uname_in = cd.find_element_by_id('uname')
cd.execute_script("jQuery.dnd.send('reset','testing')")
uname_in.send_keys("Sushisource")
uname_in.send_keys("\n")

class BrowserTests(unittest.TestCase):

    def setUp(self):
        print cd.find_element_by_id("chat_in").value_of_css_property("visible")
        WebDriverWait(cd, 3).until(
            lambda driver : driver.find_element_by_id("chat_in").is_displayed())

    def tearDown(self):
        pass

    def formfiller(self, btnid, startid, *fields):
        add = cd.find_element_by_id(btnid)
        name = cd.find_element_by_id(startid)
        #Last dialog could still be up
        WebDriverWait(cd, 3).until(
            lambda driver : not name.is_displayed())
        #Make sure name field has focus
        add.click()
        WebDriverWait(cd, 3).until(
            lambda driver : name.is_displayed())
        #Make sure name field has focus
        self.assertTrue(name.id == cd.switch_to_active_element().id)
        #send keys
        keys = "{0}"
        for i in range(1,len(fields)):
            keys += "\t{"+str(i)+"}"
        keys += "\n"
        keys = keys.format(*fields)
        name.send_keys(keys)

class LoginTest(BrowserTests):
    def runTest(self):
        userlbl = cd.find_element_by_id('user_label')
        self.assertTrue(userlbl.text == "Sushisource")

class ChatTest(BrowserTests):
    def runTest(self):
        chat_in = cd.find_element_by_id('chat_in')
        chat_in.send_keys("Chatting!\n")

class DiceTest(BrowserTests):
    def runTest(self):
        chat_in = cd.find_element_by_id('chat_in')
        chat_in.send_keys("/d 20d20\n")
        chat_in.send_keys("/d 20d20 + 300d5\n")
        chat_in.send_keys("/d 20\n")

class InitiativeTest(BrowserTests):
    def runTest(self):
        self.chars = 0
        self.addchar("Sushi",10)
        self.addchar("top",100)
        self.addchar("bottom",0)

    def addchar(self, cname, init):
        self.formfiller('init_add', 'initname', cname, init)
        self.assertTrue(cd.find_element_by_id('init_i_{0}'.format(self.chars)))
        self.chars += 1


class CharTest(BrowserTests):
    def runTest(self):
        self.chars = 0
        self.addchar("Sooshknight", 100)

    def addchar(self, name, hp):
        self.formfiller('newchar_btn', 'addchar_m_name', name, hp)
        name = cd.find_element_by_id('addchar_m_name')