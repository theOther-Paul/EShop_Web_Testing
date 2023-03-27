# EShop_Web_Testing

## Description

This is a testing project on a Prestashop E-Commerce project, using Selenium, Pytest and Behave for the website testing, and ```randomuser.me/api``` for generating random 
users. 
These random users will be used in the testing process of the login flow. 

## Requirements

All requirements needed will be found in the ```requirements.txt``` file

## Utilities

Ps1 and batch scripts will be implemented for running all the tests at once, start servers, getting html reports and more

### Additional Files

- ```generate_new_users.py``` will be called whenever the test require a new set of data for a new user to be generated. <br>The functions inside will generate and store the 
data, in case we need to debug a problem, or to check something else. 
- ```helper.py``` is a collection of functions that is used to ease the test file of any non-testing function used by the test file 
- <i> to be added </i>