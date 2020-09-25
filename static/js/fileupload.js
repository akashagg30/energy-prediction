function getFile1() {
    document.getElementById("inputfile1").click();
  }
  
  function getFile2() {
    document.getElementById("inputfile2").click();
  }
  
  function getFile3() {
    document.getElementById("inputfile3").click();
  }
  
  function upload1(obj){
    var file = obj.value;
    var fileName = file.split("\\");
    document.getElementById("fileBtn1").innerHTML = fileName[fileName.length - 1];
  }
  
  function upload2(obj){
    var file = obj.value;
    var fileName = file.split("\\");
    document.getElementById("fileBtn2").innerHTML = fileName[fileName.length - 1];
  }
  
  function upload3(obj){
    var file = obj.value;
    var fileName = file.split("\\");
    document.getElementById("fileBtn3").innerHTML = fileName[fileName.length - 1];
  }