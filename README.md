Numerology API
A FastAPI service for calculating numerology-based metrics including Basic Number, Destiny Number, Numerology Grid, Mahadasha Sequence, Antardasha Year Number, Monthly Dasha, and Day Lord.
Overview
This API provides endpoints to compute various numerology calculations based on a user's date of birth (DOB) and, where applicable, a specified year or date. All endpoints expect the DOB in DD-MM-YYYY format and return JSON responses with the calculated numerology data and a numerology grid.
Endpoints
1. Full Numerology Package
GET /numerology?dob=DD-MM-YYYY&year=YYYY
Computes all numerology metrics for a given DOB and year, including Basic Number, Destiny Number, Numerology Grid, Mahadasha Sequence, Antardasha Year Number, and Monthly Dasha.

Query Parameters:
dob: Date of birth in DD-MM-YYYY format (required).
year: Year for Antardasha and Monthly Dasha calculations (required).


Response:
Basic_Number: Single-digit number derived from the day of birth.
Destiny_Number: Single-digit number derived from the full DOB.
Numerology_Grid: Dictionary showing the count of digits 1–9 in the DOB and derived numbers.
Mahadasha_Sequence: List of planetary periods from birth year to 2030.
Antardasha_Year_Number: Single-digit number for the specified year.
Monthly_Dasha: List of monthly periods for the specified year.


Example:GET /numerology?dob=15-08-1990&year=2025

{
  "Basic_Number": 6,
  "Destiny_Number": 5,
  "Numerology_Grid": {"1": 2, "2": 1, "3": 0, "4": 0, "5": 2, "6": 1, "7": 0, "8": 1, "9": 1},
  "Mahadasha_Sequence": [
    {"MD_Number": 6, "Planet": "Venus", "Start_Year": 1990, "End_Year": 1996},
    ...
  ],
  "Antardasha_Year_Number": 4,
  "Monthly_Dasha": [
    {"Start_Number": 4, "Days": 32, "Start_Date": "15-Aug", "End_Date": "16-Sep"},
    ...
  ]
}



2. Basic Number
GET /basic-number?dob=DD-MM-YYYY
Computes the Basic Number and Numerology Grid based on the DOB.

Query Parameters:
dob: Date of birth in DD-MM-YYYY format (required).


Response:
Basic_Number: Single-digit number derived from the day of birth.
Grid: Numerology grid with digit counts.


Example:GET /basic-number?dob=15-08-1990

{
  "Basic_Number": 6,
  "Grid": {"1": 2, "2": 1, "3": 0, "4": 0, "5": 2, "6": 1, "7": 0, "8": 1, "9": 1}
}



3. Destiny Number
GET /destiny-number?dob=DD-MM-YYYY
Computes the Destiny Number and Numerology Grid based on the DOB.

Query Parameters:
dob: Date of birth in DD-MM-YYYY format (required).


Response:
Destiny_Number: Single-digit number derived from the full DOB.
Grid: Numerology grid with digit counts.


Example:GET /destiny-number?dob=15-08-1990

{
  "Destiny_Number": 5,
  "Grid": {"1": 2, "2": 1, "3": 0, "4": 0, "5": 2, "6": 1, "7": 0, "8": 1, "9": 1}
}



4. Numerology Grid
GET /grid?dob=DD-MM-YYYY
Computes the Numerology Grid based on the DOB.

Query Parameters:
dob: Date of birth in DD-MM-YYYY format (required).


Response:
Grid: Dictionary showing the count of digits 1–9.


Example:GET /grid?dob=15-08-1990

{
  "Grid": {"1": 2, "2": 1, "3": 0, "4": 0, "5": 2, "6": 1, "7": 0, "8": 1, "9": 1}
}



5. Mahadasha Sequence
GET /mahadasha?dob=DD-MM-YYYY
Computes the Mahadasha Sequence from the birth year to 2030 and the Numerology Grid.

Query Parameters:
dob: Date of birth in DD-MM-YYYY format (required).


Response:
Mahadasha: List of planetary periods with start and end years.
Grid: Numerology grid with digit counts.


Example:GET /mahadasha?dob=15-08-1990

{
  "Mahadasha": [
    {"MD_Number": 6, "Planet": "Venus", "Start_Year": 1990, "End_Year": 1996},
    ...
  ],
  "Grid": {"1": 2, "2": 1, "3": 0, "4": 0, "5": 2, "6": 1, "7": 0, "8": 1, "9": 1}
}



6. Antardasha Year Number
GET /antardasha?dob=DD-MM-YYYY&year=YYYY
Computes the Antardasha Year Number for a specific year and the Numerology Grid.

Query Parameters:
dob: Date of birth in DD-MM-YYYY format (required).
year: Year for Antardasha calculation (required).


Response:
Antardasha_Year_Number: Single-digit number for the year.
Grid: Numerology grid with digit counts.


Example:GET /antardasha?dob=15-08-1990&year=2025

{
  "Antardasha_Year_Number": 4,
  "Grid": {"1": 2, "2": 1, "3": 0, "4": 0, "5": 2, "6": 1, "7": 0, "8": 1, "9": 1}
}



7. Monthly Dasha
GET /monthly-dasha?dob=DD-MM-YYYY&year=YYYY
Computes the Monthly Dasha periods for a specific year and the Numerology Grid.

Query Parameters:
dob: Date of birth in DD-MM-YYYY format (required).
year: Year for Monthly Dasha calculation (required).


Response:
Monthly_Dasha: List of monthly periods with start/end dates and days.
Grid: Numerology grid with digit counts.


Example:GET /monthly-dasha?dob=15-08-1990&year=2025

{
  "Monthly_Dasha": [
    {"Start_Number": 4, "Days": 32, "Start_Date": "15-Aug", "End_Date": "16-Sep"},
    ...
  ],
  "Grid": {"1": 2, "2": 1, "3": 0, "4": 0, "5": 2, "6": 1, "7": 0, "8": 1, "9": 1}
}



8. Day Dasha
GET /day-dasha?dob=DD-MM-YYYY&date=DD-MM-YYYY&month_num=N
Computes the Day Lord information for a specific date and month number, along with the Numerology Grid.

Query Parameters:
dob: Date of birth in DD-MM-YYYY format (required).
date: Specific date in DD-MM-YYYY format (required).
month_num: Month number (1–9) for calculation (required).


Response:
Day_Dasha: Dictionary with date, day lord, month number, and day number.
Grid: Numerology grid with digit counts.


Example:GET /day-dasha?dob=15-08-1990&date=15-08-2025&month_num=5

{
  "Day_Dasha": {
    "Date": "15-Aug-2025",
    "Day_Lord": 1,
    "Month_Number": 5,
    "Day_Number": 6
  },
  "Grid": {"1": 2, "2": 1, "3": 0, "4": 0, "5": 2, "6": 1, "7": 0, "8": 1, "9": 1}
}



Error Handling

Invalid DOB or Date: Returns a 400 status code with the message "Provide valid DOB in DD-MM-YYYY" or "Provide valid date in DD-MM-YYYY".
Year Range: DOB years must be between 1900 and 2100.

Notes

The Mahadasha Sequence is calculated up to the year 2030. Future enhancements may allow a dynamic end year.
All endpoints include the Numerology Grid for consistency.
Ensure the year parameter for /antardasha and /monthly-dasha is reasonable (e.g., not before the DOB or far in the future).
