/*
This Script handles all moving asepcts of the game page
*/

// Carousel and Popup
let carousel_index = 1;
let total_items = $('.full').length;
let popup_index = 1;
let total_images = $('img.full').length;
let active_tab = "windows";

function carouselLeft() {
  if (carousel_index > 1) {
    $(`.full.${carousel_index}`).fadeOut(500);
    $(`.full.${carousel_index - 1}`).fadeIn(500);
    $(`.full.${carousel_index}`).removeClass("hidden");
    $(`.indicator.${carousel_index}`).removeClass("active");
    $(`.indicator.${carousel_index - 1}`).addClass("active");
    carousel_index--;
  } else {
    $(`.full.${carousel_index}`).fadeOut(500);
    $(`.full.${total_items}`).fadeIn(500);
    $(`.full.${carousel_index}`).removeClass("hidden");
    $(`.indicator.${carousel_index}`).removeClass("active");
    $(`.indicator.${total_items}`).addClass("active");
    carousel_index = total_items;
  }

  carouselScrollTo();
}

function carouselRight() {
  if (carousel_index < total_items) {
    $(`.full.${carousel_index}`).fadeOut(500);
    $(`.full.${carousel_index + 1}`).fadeIn(500);
    $(`.full.${carousel_index}`).removeClass("hidden");
    $(`.indicator.${carousel_index}`).removeClass("active");
    $(`.indicator.${carousel_index + 1}`).addClass("active");
    carousel_index++;
  } else {
    $(`.full.${carousel_index}`).fadeOut(500);
    $(`.full.${1}`).fadeIn(500);
    $(`.full.${carousel_index}`).removeClass("hidden");
    $(`.indicator.${carousel_index}`).removeClass("active");
    $(`.indicator.${1}`).addClass("active");
    carousel_index = 1;
  }

  carouselScrollTo();
}

function carouselGoTo(index, immediate=false) {
  if (carousel_index == index) return;
  if (immediate) {
    $(`.full.${carousel_index}`).fadeOut(0);
    $(`.full.${index}`).fadeIn(0);
    $(`.full.${carousel_index}`).removeClass("hidden");
    $(`.indicator.${carousel_index}`).removeClass("active");
    $(`.indicator.${index}`).addClass("active");
  } else {
    $(`.full.${carousel_index}`).fadeOut(500);
    $(`.full.${index}`).fadeIn(500);
    $(`.full.${carousel_index}`).removeClass("hidden");
    $(`.indicator.${carousel_index}`).removeClass("active");
    $(`.indicator.${index}`).addClass("active");
  }
  carousel_index = index;

  carouselScrollTo();
}

function carouselScrollTo() {
  var container = $('.images'),
  scrollTo = $(`.thumbnail.${carousel_index}`);

  container.animate({
      scrollLeft: scrollTo.offset().left - container.offset().left + container.scrollLeft()
  });
}

function openPopup(index) {
  popup_index = index;
  $('.popup-container').fadeIn(250);
  $(`.popup-full.${popup_index}`).removeClass("hidden");
  $(`.popup-text`).text( `${popup_index} of ${total_images} Screenshots`);
}

function closePopup() {
  carouselGoTo(popup_index, true);
  $('.popup-container').fadeOut(250);
}

function popupNext() {
  if (popup_index < total_images) {
    $(`.popup-full.${popup_index}`).fadeOut(500);
    $(`.popup-full.${popup_index + 1}`).fadeIn(500);
    $(`.popup-full.${popup_index}`).removeClass("hidden");
    popup_index++;
  } else {
    $(`.popup-full.${popup_index}`).fadeOut(500);
    $(`.popup-full.${1}`).fadeIn(500);
    $(`.popup-full.${popup_index}`).removeClass("hidden");
    popup_index = 1;
  }
  $(`.popup-text`).text( `${popup_index} of ${total_images} Screenshots`);
}

function popupPrev() {
  if (popup_index > 1) {
    $(`.popup-full.${popup_index}`).fadeOut(500);
    $(`.popup-full.${popup_index - 1}`).fadeIn(500);
    $(`.popup-full.${popup_index}`).removeClass("hidden");
    popup_index--;
  } else {
    $(`.popup-full.${popup_index}`).fadeOut(500);
    $(`.popup-full.${total_images}`).fadeIn(500);
    $(`.popup-full.${popup_index}`).removeClass("hidden");
    popup_index = total_images;
  }
  $(`.popup-text`).text( `${popup_index} of ${total_images} Screenshots`);
}

// System Requirements
function changeTab(tab) {
  if (active_tab == tab) return;
  $(`div.${active_tab}`).fadeOut(250, function() {
    $(`div.${tab}`).fadeIn(250);
  });
  $(`.${active_tab}`).removeClass("active");
  $(`button.${tab}`).addClass("active");
  active_tab = tab;
}