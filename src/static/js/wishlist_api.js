/*
Add the current game to the user's wishlist
*/

$('.wishlist').on("click", function() {
  $(this).addClass("active");
  add_to_wishlist();
})

$(document).ready(async function() {
  is_wishlisted = await is_game_wishlisted();

  if (is_wishlisted) $('.wishlist').addClass("active");
});

/*
Async Functions
*/

async function add_to_wishlist() {
  // Add current game to user's wishlist
  steamapp_id = get_url_steamapp_id();

  const response = await fetch('/api/add_wishlist_item', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({steamapp_id: steamapp_id})
  });

  const data = await response.json();
}

async function is_game_wishlisted() {
  steam_app_id = get_url_steamapp_id();
  const response = await fetch('/api/is_game_wishlisted', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({steamapp_id: steamapp_id})
  });

  const data = await response.json();
  return data;
}

async function get_wishlist() {
  const response = await fetch('/api/get_wishlist_items', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
  });

  const data = await response.json();

  return data;
}

/*
Helper functions
*/

function get_url_steamapp_id() {
  steamapp_id = $(".game-title").attr("data-steamid");
  steamapp_id = parseInt(steamapp_id);
  return steamapp_id;
}