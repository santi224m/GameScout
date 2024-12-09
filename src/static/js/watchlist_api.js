/*
Add the current game to the user's watchlist
*/

$('.watchlist').on("click", async function() {
  // Wishlist if not wishlisted, remove from wishlist otherwise
  is_watchlisted = await is_game_watchlisted();

  if (is_watchlisted["error"] == 500) {
    $("div.toast").fadeIn(500)
    setTimeout(function() {$("div.toast").fadeOut(500)}, 2000)
    return
  }

  if (!is_watchlisted) {
    $(this).addClass("active");
    add_to_watchlist();
  } else {
    $(this).removeClass("active");
    delete_from_watchlist();
  }
})

$(document).ready(async function() {
  is_watchlisted = await is_game_watchlisted();
  
  if (is_watchlisted && !is_watchlisted["error"]) $('.watchlist').addClass("active");
});

/*
Async Functions
*/

async function add_to_watchlist() {
  // Add current game to user's wishlist
  steamapp_id = get_steamapp_id();

  const response = await fetch('/api/add_watchlist_item', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({steamapp_id: steamapp_id})
  });

  const data = await response.json();
}

async function delete_from_watchlist() {
  // Delete current game from user's wishlist
  steamapp_id = get_steamapp_id();

  const response = await fetch('/api/delete_watchlist_item', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({steamapp_id: steamapp_id})
  });

  const data = await response.json();
}

async function is_game_watchlisted() {
  steam_app_id = get_steamapp_id();
  const response = await fetch('/api/is_game_watchlisted', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({steamapp_id: steamapp_id})
  });

  const data = await response.json();
  return data;
}

/*
Helper functions
*/

function get_steamapp_id() {
  steamapp_id = $(".game-title").attr("data-steamid");
  steamapp_id = parseInt(steamapp_id);
  return steamapp_id;
}