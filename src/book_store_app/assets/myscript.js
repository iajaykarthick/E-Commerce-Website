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

function sortbypriceformsubmit(){
  document.getElementById(`sortbyprice`).submit();
 }
 

 function disableCardForm(){

  document.getElementById("typeName").disabled = true;
  document.getElementById("typeExp").disabled = true;
  document.getElementById("typeText_1").disabled = true;
  document.getElementById("typeText_2").disabled = true;

 }

 function enableCardForm(){

  document.getElementById("typeName").disabled = false;
  document.getElementById("typeExp").disabled = false;
  document.getElementById("typeText_1").disabled = false;
  document.getElementById("typeText_2").disabled = false;

 }

 function submitPaymentForm(){
  document.getElementById(`submitPayment`).submit();
 }

 function openSearchParametersDropdown() {
  var searchdropdown = document.getElementById("mySearchDropdown")
  
  // .classList.toggle("show");
  var search_val = document.getElementById("searchvalue").value
  console.log(searchdropdown.classList.contains("show") && (search_val == null || search_val == ""))
  if (searchdropdown.classList.contains("show")) {
    if (search_val == null || search_val == "") {
    searchdropdown.classList.remove("show");
    }
  } else {
    if (search_val != null && search_val != "") {
      searchdropdown.classList.add("show");
    }
  }
}


function searchFormSubmit(param) {
  document.getElementById("search_parameter").value = param;

  document.getElementById(`searchForm`).submit();
}


function changeStore(store_id){
  document.getElementById(`changeStoreForm`).submit();
}