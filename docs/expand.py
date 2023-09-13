try:
	from error_handler import errorHandler
	import asyncio
	from pyodide import create_proxy
	from jhanley_html import HTML
	from js import document
	import csv
	from pango_collapse import Collapsor
	from pango_collapse.utils import load_potential_parents_from_file
	from pyodide.http import open_url
except Exception as e:
	errorHandler(e)

def copy_file_to_local(url):
	filename = url.split('/')[-1]
	with open(filename, 'w') as file:
		file.writelines(open_url((url)).readlines())


async def expand_lineage(event):
	lineage = 	document.getElementById("lineage").value
	collapsor = Collapsor(alias_file="alias_key.json")
	expanded_lineage = collapsor.expand(lineage)
	e = document.getElementById("expanded")
	e.value = expanded_lineage
	full_lineage = collapsor.uncompress(lineage)
	e = document.getElementById("full")
	e.value = full_lineage
	print(expanded_lineage)

async def main():
	copy_file_to_local('https://raw.githubusercontent.com/cov-lineages/pango-designation/master/pango_designation/alias_key.json')
	# Create a Python proxy for the callback function
	lineage_event = create_proxy(expand_lineage)
	# Set the listener to the callback
	e = document.getElementById("lineage")
	e.addEventListener("change", lineage_event, False)

main()
