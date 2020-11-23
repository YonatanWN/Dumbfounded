function joinGame() {
	var pin = document.getElementById("gamepintxtdiv");
	var join = document.getElementById("joinButton");
	var create = document.getElementById("creationButton");
	var make = document.getElementById("mode")
	pin.style.display = "none";
	if (pin.style.display === "none") {
		pin.style.display = "block";
		join.style.display = "none";
		create.style.display = "none";
		make.value = "join";
	}
}

function backGame() {
    var pin = document.getElementById("gamepintxtdiv");
	var join = document.getElementById("joinButton");
	var create = document.getElementById("creationButton");
	var make = document.getElementById("mode")
	pin.style.display = "block";
	if (pin.style.display === "block") {
		pin.style.display = "none";
		join.style.display = "block";
		create.style.display = "block";
		make.value = "make";
	}
}
function avatarZero(){
	new_source1 = document.getElementById('av0');
	new_source1.src = "../../static/Images/codeyColor.png";
    document.getElementById('avatar0').checked = true;
	new_source2 = document.getElementById('av1');
	new_source2.src = "../../static/Images/franUnfilled.png";
	new_source3 = document.getElementById('av2');
	new_source3.src = "../../static/Images/robertUnfilled.png";
	new_source4 = document.getElementById('av3');
	new_source4.src = "../../static/Images/oscarUnfilled.png";
}
function avatarOne(){
	new_source1 = document.getElementById('av0');
	new_source1.src = "../../static/Images/codeyUnfilled.png";
	new_source2 = document.getElementById('av1');
	new_source2.src = "../../static/Images/franColor.png";
    document.getElementById('avatar1').checked = true;
	new_source3 = document.getElementById('av2');
	new_source3.src = "../../static/Images/robertUnfilled.png";
	
	new_source4 = document.getElementById('av3');
	new_source4.src = "../../static/Images/oscarUnfilled.png";
}
function avatarTwo(){
	new_source1 = document.getElementById('av0');
	new_source1.src = "../../static/Images/codeyUnfilled.png";
	new_source2 = document.getElementById('av1');
	new_source2.src = "../../static/Images/franUnfilled.png";
	new_source3 = document.getElementById('av2');
	new_source3.src = "../../static/Images/robertColor.png";
    document.getElementById('avatar2').checked = true;
	new_source4 = document.getElementById('av3');
	new_source4.src = "../../static/Images/oscarUnfilled.png";
}
function avatarThree(){
	new_source1 = document.getElementById('av0');
	new_source1.src = "../../static/Images/codeyUnfilled.png";
	new_source2 = document.getElementById('av1');
	new_source2.src = "../../static/Images/franUnfilled.png";
	new_source3 = document.getElementById('av2');
	new_source3.src = "../../static/Images/robertUnfilled.png";
	new_source4 = document.getElementById('av3');
	new_source4.src = "../../static/Images/oscarColor.png";
    document.getElementById('avatar3').checked = true;
}

function cap(){
    textbox = document.getElementById('gamepintxt')
    textbox.value = textbox.value.toUpperCase()
}
