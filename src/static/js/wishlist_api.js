/*
Add the current game to the user's wishlist
*/

const wishlist_btn = document.querySelector('#wishlist-btn');
$('.wishlist').on("click", function() {
  $(this).addClass("active");
  add_to_wishlist()
})

$(document).ready(async function() {
  data = await get_wishlist();
  parsed_url = window.location.href.split('/');
  steamapp_id = parsed_url[parsed_url.length - 1];
  steamapp_id = parseInt(steamapp_id);

  data.forEach(element => {
    if (element[0] == steamapp_id) {
      $('.wishlist').addClass("active");
    }
  });
})

async function add_to_wishlist() {
  parsed_url = window.location.href.split('/');
  steamapp_id = parsed_url[parsed_url.length - 1];
  steamapp_id = parseInt(steamapp_id);

  const response = await fetch('/api/add_wishlist_item', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({steamapp_id: steamapp_id})
  });

  const data = await response.json();

  console.log(data);
}

async function get_wishlist() {
  parsed_url = window.location.href.split('/');

  const response = await fetch('/api/get_wishlist_items', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
  });

  const data = await response.json();

  console.log(data);

  return data;
}