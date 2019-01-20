#!python
# FunctionalTests.py

from selenium import webdriver

vBrowser = webdriver.Firefox()
vBrowser.get('http://localhost:8000')

assert 'Django' in vBrowser.title
