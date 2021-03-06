$(function() {
   $('#email').mailgun_validator({
     api_key: 'pubkey-babebd7b0c266949e4d46138e429596d',
     success: success_email,         // called when validator has returned
     error: validation_error,           // called when an error reaching the validator has occured
   });

   var email = false;
   var phone = false;

   $('#phone').keyup(check_number);
   $('#phone').blur(check_number);

   function check_number(){
     var newStr = $('#phone').val();
     newStr = newStr.replace(/\D/g,'');
     if (newStr.length){
       $.ajax({ url: "/phone/"+newStr }).done(function(resp) {
         console.log(resp)
         if (resp==="valid"){
           phone=true;
           check_inputs();
           $('#error').text("");
         } else if (resp==="invalid"){
           phone=false;
           check_inputs();
           $('#submit').prop("disabled", true);
           $('#error').text("Invalid Phone Number");
         } else {
           phone=false;
           check_inputs();
         }
       });
     }
   }

   function success_email(val){
     if (val.is_valid){
       email=true;
       check_inputs();
       $('#error').text("");
     } else {
       email=false;
       check_inputs();
       $('#submit').prop("disabled", true);
       $('#error').text("Invalid Email Address");
     }
   }

   function validation_error(val, two){
     console.log(val, two)
   }

   function check_inputs(){
     if (email && phone)
       $('#submit').prop("disabled", false);
     else
       $('#submit').prop("disabled", true);
   }

 });
