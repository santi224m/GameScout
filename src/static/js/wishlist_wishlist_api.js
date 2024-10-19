$(document).ready(function() {
  $(".games").sortable({
    axis: "y",
    handle: ".fa-grip-lines",
    tolerance: "pointer",
    deactivate: function(event, ui) {
      inputs = $(".position")
      $.each(inputs, function(i) {
        $(this).attr("value", i+1)
      })
    }
  })
})






/*
Add the current game to the user's wishlist
*/
let wishlist_halfconfirm = {}

$('.wishlist').on("click", async function() {
  let id = $(this).attr("data-steamid")

  if (wishlist_halfconfirm[id]) {
    // Remove game entry (ik its a bit janky but it'll work every time)
    $(this).parent().parent().parent().slideUp(500, function() {$(this).remove()})
    delete_from_wishlist(id);
  } else {
    wishlist_halfconfirm[id] = true;
    $(this).parent().children().first().addClass("active")
    setTimeout(function() {
      wishlist_halfconfirm[id] = false;
      $(`*[data-steamid="${id}"]`).parent().children().first().removeClass("active")
    }, 3000)
  }
})

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