$("#pfp").on("change", function(e) {
  $(".file").html($(this)[0].files[0].name)
})

$("#country").countrySelect({
  defaultCountry: "us",
  preferredCountries: ['ca', 'gb', 'us'],
  responsiveDropdown: true
});