from selenium import webdriver
from pytest import mark


@mark.smoke
@mark.body
class BodyTests:

    @mark.ui
    def test_can_navigate_to_body_page(self):
        browser = webdriver.Chrome()
        browser.get('http://www.motortrend.com/')
        assert True
        
    def test_bumper(self):
        assert True

    def windshield(self):
        assert True