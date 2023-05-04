const toggleBtn = document.querySelector('.navbar_toggleBtn');
const menu = document.querySelector('.navbar_menu');
const icons = document.querySelector('.navbar_icons');

toggleBtn.addEventListener('click', () => {
    menu.classList.toggle('active');
    icons.classList.toggle('active');
});



var thankYouMessage = form.querySelector(".thankyou_message");
    if (thankYouMessage) {
        thankYouMessage.style.display = "block";
    }


$(".close").click(function() {
    $(".thankyou_message").css("display", "none");
});


function jbSubmit() {
    // var pw1 = document.getElementById( 'pw1' ).value;
    // var pw2 = document.getElementById( 'pw2' ).value;
    alert('minji');
  }