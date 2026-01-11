/*=============== SHOW HIDDEN - PASSWORD ===============*/
const showHiddenPass = (loginPass, loginEye) =>{
   const input = document.getElementById(loginPass),
         iconEye = document.getElementById(loginEye)

   if(input && iconEye) {
       iconEye.addEventListener('click', () =>{
          if(input.type === 'password'){
             input.type = 'text'
             iconEye.classList.add('ri-eye-line')
             iconEye.classList.remove('ri-eye-off-line')
          } else{
             input.type = 'password'
             iconEye.classList.remove('ri-eye-line')
             iconEye.classList.add('ri-eye-off-line')
          }
       })
   }
}

document.addEventListener("DOMContentLoaded", function() {
    showHiddenPass('login-pass','login-eye')
});