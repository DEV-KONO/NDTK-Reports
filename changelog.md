# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

####

### ADDED

12/07/2024

- Client Name dropdown
- Other Client Name dropdown
- Plant name dropdown
- Other plant name dropdown
- Contact Name dropdown
- Other Contact Name dropdown

15/07/2024

- added send all btn for sending new client with plant and contact name to the db
- "Other" data is sent and saved in the database but just when other client is selected

16/07/2024

- text added so you can know if data is missing when uploading a new client (plant and contact name)
- Button for sending other data added

17/07/2024

- added inch/milimeter switch
- added thickness validation
- added height validation
- added ut instrument connection to the database so it shows in the dropdown

23/07/24

- aded Nde specifications and acceptance criteria tables to db and made relations to clients table
- added api call to make a new NDE Specification and Acceptance Criteria
- added api calls to show all nde specifications for client and all acceptance criteria for nde specification
- added api calls to make and show acabados superficiales from the database into the app
- added textfields to type the surface roughness, with a default value of 250, and another textfield for the measurement of the surface roughness

26/07/24

- Added Bottom Navigation Bar
- Added new file for the administration section

1/08/2024

- Added salt and hashes to passwords
- Added Firebase Authentication
- Login page now functional
- Added error message in case the email doesn't exist

2/08/2024

- Added textareas for adding new clients

5/08/2024

- Added function to change the textfield with accepted or rejected values 

12/08/2024

- Added api endpoint to validate the existence of an inspector
- Added api endpoint to add new inspectors

13/08/2024

- Added api endpoint to return all users from the admin table
- Added api endpoint to give or take admin privileges from user
- Made new dropdown to select the user and give or take admin privileges

05/09/2024

- Added new api endpoint to return all distances by client from the distance table

06/09/2024

- Added new api endpoints to return all elements from calibration blocks and scanning direction from their respective tables

### CHANGED

15/07/2024

- Default values for plant and contact dropdowns when client name is selected
- The api uses json body requests instead of query parameters
- changed the query parameters for the report to a schema

16/07/2024

- Dropdown reloads when adding another client
- Plant and Contact dropdowns select the newely entered data as default

17/07/2024

- added decimal point restrictions to dimensions in part information
- od and id are always greater than 0
- id is less than od always
- Removed s from NDE Specifications now NDE Specification
- UT Instrument changed into a dropdown combo

19/07/2024

- Image shows on pdf when downloaded
- now the pdf is downloaded and the data is sent by a dictionary

22/07/2024

- Changed the test calibration setup into a dropdown

24/07/2024

- Modified the nde textbox and changed it into a dropdown with the nde specifications grabbed from the DB
- Modified the acceptance criteria textbox and changed it into a dropdown with the acceptance criteria data grabbed from the DB
- Modified the Surface Roughness textfield into a dropdown that grabs the "Acabado superficial" from the DB

02/08/2024

- Api endpoint for adding clients now checks if the client already exists

05/06/2024

- changed default values for measure and coupling agent
- change default value for accepted/rejected values in checkbox
- added height change 

06/06/2024

- changed the sn label in the sn textbox from s/n to sn

09/08/2024

- added number input filter into serial number textbox

12/08/2024

- now you can add inspectors from the admin screen and they reload each time you enter the main screen

12/08/2024

- added a restriction to the inspector adder so you cant add a blank inspector
- changed the title of the admin page from admin to admin dashboard

05/09/2024

- Changed the distance textbox into a dropdown and connected to the database

06/09/2024

- Changed calibration blocks and scanning direction section text boxes into dropdowns

12/09/2024

- Changed the last blocks into dropdowns

17/09/2024

- Changed distance database from client related to global
- Changed notch database from client related to global
- Changed sensitivity database from client related to global

27/09/2024

- Changed Scanning database from client related to global
- Changed inspection method, stage and coupling agent from client related to global

4/10/2024

- Changed acabado and add acabado from client related to global in the database
- Changed NDE and NDE criteria from client related to global

20/10/2024

- Changed value of ndt activitiess to perform and evaluate

21/10/2024

- changed the calibration model to several tables to save information individually

22/11/2024

- Changed the way the test calibration setup is added

29/11/2024
 
- Removed the delete button from the row and moved it to the side of the dropdown, it will delete the last element of the data table

2/12/2024

- Started debugging issue that causes the app to not load the dropdowns

### REMOVED

17/07/2024

- Removed arrow controls for increasing and decreasing dimension values