import micropip

await micropip.install("pango-collapse", deps=False)

from pango_collapse import Collapsor
from pango_collapse.utils import load_potential_parents_from_file
from pyodide.http import open_url
import csv
from pyscript import when, document, window

print("✅ Required packages loaded.")
btn = document.querySelector("#myfile")
btn.style.display ='block'
loading = document.querySelector("#loading")
loading.style.display ='none'

# At this point PyScript has already applied pyscript.json configuration,
btn.disabled = False

def build_table(data, headers):
	table = document.createElement('table')
	table.id = "table"
	header = table.createTHead()
	header_row = header.insertRow(0)
	for i, col_name in enumerate(headers):
		cell = header_row.insertCell(i)
		cell.innerHTML = f"<b>{col_name}</b>"
	tbody = table.createTBody()
	for row_data in data:
		row = tbody.insertRow()
		for i, col_name in enumerate(headers):
			cell = row.insertCell(i)
			cell.innerHTML = row_data.get(col_name, "")
	document.body.appendChild(table)


def download_table_as_csv(table_id):
	table = document.getElementById(table_id)
	rows = table.getElementsByTagName('tr')
	csv_content = []
	for row in rows:
		cells = row.getElementsByTagName('td')
		if cells.length == 0:
			cells = row.getElementsByTagName('th')
		row_data = []
		for cell in cells:
			row_data.append(cell.innerText)
		csv_content.append(','.join(row_data))
	csv_string = '\n'.join(csv_content)
	blob = window.Blob.new([csv_string], { "type": "text/csv" })
	url = window.URL.createObjectURL(blob)
	a = document.createElement('a')
	a.href = url
	a.download = 'collapsed_lineages.csv'
	document.body.appendChild(a)
	a.click()
	document.body.removeChild(a)
	window.URL.revokeObjectURL(url)

def copy_file_to_local(url):
	filename = url.split('/')[-1]
	with open(filename, 'w') as file:
		file.writelines(open_url((url)).readlines())

def collapse(data, lineage_col, collapse_col, expanded_col='Lineage_expanded'):

	copy_file_to_local('https://raw.githubusercontent.com/cov-lineages/pango-designation/master/pango_designation/alias_key.json')
	collapsor = Collapsor(alias_file="alias_key.json")
	collapse_file_url = document.getElementById("collapse_file").value
	copy_file_to_local(collapse_file_url)
	potential_parents = load_potential_parents_from_file("collapse.txt")
	collapsed_data = []
	for row in data:
		row[collapse_col] = collapsor.collapse(row[lineage_col], potential_parents)
		row[expanded_col] = collapsor.expand(row[lineage_col])
		collapsed_data.append(row)
	return collapsed_data


@when("change", "#myfile")
async def process_file(event):
	print("🚀 process_file called - file input detected!")
	table_el = document.getElementById("table")
	if table_el:
		print("📊 Removing existing table")
		table_el.remove()
	e = document.getElementById("loading")
	e.style.display ='block'
	print("⏳ Loading spinner displayed")

	lineage_col =     document.getElementById("lineage_col").value
	collapse_col =    'Lineage_family'
	expanded_col = 'Lineage_expanded'
	print(f"📝 Configuration - Lineage column: {lineage_col}")

	fileList = event.target.files.to_py()
	print(f"📁 Number of files selected: {len(fileList)}")
	for f in fileList:
		print(f"📄 Processing file: {f.name}")
		delimiter = ','
		if f.name.endswith('.tsv'):
			delimiter = '\t'
		file = await f.text()
		lines = file.split("\n")
		data = csv.DictReader(lines, delimiter=delimiter)
		collapsed_data = collapse(data, lineage_col, collapse_col, expanded_col=expanded_col)
		headers = data.fieldnames
		if collapse_col not in headers:
			headers += [collapse_col]
		if expanded_col not in headers:
			headers += [expanded_col]
		build_table(collapsed_data, headers=headers) 
		download_table_as_csv('table')
	e.style.display ='none'