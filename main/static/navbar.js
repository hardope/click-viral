$(document).ready(function(){
    window.onoffline = function(){
        alert("😞 Looks like You are disconnected from the Internet");
    }
    window.ononline = function(){
        alert("😀 Your Internet connection was restored");
    }
});
function openNav() {
    $("#mySidebar").css("height", "400px");
    }

    /* Set the width of the sidebar to 0 and the left margin of the page content to 0 */
function closeNav() {
  $("#mySidebar").css("height", "0px");
}