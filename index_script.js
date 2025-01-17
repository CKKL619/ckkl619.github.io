function resizeIFrameToFitContent(iFrame) {
    iFrame.width = iFrame.contentWindow.document.body.scrollWidth;
    iFrame.height = iFrame.contentWindow.document.body.scrollHeight;
}

window.addEventListener('DOMContentLoaded', function() {
    var iFrame = document.getElementById('iFrame');
    resizeIFrameToFitContent(iFrame);
});

function logoutConfirm(){
	let text = "Press OK to logout";
	if (confirm(text) == true) {
		window.location.href = "login.html" ;
	}else{
		window.location.href = "index.html";
  }
}