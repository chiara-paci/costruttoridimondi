from django.conf import settings

from selenium.common.exceptions import NoSuchElementException

class Page(object):
    def __init__(self, test):
        self.test = test  

    def url(self):
        return self.test.browser.current_url

    def body(self):
        return self.test.browser.find_element_by_tag_name('body').text

    def click_on_link(self,txt,title=None):
        self.test.browser.find_element_by_link_text(txt).click()
        if title==None:
            self.test.wait_browser()
            return
        self.test.wait_for(lambda: self.test.assertTrue(self.has_title(title)))

    def click_on_mystories_link(self):
        self.click_on_link("My stories",title="My Stories")
        return MyStoriesPage(self.test)

    def logout(self):
        self.click_on_link("Log out")
        self.test.wait_browser()
        return HomePage(self.test)

    def login_request(self,email):
        inputbox= self.test.browser.find_element_by_name('email')
        inputbox.send_keys(email)
        inputbox.send_keys(u'\ue007')
        self.test.wait_browser()
        return HomePage(self.test)
        
    def login(self,url):
        self.test.browser.get(url)
        self.test.wait_browser()
        return LoginPage(self.test)

    def has_my_stories(self):
        return bool(self.test.browser.find_elements_by_link_text('My stories'))

    def has_win_title(self,win_title):
        return win_title in self.test.browser.title

    def has_title(self,title):
        header_text = self.test.browser.find_element_by_tag_name('h1').text
        return title in header_text

    def is_logged_in(self):
        try:
            logoutlink=self.test.browser.find_element_by_link_text('Log out')
        except NoSuchElementException:
            return False
        return bool(logoutlink)

    def is_logged_out(self):
        return not self.is_logged_in()

    def is_logged_in_user(self,email):
        navbar = self.test.browser.find_element_by_css_selector('.navbar')
        return email in navbar.text

    def is_logged_out_user(self,email):
        return not self.is_logged_in_user(email)

class AddSectionMixin(object):
    def get_section_input(self):
        return self.test.browser.find_element_by_id('id_text')

    def get_error_box(self):
        error = self.test.browser.find_element_by_css_selector('.has-error')
        return error

    def add_empty_section(self):
        inputbox = self.get_section_input()
        inputbox.send_keys("")
        inputbox.send_keys(u'\ue007')
        self.test.wait_browser()
        error=self.get_error_box()
        self.test.assertEqual(error.text, "You can't have an empty section")
        return self

class HomePage(Page,AddSectionMixin):

    def go_to_home_page(self):  
        self.test.browser.get(self.test.server_url)
        self.test.wait_for(self.get_section_input)
        return self  

    def start_new_story(self, section_text):  
        self.go_to_home_page()
        inputbox = self.get_section_input()
        inputbox.send_keys(section_text)
        inputbox.send_keys(u'\ue007')
        self.test.wait_browser()
        if self.url()==self.test.server_url+"/writing/new":
            return self
        story_page = StoryPage(self.test)  
        story_page.wait_for_new_section_in_story(section_text, 1)  
        return story_page  

    def add_section(self,section_text): return self.start_new_story(section_text)

    def email_has_sent(self):
        body = self.test.browser.find_element_by_tag_name('body')
        return 'Check your email' in body.text

class StoryPage(Page,AddSectionMixin):

    def get_story_table_rows(self):
        return self.test.browser.find_elements_by_css_selector('#id_story_table tr')

    def get_story_table_size(self):
        return len(self.get_story_table_rows())

    def get_shared_with_story(self):
        return self.test.browser.find_elements_by_css_selector('.story-sharee')

    def get_share_box(self):
        return self.test.browser.find_element_by_css_selector('input[name=email]')

    def check_for_row_in_story_table(self, row_text,position):
        table = self.test.browser.find_element_by_id('id_story_table')
        rows = table.find_elements_by_tag_name('tr')
        expected_row = '{}: {}'.format(position, row_text)
        self.test.assertIn(expected_row, [row.text for row in rows])

    def add_section(self,text):
        L=self.get_story_table_size()
        inputbox = self.get_section_input()
        inputbox.send_keys(text)
        inputbox.send_keys(u'\ue007')
        self.wait_for_new_section_in_story(text, L+1)  
        return self

    def add_duplicate_section(self,text,position):
        inputbox = self.get_section_input()
        inputbox.send_keys("")
        inputbox.send_keys(u'\ue007')
        self.test.wait_browser()
        self.check_for_row_in_story_table(text,position)
        error=self.get_error_box()
        self.test.assertEqual(error.text, "You can't have an empty section")
        return self

    def wait_for_new_section_in_story(self, section_text, position):
        expected_row = '{}: {}'.format(position, section_text)
        self.test.wait_for(lambda: self.test.assertIn(expected_row,
                                                      [row.text for row in self.get_story_table_rows()] ))

    def share_story_with(self, email):
        self.get_share_box().send_keys(email + '\n')
        
        f=lambda: self.test.assertIn(email,
                                     [item.text for item in self.get_shared_with_story()])

        self.test.wait_for(f)

    def get_story_owner(self):
        return self.test.browser.find_element_by_id('id_story_owner').text

class LoginPage(Page):
    pass

class MyStoriesPage(Page): 
    def click_on_story_link(self,txt):
        self.click_on_link(txt)
        return StoryPage(self.test)

