var content1=document.getElementById('content1');
var content2=document.getElementById('content2');
var content3=document.getElementById('content3');
var btn1=document.getElementById('btn1');
var btn2=document.getElementById('btn2');
var btn3=document.getElementById('btn3');

function openTrain(){
  content1.style.transform = "translateX(0)";
  content2.style.transform = "translateX(500%)";
  content3.style.transform = "translateX(500%)";
  btn1.style.color = "orange";
  btn2.style.color = "black";
  btn3.style.color = "black";
}

function openWeather(){
  content1.style.transform = "translateX(500%)";
  content2.style.transform = "translateX(0)";
  content3.style.transform = "translateX(500%)";
  btn1.style.color = "black";
  btn2.style.color = "orange";
  btn3.style.color = "black";
}

function openBuilding(){
  content1.style.transform = "translateX(500%)";
  content2.style.transform = "translateX(500%)";
  content3.style.transform = "translateX(0)";
  btn1.style.color = "black";
  btn2.style.color = "black";
  btn3.style.color = "orange";
}

function getFile() {
  document.getElementById("inputfile").click();
}

function upload(obj){
  var file = obj.value;
  var fileName = file.split("\\");
  document.getElementById("fileBtn").innerHTML = fileName[fileName.length - 1];
}
