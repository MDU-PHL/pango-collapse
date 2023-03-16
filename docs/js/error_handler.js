window.addEventListener("error", function (e) {
	msg  = 'Error Handler\n';
	msg += e.error.message + '\n';
	msg += 'File: ' + e.filename + '\n';
	msg += 'Line: ' + e.lineno + '\n';
	msg += 'Error: ' + e.error + '\n';

	console.error(msg)
	alert(msg);
	return false;
})

function scriptLoadFailure(msg) {
	console.error('Script Load Failure', msg)
	alert('Script Load Failure\n' + msg)
}

window.addEventListener('unhandledrejection', event => {
	console.error('Unhandled Promise Rejection:', event.reason);
	alert("Unandled Promise Rejection: " + event.reason)
	return false;
});
