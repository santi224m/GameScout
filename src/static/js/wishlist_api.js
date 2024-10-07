/*
Add the current game to the user's wishlist
*/

const wishlist_btn = document.querySelector('#wishlist-btn');
wishlist_btn.addEventListener("click", add_to_wishlist);

async function add_to_wishlist(e) {
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