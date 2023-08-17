// test






// $(document).ready(function() {

  $('.minus-cart, .plus-cart').parent().hide();

 

  $('.plus-cart').click(function(){
      // var id =$(this).attr("pid").toString();
      // var eml = this.parentNode.children[2];
      var id = $(this).attr('pid'); // Get the product ID
      var quantityElements = $('.quantityCounter-' + id); // Get all quantity elements with the specific class name
      var quantity = parseInt(quantityElements.first().text()); // Get the current quantity from the first element
      // console.log("pid= ", id)
      console.log("quantity" , quantity);
      if(quantity > 0) { //make sure add to cart has added quantity
          $.ajax({
              type:"GET",
              url:"/pluscart",
              data:{
                  prod_id:id
              },
              success:function(data){
                  // console.log("data= ", data);
                  quantityElements.text(data.quantity);
                  // document.getElementById("amount").innerText=data.amount
                  // document.getElementById("totalamount").innerText=data.totalamount
              }
              
          })
      }
  })

  $('.add-to-cart').click(function(){

    var quantity = document.getElementById("quantityCounter");
    var id = $(this).attr('pid'); // Get the product ID
    var quantityElements = $('.quantityCounter-' + id); // Get all quantity elements with the specific class name
    $.ajax({
        type:"GET",
        url:"/add-to-cart",
        data:{
            prod_id:id
        },
        success:function(data){
            console.log("add to cart =", data.message);
            console.log("data",data.quantity);
            $('#quantityCounter-' + id).text(data.quantity);
            $('.add-to-cart-' + id).parent().hide();
            $('.minus-cart-' + id + ', .plus-cart-' + id).parent().show();
            quantityElements.text(data.quantity);
    
            // document.getElementById("amount").innerText=data.amount
            // document.getElementById("totalamount").innerText=data.totalamount
        }
    });

    
  });



  $('.minus-cart').click(function() {
    // var id = $(this).attr("pid").toString();
    // var eml = this.parentNode.children[2];
    var id = $(this).attr('pid'); // Get the product ID
    var quantityElements = $('.quantityCounter-' + id); // Get all quantity elements with the specific class name
    var quantity = parseInt(quantityElements.first().text()); // Get the current quantity from the first element
    
    if (quantity > 1) {
      $.ajax({
        type: "GET",
        url: "/minuscart",
        data: {
          prod_id: id
        },
        success: function(data) {
          console.log("data= ", data);
          quantityElements.text(data.quantity);
          // document.getElementById("amount").innerText = data.amount;
          // document.getElementById("totalamount").innerText = data.totalamount;
        }
      });
    } else {
      $.ajax({
        type: "GET",
        url: "/removecart",
        data: {
          prod_id: id
        },
        success: function(data) {
          // document.getElementById("amount").innerText = data.amount;
          // document.getElementById("totalamount").innerText = data.totalamount;
          console.log("remove by minus...");
          // eml.parentNode.remove();
          $('#quantityCounter-' + id).text('0');
          $('.minus-cart-' + id + ', .plus-cart-' + id).parent().hide();
          $('.add-to-cart-' + id).parent().show();
        }
      });
    }
  });



//   $('.remove-cart').click(function(){
//     var id =$(this).attr("pid").toString();
//     var eml = this

//     $.ajax({
//         type:"GET",
//         url:"/removecart",
//         data:{
//             prod_id:id
//         },
//         success:function(data){
//             // document.getElementById("amount").innerText=data.amount
//             // document.getElementById("totalamount").innerText=data.totalamount
//             eml.parentNode.parentNode.parentNode.parentNode.remove()
//         }

//     })
// })

$('[id^="quantityCounter-"]').each(function() {
  var id = $(this).attr('id').split('-')[1]; // Get the product ID
  var quantityElement = $(this); // Store the quantity element

  $.ajax({
    type: "GET",
    url: "/getquantity", // Replace with the appropriate URL to fetch the quantity
    data: {
      prod_id: id
    },
    success: function(data) {
      var quantity = parseInt(data.quantity);
      console.log("the item Qt:   ", quantity);

      if (quantity > 0) {
        $('.add-to-cart-' + id).parent().hide();
        $('.minus-cart-' + id + ', .plus-cart-' + id).parent().show();
      }

      // Update the quantity element with the fetched value
      quantityElement.text(quantity);
    }
  });
});
// }); //end of ready()

// widhlist
$(document).ready(function() {
    $(document).on('click', '.plus-wishlist', function() {
      var id = $(this).attr("pid").toString();
      var heartIcon = $(this).find('svg');
      var heartButton = $(this);
      $.ajax({
        type: "GET",
        url: "/pluswishlist",
        data: {
          prod_id: id
        },
        success: function(data) {
          heartIcon.attr('data-prefix', 'fas'); // Update the data-prefix attribute
          heartButton.removeClass('plus-wishlist').addClass('minus-wishlist');
  
          console.log("Plus Should be clicked");
        }
      });
    });
  
    $(document).on('click', '.minus-wishlist', function() {
      var id = $(this).attr("pid").toString();
      var heartIcon = $(this).find('svg');
      var heartButton = $(this);
      $.ajax({
        type: "GET",
        url: "/minuswishlist",
        data: {
          prod_id: id
        },
        success: function(data) {
          heartIcon.attr('data-prefix', 'far'); // Update the data-prefix attribute
          heartButton.removeClass('minus-wishlist').addClass('plus-wishlist');
  
          console.log("Minus Should be clicked");
        }
      });
    });
  });
  
  
