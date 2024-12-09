/*
JQuery functions
*/
$(document).ready(async function() {
  steamids = get_steamapp_ids();
  wishlist_status = await are_games_wishlisted(steamids);

  for(id in wishlist_status) {
    if (!wishlist_status[id] || wishlist_status[id]["error"] == 500) continue
    $(`*[data-steamid="${id}"]`).addClass("active")
  }
})

/*
Removes the game from the watchlist if double confirmed
*/
let watchlist_halfconfirm = {}

$('.watchlist').on("click", async function() {
  let id = $(this).attr("data-steamid")

  if (watchlist_halfconfirm[id]) {
    // Remove game entry (ik its a bit janky but it'll work every time)
    $(this).parent().parent().parent().slideUp(500, function() {$(this).remove()})
    delete_from_watchlist(id);
    setTimeout(function() {update_items();}, 600)
  } else {
    watchlist_halfconfirm[id] = true;
    $(this).parent().children().first().addClass("active")
    setTimeout(function() {
      watchlist_halfconfirm[id] = false;
      $(`*[data-steamid="${id}"]`).parent().children().first().removeClass("active")
    }, 3000)
  }
})

function update_items() {
  items = get_steamapp_ids().length;

  if (items == 1) $('.num').text(`${items} item`);
  else $('.num').text(`${items} items`);
}

/*
Removes item from wishlist
*/

$('.wishlist').on("click", async function() {
  let id = $(this).attr("data-steamid")

  is_wishlisted = await is_game_wishlisted(id);

  if (!is_wishlisted) {
    $(this).addClass("active");
    add_to_wishlist(id);
  } else {
    $(this).removeClass("active");
    delete_from_wishlist(id);
  }
})

/*
Async Functions
*/

async function delete_from_wishlist(id) {
  // Delete current game from user's wishlist
  const response = await fetch('/api/delete_wishlist_item', {
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

async function add_to_wishlist(id) {
  // Add current game to user's wishlist
  const response = await fetch('/api/add_wishlist_item', {
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

function get_steamapp_ids() {
  buttons = $(".wishlist")
  steamids = []
  $.each(buttons, function() {
    steamids.push(parseInt($(this).attr("data-steamid")))
  });
  return steamids
}