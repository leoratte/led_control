function calculateBrightness(rgb, a) {
	for(i = 0; i < rgb.length; i++) {
		rgb[i] = Math.floor(rgb[i] * a);
	}
	return rgb;
}

function sendRGB(rgb){
	var led = document.getElementById("selectLed").value;
	ws.send(JSON.stringify({"name":led,
							"type":"static",
							"color":rgbToHex(rgb).substring(1,7)}));
	return 0;
}

function setLedHex(hex){
	var rgb = [0,0,0];
	for(i = 0; i < 3;i++){
		rgb[i] = parseInt("0x"+hex.substring(i*2+1, i*2+3));
	}
	var a = document.getElementById("aValSelect").value;
	rgb = calculateBrightness(rgb,a);
	sendRGB(rgb);
	return 0;
}

function animation(animationType){
	var speed = document.getElementById("speed").value;
	var led = document.getElementById("selectLed").value;
	ws.send(JSON.stringify({"name":led,
							"type":"animation",
							"animationType":animationType,
							"animationSpeed":speed}));
	return 0;
}

function setLed(){
	var rgb = getRGB();
	var a = document.getElementById("aValManual").value;
	rgb = calculateBrightness(rgb, a);
	sendRGB(rgb);
	return 0;
}

function getRGB(){
	var r = document.getElementById("rVal").value;
	var g = document.getElementById("gVal").value;
	var b = document.getElementById("bVal").value;
	return [r, g, b];
}

function rgbToHex(rgb){
	var ret = "#";
	for(i = 0; i<3; i++) {
		var hex = Number(rgb[i]).toString(16);
		if (hex.length < 2) {
			hex = "0" + hex;
		}
		ret += hex;
	}
  return ret;
}

function preview() {
	var rgb = getRGB();
	var a = document.getElementById("aValManual").value;
	rgb = calculateBrightness(rgb, a);
	var hex = rgbToHex(rgb);
	document.getElementById("preview").style.background = hex;
	return 0;
}

function readConfig(data){
	config = JSON.parse(data);
	config.leds.forEach(addOption)
	return 0;
}

function addOption(item){
	var x = document.getElementById("selectLed");
	var option = document.createElement("option");
	option.text = item;
	option.value = item;
	x.add(option); 
	return 0;
}

function show(page){
	document.getElementById("colorSelection").style.display = "none";
	document.getElementById("manualColorSelection").style.display = "none";
	document.getElementById("animationSelection").style.display = "none";
	document.getElementById(page).style.display = "inline";
}

document.addEventListener("DOMContentLoaded", function(){
			var slider = document.getElementsByTagName("input");
			for(i = 0; i < slider.length;i++){
				slider[i].addEventListener("input", preview);
			}
	    });



var ip = "localhost"
var ws = new WebSocket("ws://"+ip+":6789");
ws.onmessage = function (event) {
  readConfig(event.data);
}
window.onload = preview;

