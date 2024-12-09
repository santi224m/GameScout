/*
Add the current game to the user's wishlist
*/

let wishlist_status;

$('.wishlist').on("click", async function() {
  // Wishlist if not wishlisted, remove from wishlist otherwise
  let id = $(this).attr("data-steamid")

  if (wishlist_status[id]["error"] == 500) {
    $("div.toast").fadeIn(500)
    setTimeout(function() {$("div.toast").fadeOut(500)}, 2000)
    return
  }

  if (wishlist_status[id]) {
    wishlist_status[id] = false;
    $(this).removeClass("active");
    delete_from_wishlist(id);
  } else {
    wishlist_status[id] = true;
    $(this).addClass("active");
    add_to_wishlist(id);
  }
})

let watchlist_status;

$('.watchlist').on("click", async function() {
  // Wishlist if not wishlisted, remove from wishlist otherwise
  let id = $(this).attr("data-steamid")

  if (watchlist_status[id]["error"] == 500) {
    $("div.toast").fadeIn(500)
    setTimeout(function() {$("div.toast").fadeOut(500)}, 2000)
    return
  }

  if (watchlist_status[id]) {
    watchlist_status[id] = false;
    $(this).removeClass("active");
    delete_from_watchlist(id);
  } else {
    watchlist_status[id] = true;
    $(this).addClass("active");
    add_to_watchlist(id);
  }
})

$(document).ready(async function() {
  steamids = get_steamapp_ids();

  wishlist_status = await are_games_wishlisted(steamids);

  for(id in wishlist_status) {
    if (!wishlist_status[id] || wishlist_status[id]["error"] == 500) continue
    $(`.wishlist[data-steamid="${id}"]`).addClass("active")
  }

  watchlist_status = await are_games_watchlisted(steamids);

  for(id in watchlist_status) {
    if (!watchlist_status[id] || watchlist_status[id]["error"] == 500) continue
    $(`.watchlist[data-steamid="${id}"]`).addClass("active")
  }
});

/*
Async Functions
*/

async function add_to_wishlist(id) {
  // Add current game to user's wishlist
  const response = await fetch('/api/add_wishlist_item', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({steamapp_id: id})
  });

  const data = await response.json();
}

async function delete_from_wishlist(id) {
  // Delete current game from user's wishlist
  const response = await fetch('/api/delete_wishlist_item', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({steamapp_id: id})
  });

  const data = await response.json();
}

async function is_game_wishlisted(id) {
  const response = await fetch('/api/is_game_wishlisted', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({steamapp_id: id})
  });

  const data = await response.json();
  return data;
}

async function are_games_wishlisted(steamids) {
  let data = {}
  
  for(id in steamids) {
    if (steamids[id] == "") continue;
    data[steamids[id]] = await is_game_wishlisted(steamids[id]);
  }

  return data
}



async function add_to_watchlist(id) {
  // Add current game to user's wishlist
  const response = await fetch('/api/add_watchlist_item', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({steamapp_id: id})
  });

  const data = await response.json();
}

async function delete_from_watchlist(id) {
  // Delete current game from user's wishlist
  const response = await fetch('/api/delete_watchlist_item', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({steamapp_id: id})
  });

  const data = await response.json();
}

async function is_game_watchlisted(id) {
  const response = await fetch('/api/is_game_watchlisted', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({steamapp_id: id})
  });

  const data = await response.json();
  return data;
}

async function are_games_watchlisted(steamids) {
  let data = {}
  
  for(id in steamids) {
    if (steamids[id] == "") continue;
    data[steamids[id]] = await is_game_watchlisted(steamids[id]);
  }

  return data
}

/*
Helper functions
*/

function get_steamapp_ids() {
  buttons = $(".wishlist")
  steamids = []
  $.each(buttons, function() {
    steamids.push(parseInt($(this).attr("data-steamid")))
  });
  return steamids
}