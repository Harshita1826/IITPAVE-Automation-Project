import os
import subprocess
from openpyxl import Workbook
import re


#defining constants
E_granular = 240.2
E_subgrade = 76.8
thickness_granular = 450
thickness_DBM = 100
poisson_ratio = 0.35
tyre_radius = 0.56
wheel_load = 20000


E1_values = [2000, 2500, 3000, 3500, 4000]
E2_values = [300, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
h1_values = [40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 110.0, 120.0, 130.0, 140.0, 150.0]


#opening excel
wb = Workbook()
default_sheet = wb.active
wb.remove(default_sheet)


#defining paths for input output files and .exe path
exe_path= "IITPFILE.exe"
output_path= "iitpave.out"
input_path = "IITPAVE.in"


for E2 in E2_values:
    sheet = wb.create_sheet(title=f"E2_{E2}")
    sheet.append([
        "E1", "E1/E2", "h1", 
        "sigz_h1", "sigt_h1", "sigr_h1", "tau_h1", "epz_h1", "ept_h1", "epr_h1", 
        "sigz_h1/2", "sigt_h1/2", "sigr_h1/2", "tau_h1/2", "epz_h1/2", "ept_h1/2", "epr_h1/2",
    ])
    for E1 in E1_values:
        for h1 in h1_values:
            with open(input_path, "w") as f:  #opening and writing input values in input file
                f.write("4\n")
                f.write(f"{E1} {E2} {E_granular} {E_subgrade}\n")
                f.write(f"{poisson_ratio} {poisson_ratio} {poisson_ratio} {poisson_ratio}\n")
                f.write(f"{h1} {thickness_DBM} {thickness_granular}\n")
                f.write(f"{wheel_load} {tyre_radius}\n")
                f.write("2\n")
                f.write(f"{h1} 0\n")
                f.write(f"{h1/2} 0\n")
                f.write("2\n") 

        
            subprocess.run([exe_path], check=True)  #running the IITPAVE software


            values = {
                "h1": {},  # Z = h1
                "h1/2": {}  # Z = h1/2
            }

            with open(output_path, "r") as f:
                for line in f:
                    
                    parts = re.findall(r'[-+]?\d*\.\d+(?:[Ee][-+]?\d+)?', line)  #use regex module to extract all numbers (including scientific notation) from the line
                    if len(parts) >= 9:
                        try:
                            z = float(parts[0].replace("L", ""))
                            r = float(parts[1])
                            if r!=0:
                                continue
                            data = {
                                "sigz": parts[2],
                                "sigt": parts[3],
                                "sigr": parts[4],
                                "tau": parts[5],
                                "epz": parts[7],
                                "ept": parts[8],
                                "epr": parts[9],
                            }
                            if z-h1==0:
                                values["h1"] = data
                            elif z-(h1/2)==0:
                                values["h1/2"] = data
                        except:
                            continue

            
            # write in excel
            row = [E1, round(E1 / E2, 2), h1]

            # Add values at depth h1
            for key in ["sigz", "sigt", "sigr", "tau", "epz", "ept", "epr"]:
                row.append(values["h1"].get(key, ""))

            # Add values at depth h1/2
            for key in ["sigz", "sigt", "sigr", "tau", "epz", "ept", "epr"]:
                row.append(values["h1/2"].get(key, ""))

            sheet.append(row)

            

#save the excel sheet
excel_path = "IITPAVE_Results_Tabular.xlsx"
wb.save(excel_path)








#4
#2000 300 240.2 76.8 
#0.35 0.35 0.35 0.35 
#40 100 450 
#20000 0.56
#2
#40 0
#20 0
#2
