/*
JQuery functions
*/
$(document).ready(async function() {
  steamids = get_steamapp_ids();
  watchlist_status = await are_games_watchlisted(steamids);

  for(id in watchlist_status) {
    if (!watchlist_status[id] || watchlist_status[id]["error"] == 500) continue
    $(`*[data-steamid="${id}"]`).addClass("active")
  }

  renumber()
  $(".games").sortable({
    axis: "y",
    handle: ".fa-grip-lines",
    tolerance: "pointer",
    deactivate: function(event, ui) {renumber(); update_db()}
  })
})

$(".position").on('keypress',function(e) {
  if(e.which == 13) {
    changePos(e);
  }
});

$(".position").on('blur', function(e) {
  changePos(e);
})

/*
Change game position on text input
*/
function changePos(e) {
  val = parseInt(e.target.value)
  parent = $(e.currentTarget.parentElement.parentElement.parentElement)
  pos = parseInt(parent.attr("data-pos"))

  if (val == 0) val = 1
  else if (val < 0) {
    renumber()
    return
  } else if (val > $(".game").length) val = $(".game").length

  if (val < pos) parent.insertBefore($(`[data-pos=${val}]`))
  else parent.insertAfter($(`[data-pos=${val}]`))
  renumber()
  update_db()
}

/*
Renumber items
*/
async function renumber() {
  let inputs = $(".position")
  $.each(inputs, function(i) {
    $(this).attr("value", i+1)
    $(this).val(i+1)
    $(this).parent().parent().parent().attr("data-pos", i+1)
  })
}

/*
Update positions in the db
*/
async function update_db() {
  let inputs = $(".position")
  // Update game ranks in database
  game_pos_dict = {}
  for (let i = 0; i < inputs.length; i++) {
    let pos = inputs[i].value;
    let steamid = inputs[i].parentElement.parentElement.parentElement.querySelector('button[data-steamid]').dataset.steamid;
    game_pos_dict[steamid] = parseInt(pos);
  }
  const response = await fetch('/api/update_wishlist_rank', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(game_pos_dict)
  });
}

/*
Removes the game from the wishlist if double confirmed
*/
let wishlist_halfconfirm = {}

$('.wishlist').on("click", async function() {
  let id = $(this).attr("data-steamid")

  if (wishlist_halfconfirm[id]) {
    // Remove game entry (ik its a bit janky but it'll work every time)
    $(this).parent().parent().parent().slideUp(500, function() {$(this).remove()})
    delete_from_wishlist(id);
    setTimeout(function() {
      renumber(); 
      update_items();
    }, 600)
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
Removes item from watchlist
*/

$('.watchlist').on("click", async function() {
  let id = $(this).attr("data-steamid")

  is_watchlisted = await is_game_watchlisted(id);

  if (!is_watchlisted) {
    $(this).addClass("active");
    add_to_watchlist(id);
  } else {
    $(this).removeClass("active");
    delete_from_watchlist(id);
  }
})

function update_items() {
  items = get_steamapp_ids().length;

  if (items == 1) $('.num').text(`${items} item`);
  else $('.num').text(`${items} items`);
}


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

async function add_to_watchlist(id) {
  // Add current game to user's wishlist
  const response = await fetch('/api/add_watchlist_item', {
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

function get_steamapp_ids() {
  buttons = $(".watchlist")
  steamids = []
  $.each(buttons, function() {
    steamids.push(parseInt($(this).attr("data-steamid")))
  });
  return steamids
}