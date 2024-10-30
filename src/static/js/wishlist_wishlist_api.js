$(document).ready(function() {
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

async function renumber() {
  let inputs = $(".position")
  $.each(inputs, function(i) {
    $(this).attr("value", i+1)
    $(this).val(i+1)
    $(this).parent().parent().parent().attr("data-pos", i+1)
  })
}

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
Add the current game to the user's wishlist
*/
let wishlist_halfconfirm = {}

$('.wishlist').on("click", async function() {
  let id = $(this).attr("data-steamid")

  if (wishlist_halfconfirm[id]) {
    // Remove game entry (ik its a bit janky but it'll work every time)
    $(this).parent().parent().parent().slideUp(500, function() {$(this).remove()})
    delete_from_wishlist(id);
    setTimeout(function() {renumber()}, 600)
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

async function delete_from_wishlist(id) {
  // Delete current game from user's wishlist
  const response = await fetch('/api/delete_wishlist_item', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({steamapp_id: id})
  });

  const data = await response.json();
}