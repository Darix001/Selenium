import os,time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium import webdriver

def wait():
    for i in range(10):
        time.sleep(1)

class Youtube_Search(object):
    def __init__(self):
        super(Youtube_Search, self).__init__()
        self.service = Service(executable_path=os.getcwd().replace('\\','/')+"/edgedriver")
        self.driver = webdriver.Edge(service=self.service)
        self.driver.get("https://www.youtube.com/")
        assert self.driver.title.lower()=='youtube'
        print("Youtube Page correctly charged.")
        self.search_box=self.driver.find_element(by=By.XPATH, 
            value="//input[@id='search']")
        self.button_search=self.driver.find_element(by=By.XPATH, 
            value="//button[@id='search-icon-legacy']")
        self.topic=''

    def set_topic(self,topic):
        self.topic=topic
        self.search_box.send_keys(topic)
        assert self.search_box.get_attribute('value') == topic
        print('TextBox Filled Sucessfully')

    def search_topic(self):
        if not self.topic:
            raise Exception("The topic hasn't been set up.")
        self.search_box.send_keys(Keys.ENTER)
        self.button_search.click()
        wait()
        assert self.driver.title.lower()==f'{self.topic.lower()} - youtube'
        print('Searching the video')

    def clear_search(self):
        self.search_box.clear()
        assert self.search_box.get_attribute('value')==''
        print('Search Box cleared.')
        self.topic=''

    def search_by_url(self,url):
        self.driver.get(url)
        # wait for the page to load everything (works without it)
        video = self.driver.find_element(by=By.ID,value='movie_player')
        video.send_keys(Keys.SPACE) #hits space
        time.sleep(1)
        try:
            video.click()
        except Exception as e:
            return False
        else:
            return True

    def __enter__(self):
        return self

    def __exit__(self,*args):
        self.driver.quit()
        del self

if __name__ == '__main__':
    with Youtube_Search() as youtube:
        youtube.set_topic("APRENDE PYTHON")
        youtube.search_topic()
        youtube.clear_search()
        assert youtube.search_by_url("https://www.youtube.com/watch?v=chPhlsHoEPo")