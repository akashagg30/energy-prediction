function ValidateFname(){
  console.log("validate f name");
  var name = document.form1.first_name;
  if(name.value == ''){
    return true;
  }
  var nameFormat = name.value.replace(/[^a-zA-Z ]+/, '');
  console.log(name.value.replace(/[^a-zA-Z]+/, ''));
  if(nameFormat != '' && nameFormat == name.value){
    return true;
  }
  else{
    document.getElementsByClassName("tooltiptextFname")[0].style.visibility = "visible";
    name.value = "";
    document.form1.first_name.focus();
    setTimeout(function(){
      document.getElementsByClassName("tooltiptextFname")[0].style.visibility = "hidden"; }, 3000);
    return false;
  }
}

function ValidateLname(){
  var name = document.form1.last_name;
  if(name.value == ''){
    return true;
  }
  var nameFormat = name.value.replace(/[^a-zA-Z ]+/, '');
  if(nameFormat != '' && nameFormat == name.value){
    return true;
  }
  else{
    document.getElementsByClassName("tooltiptextLname")[0].style.visibility = "visible";
    name.value = "";
    document.form1.last_name.focus();
    setTimeout(function(){
      document.getElementsByClassName("tooltiptextLname")[0].style.visibility = "hidden"; }, 3000);
    return false;
  }
}

 function ValidateUname(){
   var uname = document.form1.username;
   if(uname.value == ''){
     return true;
   }
   var unameFormat = uname.value.replace(/[^_a-zA-Z0-9]+/,'');
   console.log(unameFormat);
   if(unameFormat == uname.value){
     return true;
   }
   else{
     document.getElementsByClassName("tooltiptextUname")[0].style.visibility = "visible";
     uname.value = "";
     document.form1.username.focus();
     setTimeout(function(){
       document.getElementsByClassName("tooltiptextUname")[0].style.visibility = "hidden"; }, 3000);
     return false;
   }

 }


function ValidateEmail() {
  var inputText = document.form1.email;
  var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
  if(inputText.value=='' || inputText.value.match(mailformat)) {
    return true;
  }
  else {
    document.getElementsByClassName("tooltiptextEmail")[0].style.visibility = "visible";
    inputText.value = "";
    document.form1.email.focus();
    setTimeout(function(){
      document.getElementsByClassName("tooltiptextEmail")[0].style.visibility = "hidden"; }, 3000);
    return false;
  }
}

function ValidatePassword() {
  var inputText = document.form1.password1;
  if(inputText.value=='' || inputText.value.length>=8) {
    return true;
  }
  else{
    document.getElementsByClassName("tooltiptextPwd")[0].style.visibility = "visible";
    inputText.value = "";
    document.form1.password1.focus();
    setTimeout(function(){
      document.getElementsByClassName("tooltiptextPwd")[0].style.visibility = "hidden"; }, 3000);
    return false;
  }
}

function CheckPwdMatch(){
  var confirmPwd = document.form1.password2;
  var pwd = document.form1.password1;
  if(confirmPwd.value=='' || pwd.value==confirmPwd.value) {
    return true;
  }
  else{
    document.getElementsByClassName("tooltiptextConfirmPwd")[0].style.visibility = "visible";
    confirmPwd.value = "";
    document.form1.password2.focus();
    setTimeout(function(){
      document.getElementsByClassName("tooltiptextConfirmPwd")[0].style.visibility = "hidden"; }, 3000);
    return false;
  }
}
