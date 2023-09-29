
# import required module
from pathlib import Path
import PyPDF2
import re
import datetime
import shutil
import argparse
try:
    from config import account_alias
except:
    account_alias = {}


parser = argparse.ArgumentParser()
parser.add_argument("--from", dest="from_path", help="Source path (%%P in Total Commander). Default: in", default="in")
parser.add_argument("--to", dest="to_path", help="Target path (%%T in Total Commander). Default: out", default="out")
parser.add_argument("--mode", help="copy or move the file.  Default: copy", choices=["copy","move"],default="copy")
args = parser.parse_args()

# assign directory
input_directory = args.from_path
output_directory = args.to_path
mode = args.mode
# print(input_directory,output_directory,mode)
# exit(1)
#Innbetalingsoversikt for konto: xxxx.xx.xxxx
#Dato31.07.2023

account_line_pattern = "\w+\sKontoutskrift nr. (?P<number>\d+) for konto (?P<account_number>[\d\.]+) i perioden (?P<from_date>[\d\.]+) - (?P<to_date>[\d\.]+) (?P<account_name>\w+)"
input_line_pattern = "Innbetalingsoversikt for konto: (?P<account_number>[\d\.]+)"
input_date_pattern = "Dato(?P<date>[\d\.]+)"


path_dict = {} # keys=from, value = to
 
# iterate over files in
# that directory
files = Path(input_directory).glob('*.pdf')
for file in files:
    # print(file)
    with open(file, 'rb') as pdfFileObj:
        pdfReader = PyPDF2.PdfReader(pdfFileObj)
        #print(len(pdfReader.pages))
        pageObj = pdfReader.pages[0]
        content = pageObj.extract_text()
        pdf_type = None
        content_list = content.split("\n")
        #print(content_list)
        if "Kontoutskrift" in content:
            pdf_type = "Kontoutskrift"
            transcript_matches = re.search(account_line_pattern, content)
            account_number = transcript_matches.group("account_number")
            account_type = transcript_matches.group("account_name")
            from_date = transcript_matches.group("from_date")
            to_date_str = transcript_matches.group("to_date")
            transcript_number = transcript_matches.group("number")
            to_date = datetime.datetime.strptime(to_date_str, "%d.%m.%Y").strftime("%Y%m%d")
            if account_number in account_alias:
                account_name = account_alias[account_number]
            else:
                account_name = account_type


            filename = f"{to_date}_{pdf_type}_{account_number}_{account_name}_{transcript_number}.pdf"
            #print(filename)
        elif "Innbetalingsoversikt" in content:
            pdf_type = "Innbetalingsoversikt"
            #print(content_list)
            date_matches = re.search(input_date_pattern, content)
            details_matches = re.search(input_line_pattern, content)
            #print(date_matches.group("date"))
            to_date_str = date_matches.group("date")
            to_date = datetime.datetime.strptime(to_date_str, "%d.%m.%Y").strftime("%Y%m%d")
            account_number = details_matches.group("account_number")
            if account_number in account_alias:
                account_name = "_"+account_alias[account_number]
            else:
                account_name = ""
            filename = f"{to_date}_{pdf_type}_{account_number}{account_name}.pdf"

        path_dict[file] = f"{output_directory}/{filename}"

    #print(pdf_type)

for input_file, output_file in path_dict.items():
    from_path = Path(input_file)
    to_path = Path(output_file)
    # Create the folder
    to_path.parent.mkdir(parents=True, exist_ok=True)
    if mode == "copy":
        #from_path.copy(to_path)
        shutil.copy(from_path, to_path)
    elif mode == "move":
        from_path.rename(to_path)
    elif mode == "symlink":
        to_path.symlink_to(from_path)
    else:
        print("Unknown mode")
    print(f"{input_file} -> {output_file}")

