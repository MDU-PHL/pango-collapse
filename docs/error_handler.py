import sys
from js import alert, console

def errorHandler(e):
	exception_type, exception_object, exception_traceback = sys.exc_info()
	filename = exception_traceback.tb_frame.f_code.co_filename
	lineno = exception_traceback.tb_lineno

	msg  = 'Exception Type: ' + str(exception_type) + '\n'
	msg += 'File: ' + filename + '\n'
	msg += 'Line: ' + str(lineno) + '\n'
	msg += str(e)

	console.error(msg)
	alert(msg)

