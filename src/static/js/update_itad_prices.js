// Get all stores on page
steamapp_id = $(".game-title").attr("data-steamid");
steamapp_id = parseInt(steamapp_id);

const stores = document.querySelectorAll('.store-entry');


let update_prices = async () => {
  const response = await fetch('/api/get_prices', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({steam_app_id: steamapp_id})
  });
  
  const data = await response.json();
  const deals = data.deals;
  console.log(deals)

  for (let i = 0; i < stores.length; i++) {
    let store_name = stores[i].querySelector('.name').textContent;
  }
}

update_prices();