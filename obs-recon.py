
# ----------------------------------------------------------------------------- README ------------------------------------------------------------------------------

# OBS RECON v 1.0

# This code makes an HTTP GET request to a list of OBS URL's (expected in url_list.txt - make sure URL don't end with '/' - format https://www.google.com ) 
# & generates a CSV file with the HTTP status code followed by parsing the various fields and writes them to the CSV file, provided the HTTP request was successful. 
# Please add file types extensions of the files you want to download to 'exten' tuple.

# Tested on Python 2.7

# RELEASE NOTES 1.0: 
# Final build after testing with various types of input XML from various OBS. Generating domain name & date for use by SIEM.  


# AUTHOR: Alex John, B


# Run the following commands to install libraries.
# pip install urllib3
# pip install beautifulSoup
# pip install re
# pip install csv
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------

from bs4 import BeautifulSoup
import urllib3, re, csv, shutil, httplib, os, ssl, time
from datetime import datetime
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Add the extensions of file types you want the scanner to download =================================================================================================
exten = ('.docx','.xlsx','.txt','.sql','.csv','.gz','.zip')

# HTML CLEANER ======================================================================================================================================================
def cleanhtml(val):
  clean_can = re.compile('<.*?>')
  cleanedtext = re.sub(clean_can, '', val)
  return cleanedtext

# GET DOMAIN OF OBS BUCKET URL ======================================================================================================================================
def getdom(furl):
    s1 = furl.split('.obs')
    cleaned = s1[0].replace('https://','')
    return cleaned

# HTTP REQUEST METHOD ===============================================================================================================================================
def http_req(url,meth):
    try:
        http = urllib3.PoolManager(cert_reqs = ssl.CERT_NONE)
        headers = urllib3.make_headers(keep_alive=True, user_agent='OBS Recon v1.0 GitHub west-wind/OBS-Recon')
        response = http.request(meth, url, headers=headers)
        response.release_conn()
        return response
    except Exception as e:
        time.sleep(5)
        pass

# HTTP DOWNLOAD METHOD ==============================================================================================================================================
def http_download(base_url, url, file_title):
    try:
        s = base_url.replace("https://","")
        dir_name = s + "/" + file_title + "/"
        s1 = file_title.replace("/","")
        os.makedirs(dir_name)
    except OSError as exc:
        pass
    try:
        conn = urllib3.PoolManager(cert_reqs = ssl.CERT_NONE)
        headers = urllib3.make_headers(keep_alive=True, user_agent='OBS Recon v1.0 GitHub west-wind/OBS-Recon')
        with conn.request('GET',url, preload_content=False, headers=headers) as resp, open(dir_name + s1, 'wb') as out_file:
            shutil.copyfileobj(resp, out_file)
        resp.release_conn()
    except Exception as e:
        time.sleep(5)
        pass

# WRITES TO CSV FILE ================================================================================================================================================
def write_to_file(rows_val):
    with open("results.csv", "a") as inp_file:
        writer = csv.writer(inp_file)
        writer.writerow(rows_val)

# MAIN FUNCTION =====================================================================================================================================================

row_1 = ['Date & Time','Domain','OBS URL','HTTP Request Status','File Name','Size','HTTP File Request Status','Extension']
write_to_file(row_1)
with open('url_list.txt') as f:
    lines = f.readlines()
for line in lines:
    print "\n[+] Checking URL:", line.strip()
    try:
        response = http_req(line.strip(),'GET')
        d_and_t = str(datetime.now())
        domain = getdom(line.strip())
        soup = BeautifulSoup(response.data, 'xml')
        http_status = response.status
        print "    Response: ", http_status
        if http_status == 200:
            if soup.find_all("Contents"):
                print ""
            else:
                row_s = [d_and_t,domain,line.strip(),http_status]
                write_to_file(row_s)
            for element in soup.find_all("Contents"):
                for i,j in zip(element.find_all("Key"),element.find_all("Size")):
                    row_s = [d_and_t, domain, line.strip(),http_status]
                    clean_e1 = cleanhtml(str(i))
                    clean_e2 = cleanhtml(str(j))
                    new_url = line.strip() + "/" + clean_e1
                    if clean_e1.endswith(exten) == True and clean_e1 != '':
                        row_s += [new_url,clean_e2]
                        try:
                            response = http_req(new_url.strip(), 'HEAD')
                            http_status = response.status
                            row_s += [http_status,os.path.splitext(clean_e1)[1]]
                            write_to_file(row_s)
                            # CHECKS FILE SIZE -- WILL ONLY DOWNLOAD IF IT'S LESS THAN 1 MB. CHANGE THE FILE SIZE HERE.
                            # NOTE THAT, DOWNLOADING LARGER FILE SIZES WILL PROLONG THE RUNTIME. 
                            if int(clean_e2) < 100000000:
                                print "    Going to download. File Download HEAD Response: ", http_status
                                http_download(line.strip(), new_url, clean_e1)
                        except Exception as download_e:
                            pass
                            row_s += ["Exception Occured","Exception Occured"]
                            write_to_file(row_s)
                    else:
                        row_s += [new_url,clean_e2]
                        try:
                            response = http_req(new_url.strip(), 'HEAD')
                            http_status = response.status
                            print "    File Response: ", http_status
                            row_s += [http_status,os.path.splitext(clean_e1)[1]]
                            write_to_file(row_s)
                        except Exception as non_down_e:
                            pass
                            row_s += ["Exception Occured","Exception Occured"]
                            write_to_file(row_s)
        else:
            row_s = [d_and_t,domain,line.strip(),http_status]
            write_to_file(row_s)
    except Exception as main_e:
        print main_e
        pass
        # FINAL FAIL SAFE CODE
        row_s = [d_and_t,domain,line.strip(),"Exception Occured"]