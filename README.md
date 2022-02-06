# OBS Recon
**OBS Recon** is a python script created to download interesting files from open OBS buckets on HUAWEI Cloud. Files with certain extensions are downloaded and saved for information disclosure/cloud security misconfiguration analysis, or to even be sent to the SIEM for alerting SOC. 
# Installing
## Prerequisites
 - Python 2.7
## Dependencies
 - beautifulSoup
## Installation 

    $ git clone https://github.com/west-wind/OBS-Recon.git
    $ cd OBS-Recon
    $ python obs-recon.py
# Intended Use
The intention of this script is to find & download interesting files from open OBS buckets on HUAWEI Cloud. The idea is to ensure tenants configure OBS bucket security correctly. This can be used by HUAWEI Cloud Service Providers/Auditors to monitor open OBS bucketsby alerting SOC when an open bucket is found. 

It is the end user's responsibility to obey all applicable local, state and federal laws; and it is the end-users responsibility to obtain relevant authorisation from the OBS bucket tenant/owner prior to scan/download. Developer assume no liability and are not responsible for any misuse or damage caused by this program. 
# Getting Started
This script requires the user to input the extension of files this code needs to download in line 32 in - **exten** tuple. Finally, a list of OBS bucket URL's need to be saved as a TXT file -**url_list.txt** to the same directory the code is in. The code will read OBS bucket URL's from this file and scan the same and download files from these buckets.  

To begin

- Create TXT file with title -- url_list.txt with OBS bucket URL's and save to the OBS-Recon directory. 

    $ cd OBS-Recon
    $ python obs-recon.py

All the results will then be output to a csv file - **results.csv**.

## Output
As detailed above, if open buckets are found, files will be downloaded to the same directory this code resides. Additionally, the output CSV can be sent to a SIEM for parsing and correlation rule regarding open buckets can be created to alert SOC personnel.

## Reporting Errors
If you encounter an error, create an issue here. 

# Built With
 - Python
# Authors
Alex John, B. ([@Praetorian_GRD](https://twitter.com/Praetorian_GRD))
# License
Copyright (C) 2022 Alex John, B. This project is licensed under the MIT License - see the [LICENSE.md](https://raw.githubusercontent.com/west-wind/OBS-Recon/main/LICENSE) file for details.
