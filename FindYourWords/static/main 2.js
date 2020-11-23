function joinGame() {
	var pin = document.getElementById("gamepintxtdiv");
	var join = document.getElementById("joinButton");
	var create = document.getElementById("creationButton");
	pin.style.display = "none";
	if (pin.style.display === "none") {
		pin.style.display = "inline-block";
		join.style.display = "none";
		create.style.display = "none";
	}
}

function createGame(){
	var code = document.getElementById("codeTxtBox");
	var join = document.getElementById("joinButton");
	var create = document.getElementById("creationButton");
	code.style.display = "none";
	if (code.style.display === "none") {
		code.style.display = "inline-block";
		join.style.display = "none";
		create.style.display = "none";
	}
}