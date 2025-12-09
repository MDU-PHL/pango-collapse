from js import console, document, window
from pyodide.ffi import create_proxy

class HTML:
	def init():
		self._id = None

	def __init__(self, id=None):
		if id is not None:
			self._id = id
			self._element = document.getElementById(id)

	def create(self, type, id, parent):
		self.__init__(None)
		self._element = document.createElement(type)
		if id is not None:
			self._element.id = id
		self._id = id

		if parent is None:
			document.body.appendChild(self._element)
		else:
			parent._element.appendChild(self._element)

		return self

	@property
	def element(self):
		return self._element

	@property
	def innerHTML(self):
		return self._element.innerHTML

	@innerHTML.setter
	def innerHTML(self, value):
		self._element.innerHTML = value
		return self

	@property
	def css(self):
		console.log(window.getComputedStyle(self._element))
		return window.getComputedStyle(self._element)

	@css.setter
	def css(self, value):
		self._element.setAttribute('style', value)

	# @property
	def test(self):
		styles = window.getComputedStyle(self._element)
		console.log(styles.fontSize)
		console.log(styles.padding)
		console.log(styles.backgroundColor)

	def bind_event(self, event_name, func):
		proxy = create_proxy(func)
		self._element.addEventListener(event_name, proxy)

	"""
	@property
	def style(self, name):
		styles = window.getComputedStyle(self._element)
		return styles.fontSize

		console.log(window.getComputedStyle(self._element, name))
		return window.getComputedStyle(self._element, name)
"""

	############################################################
	# HTML Table
	############################################################

	def table(self, id=None, parent=None, header_row=None, table_data=None):
		# t = HTML().create('table', id, parent)
		t = self.create('table', id, parent)

		self._thead = HTML().create("thead", None, t)

		if header_row is not None:
			row = HTML().create("tr", None, self._thead)
			for col in header_row:
				HTML().create("th", None, row).innerHTML = col

		self._tbody = HTML().create("tbody", None, t)

		if table_data is not None:
			for table_row in table_data:
				row = HTML().create("tr", None, self._tbody)
				for table_col in table_row:
					HTML().create("td", None, row).innerHTML = table_col

		return self

	def header_append(self, header_row):
		row = HTML().create("tr", None, self._thead)
		for col in header_row:
			HTML().create("th", None, row).innerHTML = col

		return self

	def row_append(self, row_data):
		row = HTML().create("tr", None, self._tbody)
		for table_col in row_data:
			HTML().create("td", None, row).innerHTML = table_col

		return self

	############################################################
	# HTML List
	############################################################

	def list(self, id=None, parent=None, items=None, ordered=False):
		if ordered is False:
			l = self.create('ul', id, parent)
		else:
			l = self.create('ol', id, parent)

		# l.css = 'display:block; list-style: decimal;'

		for item in items:
			HTML().create("li", None, l).innerHTML = item

		return self

	############################################################
	# HTML Anchor
	############################################################

	def anchor(self, label, href, target=None, id=None, parent=None):
		a = self.create('a', id, parent)

		a.innerHTML = label
		a._element.href = href

		if target is not None:
			a._element.target = target

		return self
