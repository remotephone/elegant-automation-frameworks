# Intro

## Setup

Install Pytest

`pipenv install pytest` - probably

### Install Selenium and Chrome and Chrome WebDriver

I seem to like to make things harder for myself, so I am doing this in Windows Subsystem for Linux instead of on Windows or a native OS. this breaks a few of the steps provided by the author.

This guide worked - <https://cloudbytes.dev/snippets/run-selenium-and-chrome-on-wsl2>

```bash
## Install Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt --fix-broken install
chrome_driver=$(curl "https://chromedriver.storage.googleapis.com/LATEST_RELEASE") && \
echo "$chrome_driver"
curl -Lo chromedriver_linux64.zip "https://chromedriver.storage.googleapis.com/\
${chrome_driver}/chromedriver_linux64.zip"
unzip chromedriver_linux64.zip
sudo mnv chromedrive /usr/bin/chromedriver
rm *.zip
```

I also had to modify the chromedriver fixture. This is an example of a working function

```python
def test_engine_functions_as_expected():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--window-size=1420,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.get('http://www.artofmanliness.com/')
    assert True
```

## pytest.ini

see pytest.ini, `[pytest]` starts the file. We can usually get away with a minimum of 3 configurations, what you test files look like, what the test functions look like, and what the classes should look like.

## Markers

delineate tests so we know what we want to run when

```python
from pytest import mark

@mark.engine 
def test_engine_functions_as_expected():
    assert True

```

Test only the tests you want to test with `pytest -m engine`. Document the ones you want to use and expose to other people in your pytest.ini file

## Smoke testing

Bare minimum tests to be sure the whole thing won't blow up. You can mark it a smoke test.

You can run smoke and engine tests with `pytest -m "smoke or engine"`.

## Classes to group tests

simplifies grouping tests together. You can add functions really easy, mark it once, boom it all runs (see [body tests](../code/section_1/sportscar/body/test_body.py))

## Fixtures

Any fixture created in conftest.py is accessible to any directory its in and anything under it! Just put it at the root of your tests folder

You don't have to import them either! Pytest does the magic.

### Fixture Setup

1. Create them in your `conftest.py` - There's a working example in this repo.
2. Create your function and import what you need
3. Make sure it returns what you want.
4. Modify your test function to take the fixture as an argument

```py title="conftest.py"
# conftest.py
from pytest import fixture

from selenium import webdriver

@fixture(scope='function')
def chrome_browser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--window-size=1420,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    return browser
```

```py
#my test
@mark.ui
@mark.entertainment
def test_can_navigate_to_entertainment_page(chrome_browser):
    chrome_browser.get('http://www.siriusxm.com/')
    assert True
```

## Reporting

This section does not spark joy for me. Convert it to html or convert it to something jenkins can read.

```py
sudo apt install lynx
pytest --html="results.html"
lynx results.html
```

Also export with `pytest --junitxml="results.xml"`

----

There's an arbitrary split here in my notes, section_2 code begins here

----

## Customizing Test Runs with CLI and Config files

We can use command line arguments to specify which tests we run, for example, for different environments.

This is a nice little syntax. It takes an argument and when you call the class later, depending on the value of the argument, it returns a dictionary with the values already set for you.

```python
        self.app_port = {
            'dev': 8080,
            'qa': 80
        }[env]
```

Since fixtures can use fixtures, in the [conftest.py](code/section_2/tests/conftest.py) file, we create session wide fixtures to retrieve the env variable and pass that to app_config, and hence Config, to get a prebuilt dictionary with what we need.

```python
??????(06:44:06 on master ??? ??? ???)??????> pytest --env qa                                                                                                                                                                              1 ??? ??????(Fri,Jul29)??????
============================================================================================================== test session starts ==============================================================================================================
platform linux -- Python 3.8.10, pytest-7.1.2, pluggy-1.0.0
rootdir: /home/computer/gits/elegant-automation-frameworks/code/section_2, configfile: pytest.ini
plugins: html-3.1.1, metadata-2.0.1
collected 3 items                                                                                                                                                                                                                               

test_environment.py .FF                                                                                                                                                                                                                   [100%]

=================================================================================================================== FAILURES ====================================================================================================================
____________________________________________________________________________________________________________ test_environment_is_dev ____________________________________________________________________________________________________________

app_config = <config.Config object at 0x7fb42c1d1b80>

    def test_environment_is_dev(app_config):
        base_url = app_config.base_url
        port = app_config.app_port
>       assert base_url == "https://mydev-env.com"
E       AssertionError: assert 'https://myqa-env.com' == 'https://mydev-env.com'
E         - https://mydev-env.com
E         ?           ^^^
E         + https://myqa-env.com
E         ?           ^^

test_environment.py:13: AssertionError
__________________________________________________________________________________________________________ test_environment_is_staging __________________________________________________________________________________________________________

app_config = <config.Config object at 0x7fb42c1d1b80>

    def test_environment_is_staging(app_config):
        base_url = app_config.base_url
        port = app_config.app_port
>       assert base_url == "staging"
E       AssertionError: assert 'https://myqa-env.com' == 'staging'
E         - staging
E         + https://myqa-env.com

test_environment.py:19: AssertionError
============================================================================================================ short test summary info ============================================================================================================
FAILED test_environment.py::test_environment_is_dev - AssertionError: assert 'https://myqa-env.com' == 'https://mydev-env.com'
FAILED test_environment.py::test_environment_is_staging - AssertionError: assert 'https://myqa-env.com' == 'staging'
========================================================================================================== 2 failed, 1 passed in 0.03s ==========================================================================================================
```

## Skipping tests

So don't skip things usually. If you're skipping it, you need to fix it or remove it. This is nice though because it at least calls out that you're skipping it. This is a skipped test

```python
from pytest import mark

@mark.skip(reason="broken by deploy, needs to be fixed")
def test_environment_is_staging(app_config):
    base_url = app_config.base_url
    port = app_config.app_port
    assert base_url == "staging"
```

This results in this output when you pass the -rs flag

```python
??????(07:01:21 on master ??? ??? ???)??????> pytest --env qa -rs                                                                                                                                                                          1 ??? ??????(Fri,Jul29)??????
============================================================================================================== test session starts ==============================================================================================================
platform linux -- Python 3.8.10, pytest-7.1.2, pluggy-1.0.0
rootdir: /home/computer/gits/elegant-automation-frameworks/code/section_2, configfile: pytest.ini
plugins: html-3.1.1, metadata-2.0.1
collected 3 items                                                                                                                                                                                                                               

test_environment.py .ss                                                                                                                                                                                                                   [100%]

============================================================================================================ short test summary info ============================================================================================================
SKIPPED [1] test_environment.py:12: broken by deploy, needs to be fixed
SKIPPED [1] test_environment.py:19: broken by deploy, needs to be fixed
========================================================================================================= 1 passed, 2 skipped in 0.02s ==========================================================================================================
```

So you could probably add `-rs` to your pytest config so it runs it every time. That would look like this

```ini
[pytest]
addopts = -rs
python_functions = test_*
python_files = test_*
python_classes = *Tests
```

## Tests that are supposed to Fail

You can use `@mark.xfail` to mark tests that are supposed to fail. Use -rsx to see xfail messages

```python
??????(07:08:45 on master ??? ??? ???)??????> pytest --env qa -rsx                                                                                                                                                                         1 ??? ??????(Fri,Jul29)??????
============================================================================================================== test session starts ==============================================================================================================
platform linux -- Python 3.8.10, pytest-7.1.2, pluggy-1.0.0
rootdir: /home/computer/gits/elegant-automation-frameworks/code/section_2, configfile: pytest.ini
plugins: html-3.1.1, metadata-2.0.1
collected 3 items                                                                                                                                                                                                                               

test_environment.py .sx                                                                                                                                                                                                                   [100%]

============================================================================================================ short test summary info ============================================================================================================
SKIPPED [1] test_environment.py:12: broken by deploy, needs to be fixed
XFAIL test_environment.py::test_environment_is_staging
  This has been deprecated, want to be sure it doesn't work
```

This isn't great though. Fix it, but this lets you know why its not fixed yet at least. 