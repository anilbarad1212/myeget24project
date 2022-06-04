$("#slider1, #slider2, #slider3").owlCarousel({
  loop: true,
  margin: 20,
  responsiveClass: true,
  responsive: {
    0: {
      items: 1,
      nav: false,
      autoplay: true,
    },
    600: {
      items: 3,
      nav: true,
      autoplay: true,
    },
    1000: {
      items: 5,
      nav: true,
      loop: true,
      autoplay: true,
    },
  },
});

$(".plus-cart").click(function () {
  var id = $(this).attr("pid").toString();
  var eml = this.parentNode.children[2];
  $.ajax({
    type: "GET",
    url: "/pluscart/",
    data: {
      prodd_id: id,
    },
    success: function (data) {
      console.log(data);
      eml.innerText = data.quantity;
      document.getElementById("amount").innerText = data.amount;
      document.getElementById("total-amount").innerText = data.amount;
    },
  });
});

$(".minus-cart").click(function () {
  var id = $(this).attr("pid").toString();
  var eml = this.parentNode.children[2];
  $.ajax({
    type: "GET",
    url: "/minuscart/",
    data: {
      proddd_id: id,
    },
    success: function (data) {
      console.log(data);
      eml.innerText = data.quantity;
      document.getElementById("amount").innerText = data.amount;
      document.getElementById("total-amount").innerText = data.amount;
    },
  });
});

$(".remove-cart").click(function () {
  var id = $(this).attr("pid").toString();
  var eml = this;
  console.log(id);
  $.ajax({
    type: "GET",
    url: "/removecart/",
    data: {
      prodc_id: id,
    },
    success: function (data) {
      console.log("Delete");
      document.getElementById("amount").innerText = data.amount;
      document.getElementById("total-amount").innerText = data.amount;
      eml.parentNode.parentNode.parentNode.parentNode.remove();
    },
  });
});

var a = $("#amount").val($("#total_price").html());
console.log(a);

document.paytm.submit();
