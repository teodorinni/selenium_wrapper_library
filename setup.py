from setuptools import setup, find_packages

setup(
   name='selenium_wrapper',
   version='1.0.42',
   description='Wrapper for Selenium Webdriver',
   author='Fedor Nesterovich',
   author_email='fnesterovich@mfsadmin.com',
   packages=find_packages(),
   install_requires=['selenium', 'webdriver-manager']
)
