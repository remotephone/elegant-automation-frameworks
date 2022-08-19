# Elegant Automation Frameworks with Python and Pytest

My notes from <https://www.udemy.com/course/elegant-automation-frameworks-with-python-and-pytest/>

## Folder Structure

If you follow along the videos, you'll have to move and shuffle things around as you go if you want to keep everything in one repo. As of my section_2, this is the folder structure I'm working with.

```bash
├── Pipfile
├── Pipfile.lock
├── README.md
├── code
│   ├── section_1
│   │   ├── conftest.py
│   │   ├── pytest.ini
│   │   ├── sportscar
│   │   └── test_widget.py
│   └── section_2
│       └── pytest.ini
├── notes
│   └── 01_intro.md
└── requirements.txt
```


## Ending notes

Good course, learned much about testing. To summarize:

- Test your code
- pytest.ini
- tox is cool, maybe not necessary 


Good example of minimal pytest.ini (in root of project)

```conf
[pytest]
python_functions = test_*
python_files = test_*
python_classes = *Tests

markers = 
    smoke: All critical smoke Tests
```