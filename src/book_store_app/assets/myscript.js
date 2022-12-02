function reset_register_form() {
    document.getElementById('register_form').reset();
}


function alertFunc() {
    // Get the snackbar DIV
    var x = document.getElementById("snackbar");
  
    // Add the "show" class to DIV
    x.className = "show";
  
    // After 3 seconds, remove the show class from DIV
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
  }

  function deleteCartItem(isbn) {
    console.log(`${isbn}`)
    document.getElementById(`deleteCartItemForm_${isbn}`).submit();
  }

  function addToCartFunc(){
    document.getElementById(`addToCart`).submit();
  }


  function increment(quantity_id) {
    document.getElementById(`quantity_${quantity_id}`).stepUp();
 }
 function decrement(quantity_id) {
    document.getElementById(`quantity_${quantity_id}`).stepDown();
 }