document.addEventListener('DOMContentLoaded', function(){
    window.addEventListener('offline', (e) => {
    // User is offline
    alert("You are disconnected from the Internet");
    })
});
function openNav() {
    document.getElementById("mySidebar").style.height = "400px";

    }

    /* Set the width of the sidebar to 0 and the left margin of the page content to 0 */
function closeNav() {
  document.getElementById("mySidebar").style.height = "0";
  document.getElementById("mysidebar").style.paddingtop = "0px";
}