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

$(document).ready(async function() {
  steamids = get_steamapp_ids();
  wishlist_status = await are_games_wishlisted(steamids);

  for(id in wishlist_status) {
    if (!wishlist_status[id] || wishlist_status[id]["error"] == 500) continue
    $(`*[data-steamid="${id}"]`).addClass("active")
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