$( document ).ready(function() {

  /* This Page Used for Add custom CheckBox To all edits User form to toggle password
     also will used to show the current hashed password */
  let firstWait = 1500;
  let maxWait = 5000;
  let passwordVisiblity = false;
  let flaskWTFPasswordId = "#user_password";
  let labelId = "#toggle_label";
  /* add event listener on create button to display toggle custom password checkbox */

  // add eventlistener click to all edit buttons using map and this refer to current ainloop
   $("a[title='Edit Record']").map(function() {
     return this.addEventListener("click", getUserPasswordInput);
   })
    /* function to display the password content and hide it */
    function togglePassword(event){
      if ($(flaskWTFPasswordId)[0]){
        if ($(event.target).attr("data-status") && $(event.target).attr("data-status") == "false"){
          $(flaskWTFPasswordId).attr("type", "text");
          $(event.target).attr("data-status", "true");
          passwordVisiblity = true;
          $(labelId).text("Hide Password");
        } else {
          $(flaskWTFPasswordId).attr("type", "password");
          $(event.target).attr("data-status", "false");
          $(labelId).text("Show Password");
        }
        return true;
      }
      return false;
    }

    /* new custom function work with wtf, to add custom inputs to model views flask-admin
     and add callbacks and also api calles if needed */
    function CreateCustomJSWTFInput(type="checkbox"){
        if (!$('#togglepass')[0]){
          $('<label id="toggle_label" for="togglepass" style="font-size:13px;float: right;">'+
            'Show Password</label><input data-status="false" type="checkbox" id="togglepass" name="toggle_pass"' +
            'style="float: right;" class="m-1">')
          .insertAfter(flaskWTFPasswordId);
          $('#togglepass').click(togglePassword);
        }
      }

    /* function that check for userpassword input using wtf id and create the toggle content
     and apply the callback which togglepass function */
    function getUserPasswordInput(){
      setTimeout(function(){
        if ($(flaskWTFPasswordId)[0]){
          /* The user_passwrd generated within the firstWait */
          CreateCustomJSWTFInput();
        } else {
          setTimeout(function(){
            /* The user_passwrd generated after the firstWait and within the maxWait */
          CreateCustomJSWTFInput();
          }, maxWait);
        }
      },firstWait);
    }


    

});
