# MendChallenge
Mend Coding Challenge

## Challenge

Reach out to https://www.senate.gov/general/contact_information/senators_cfm.xml and convert the XML data to the following JSON format. 
```
{
  “firstName”: “First”,
  “lastName”: “Last”,
  “fullName”: “First Last”,
  “chartId”: “:Contents of bioguide_id:”,
  “mobile”: “Phone”,
  “address”: [
    {
      “street”: “123 Main Street”,
      “city”: “Orlando”,
      “state”: “FL”,
      “postal”: 32825
    }
  ]
}
```
Then print out the results to stdout. 

---
## Dependencies
* Python 3.7 (May work with others, but program was created using 3.7)
---
## Instructions to run

  1. Clone the repository
    ```
    git clone https://github.com/Martakia/MendChallenge
    ```
  2. Install Python 3.7 if not installed already
  3. Call MendChallenge.py like below
  ```
  python MendChallenge.py
  ```
  * The program can also be output to a file for easier readability of results using `python MendChallenge.py > results.txt`
  
  * NOTE: If result analysis is automated, results have an empty line printed in between them for readability. This can be modified in SenatorChartConverter.py by removing line 100.
