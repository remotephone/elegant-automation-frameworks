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
sudo mv chromedriver /usr/bin/chromedriver
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
└─(06:44:06 on master ✖ ✹ ✭)──> pytest --env qa                                                                                                                                                                              1 ↵ ──(Fri,Jul29)─┘
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
└─(07:01:21 on master ✖ ✹ ✭)──> pytest --env qa -rs                                                                                                                                                                          1 ↵ ──(Fri,Jul29)─┘
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
└─(07:08:45 on master ✖ ✹ ✭)──> pytest --env qa -rsx                                                                                                                                                                         1 ↵ ──(Fri,Jul29)─┘
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

## Parameterization

### Doing it on the fly

Probably don't do this, but you can. 

Match the input you need in the function with what you're parametrizing. Gonna be a string, and we need to provide it an iterable to go through.

```py
from pytest import mark

@mark.parametrize('tv_brand', [
        ('Samsung'),
        ('Sony'),
        ('Vizio')
    ]
)
def test_television_turns_on(tv_brand):
    # This is a toy example to show we're going through different TVs
    print(f'{tv_brand} turns on as expected')
```

### 

When i add `params=[]` to the fixture, any test that calls this will run a test per parameter we pass.

```py
from pytest import fixture
from selenium import webdriver


@fixture(params=[webdriver.Chrome, webdriver.Firefox, webdriver.Edge])
def browser(request):
    driver = request.param
    drvr = driver()
    yield drvr
    drvr.quit()
```
Write one test and hit it with 3 different browsers

### Data Driven Testing

Create a fixture that loads a file and iterate through that

```py
conftest.py

data_path = 'test_data.json'

def load_test_data(path):
    with open(path) as data_file:
        data = json.load(data_file)
    return data


@fixture(params=load_test_data(data_path))
def tv_brand(request):
    data = request.param
    return data
```

## Speed it up

Install `pytest-xdist` and then just add the -nX flag where X is the number of threads

```python
└─(22:26:44 on master ✹ ✭)──> pytest -s -v -n4                                                                                                                                                             ──(Mon,Aug15)─┘
=================================================================================================== test session starts ===================================================================================================
platform linux -- Python 3.8.10, pytest-7.1.2, pluggy-1.0.0 -- /home/computer/.local/share/virtualenvs/elegant-automation-frameworks-7jaw7Dhg/bin/python
cachedir: .pytest_cache
metadata: {'Python': '3.8.10', 'Platform': 'Linux-5.10.102.1-microsoft-standard-WSL2-x86_64-with-glibc2.29', 'Packages': {'pytest': '7.1.2', 'py': '1.11.0', 'pluggy': '1.0.0'}, 'Plugins': {'forked': '1.4.0', 'metadata': '2.0.2', 'xdist': '2.5.0', 'html': '3.1.1'}}
rootdir: /home/computer/gits/elegant-automation-frameworks/code/section_4, configfile: pytest.ini
plugins: forked-1.4.0, metadata-2.0.2, xdist-2.5.0, html-3.1.1
[gw0] linux Python 3.8.10 cwd: /home/computer/gits/elegant-automation-frameworks/code/section_4
[gw1] linux Python 3.8.10 cwd: /home/computer/gits/elegant-automation-frameworks/code/section_4
[gw2] linux Python 3.8.10 cwd: /home/computer/gits/elegant-automation-frameworks/code/section_4
[gw3] linux Python 3.8.10 cwd: /home/computer/gits/elegant-automation-frameworks/code/section_4
[gw0] Python 3.8.10 (default, Mar 15 2022, 12:22:08)  -- [GCC 9.4.0]
[gw1] Python 3.8.10 (default, Mar 15 2022, 12:22:08)  -- [GCC 9.4.0]
[gw2] Python 3.8.10 (default, Mar 15 2022, 12:22:08)  -- [GCC 9.4.0]
[gw3] Python 3.8.10 (default, Mar 15 2022, 12:22:08)  -- [GCC 9.4.0]
gw0 [4] / gw1 [4] / gw2 [4] / gw3 [4]
scheduling tests via LoadScheduling

tests/test_chemistry_results.py::test_result_2_completes_as_expected 
tests/test_chemistry_results.py::test_result_3_completes_as_expected 
tests/test_chemistry_results.py::test_result_4_completes_as_expected 
tests/test_chemistry_results.py::test_result_1_completes_as_expected 
[gw2] PASSED tests/test_chemistry_results.py::test_result_3_completes_as_expected 
[gw0] PASSED tests/test_chemistry_results.py::test_result_1_completes_as_expected 
[gw3] PASSED tests/test_chemistry_results.py::test_result_4_completes_as_expected 
[gw1] PASSED tests/test_chemistry_results.py::test_result_2_completes_as_expected 

==================================================================================================== 4 passed in 3.48s ====================================================================================================
(elegant-automation-frameworks) ┌─(~/gits/elegant-automation-frameworks/code/section_4)────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────(computer@computer:pts/4)─┐
```

You won't get a lot of out this if you have only a few tests, but sometimes if you have a ton of tests, it will help.

You should write isolated tests for this. 


## Whitebox Testing

We know the code, we know what to test, write some unit tests.

- Tests should exist in tests/ directory outside of your module
    - keeps them from being included with a built module
    - __init__ files in module let your tests orient themselves and find the code
- Tests should check functionality of your code and follow its structure
    - if you wanna test functionality in myapp/feature folder, your tests should be in tests/feature

## Running Unit tests with tox

Creates separation of concerns between logic of library and logic of the tests. You don't need pytest for the library and it should be separate. tox does this.

`tox.ini` goes into the root of the direcotry
```
├── README.md
├── elegantcasing.egg-info
│   ├── PKG-INFO
│   ├── SOURCES.txt
│   ├── dependency_links.txt
│   └── top_level.txt
├── setup.py
├── tests
│   ├── pytest.ini
│   └── test_titlecase.py
├── titlecase
│   ├── __init__.py
│   └── titlecase.py
└── tox.ini              ### Here it is
```

This is functioning tox.ini file

```ini
[tox]
envlist = py38

[testenv]
deps = pytest
commands =
    pytest

[pytest]
python_classes = *Tests
python_functions = test_*
python_files = test_*
```

blamo.


## Functional Tests/Blackbox Testing


Write them I guess. This wasn't too illuminating. You're testing behavior of objects, your code is going to be more put in something and verify I get back what I expect instead of does this function do exactly what I think it will do.
