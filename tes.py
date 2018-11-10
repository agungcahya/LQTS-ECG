dic = {"John": "john@example.com", "Mary": "mary@example.com"} #dictionary

download_dir = "exampleCsv2.csv" #where you want the file to be downloaded to

csv = open(download_dir, "w")
#"w" indicates that you're writing strings to the file

columnTitleRow = "name, email\n"
csv.write(columnTitleRow)

for key in dic.keys():
	name = key
	email = dic[key]
	row = name + "," + email + "\n"
	csv.write(row)



print csv[0].split(',')[0]