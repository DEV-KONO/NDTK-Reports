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

### REMOVED

17/07/2024

- Removed arrow controls for increasing and decreasing dimension values