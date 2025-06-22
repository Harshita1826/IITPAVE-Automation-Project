# IITPAVE-Automation-Project
This project automates the flexible pavement response analysis using IITPAVE software. It generates multiple input cases, runs analysis through the .exe file, parses the output, and compiles all stress-strain results into an Excel workbook.

**Problem Statement**

Manually analyzing multiple pavement sections in IITPAVE is time-consuming. This project aims to automate:

• Input generation (E1, E2, h1)

• Running the IITPAVE analysis for each case

• Extracting output values (σz, σt, σr, τrz, εz, εt, εr)

• Storing results in a structured Excel file

**How It Works**

• The Python script does the following:

• Generates IITPAVE.in files for each combination of E1 (BC modulus), E2 (DBM modulus) and h1 (BC thickness)

• Runs IITPFILE.exe (the IITPAVE executable)

• Reads the iitpave.out file and extracts stress & strain values at (1) bottom of BC layer (depth = h1) and (2) mid-depth of BC layer (depth = h1/2)

• Writes results to excel using openpyxl, for each value of E2 new worksheet is created

**Technologies Used**

• Language- Python 3

• openpyxl library– for writing Excel files

• subprocess module– to run .exe from Python

• re module– to parse scientific notation values

• IITPAVE.exe – flexible pavement analysis tool
