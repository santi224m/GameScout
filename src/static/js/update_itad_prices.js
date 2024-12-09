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

  for (let i = 0; i < stores.length; i++) {
    let store_el = stores[i];
    let store_name = store_el.querySelector('.name').textContent;
    let store_info = deals[store_name];

    // Update discount
    if (store_info.discount > 0) {
      percent_el = store_el.querySelector('.percent');
      val = `-${store_info.discount}%`
      percent_el.textContent = val;

      // Update regular price
      regular_price_el = store_el.querySelector('.retail-price');
      val = `$${store_info.regular_price}`;
      regular_price_el.textContent = val;
    }

    // Update price
    let price_el = store_el.querySelector('.price');
    price_el.textContent = `$${store_info.current_price}`;
  }
}

update_prices();