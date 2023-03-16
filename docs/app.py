try:
	from error_handler import errorHandler
	import asyncio
	from pyodide import create_proxy
	from jhanley_html import HTML
	from js import document, FileReader, download_table_as_csv
	import csv
	from pango_collapse import Collapsor
	from pango_collapse.utils import load_potential_parents_from_file
	from pyodide.http import open_url
except Exception as e:
	errorHandler(e)

def build_table(data, headers):
	table_data = []

	for item in data:
		entry = []
		for k in item:
			entry.append(item[k])

		table_data.append(entry)

	HTML().table(header_row=headers, table_data=table_data, id='table')

def copy_file_to_local(url):
	filename = url.split('/')[-1]
	with open(filename, 'w') as file:
		file.writelines(open_url((url)).readlines())

def collapse(data, lineage_col, collapse_col):
	copy_file_to_local('https://raw.githubusercontent.com/cov-lineages/pango-designation/master/pango_designation/alias_key.json')
	collapsor = Collapsor(alias_file="alias_key.json")
	copy_file_to_local("https://raw.githubusercontent.com/MDU-PHL/pango-collapse/main/pango_collapse/collapse.txt")
	potential_parents = load_potential_parents_from_file("collapse.txt")
	collapsed_data = []
	for row in data:
		row[collapse_col] = collapsor.collapse(row[lineage_col], potential_parents)
		collapsed_data.append(row)
	return collapsed_data

async def process_file(event):
	table_el = document.getElementById("table")
	if table_el:
		table_el.remove()
	e = document.getElementById("loading")
	e.style.display ='block'

	collapse_col = 	document.getElementById("collapse_col").value
	lineage_col = 	document.getElementById("lineage_col").value

	fileList = event.target.files.to_py()
	for f in fileList:
		delimiter = ','
		if f.name.endswith('.tsv'):
			delimiter = '\t'
		file = await f.text()
		lines = file.split("\n")
		data = csv.DictReader(lines, delimiter=delimiter)
		collapsed_data = collapse(data, lineage_col, collapse_col)
		headers = data.fieldnames
		if collapse_col not in headers:
			headers += [collapse_col]
		build_table(collapsed_data, headers=headers) 
		download_table_as_csv('table')
	e.style.display ='none'

async def main():
	# Create a Python proxy for the callback function
	# process_file() is your function to process events from FileReader
	file_event = create_proxy(process_file)

	# Set the listener to the callback
	e = document.getElementById("myfile")
	e.addEventListener("change", file_event, False)

main()
