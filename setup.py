from setuptools import setup, find_packages

setup(
   name='selenium_wrapper',
   version='1.0.48',
   description='Wrapper for Selenium Webdriver',
   author='Fedor Nesterovich',
   author_email='fnesterovich@mfsadmin.com',
   packages=find_packages(),
   install_requires=['selenium', 'webdriver-manager']
)
