// This example requires the Places library. Include the libraries=places
// parameter when you first load the API. For example:
// <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places">

var trip = [];

function initMap() {
  var map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: -33.8688, lng: 151.2195},
    zoom: 13
  });
  var format_address = '';
  var place_id= '';
  var card = document.getElementById('pac-card');
  var input = document.getElementById('pac-input');
	var add = document.getElementById('addLocation');
  map.controls[google.maps.ControlPosition.TOP_RIGHT].push(card);

  var autocomplete = new google.maps.places.Autocomplete(input);

  // Bind the map's bounds (viewport) property to the autocomplete object,
  // so that the autocomplete requests use the current map bounds for the
  // bounds option in the request.
  autocomplete.bindTo('bounds', map);

  var infowindow = new google.maps.InfoWindow();
  var infowindowContent = document.getElementById('infowindow-content');
  infowindow.setContent(infowindowContent);
  var marker = new google.maps.Marker({
    map: map,
    anchorPoint: new google.maps.Point(0, -29)
  });
	var locationList = document.getElementById('location-list');
  $('#addLocation').click(function(){
  	$("#location-list").append('<li draggable="true" class="collection-item"><div>'+format_address+'</div></li>');
    
  });
	
  
  autocomplete.addListener('place_changed', function() {
    infowindow.close();
    marker.setVisible(false);
    var place = autocomplete.getPlace();
    if (!place.geometry) {
     	window.alert("No details available for input: '" + place.name + "'");
      return;
    }

    // If the place has a geometry, then present it on a map.
    if (place.geometry.viewport) {
      map.fitBounds(place.geometry.viewport);
    } else {
      map.setCenter(place.geometry.location);
      map.setZoom(17);  // Why 17? Because it looks good. -thank you google you got a laugh out of me - CK
    }
    marker.setPosition(place.geometry.location);
    marker.setVisible(true);

    var address = '';
    var place_id = '';
    
    format_address = place.name;
    place_id = place.id;
    console.log(format_address);
    console.log(place.id);
    
    trip.push({"place":place_id,"address":format_address});
		
    console.log(trip);
    infowindowContent.children['place-name'].textContent = place.name;
    infowindowContent.children['place-address'].textContent = address;
    infowindow.open(map, marker);
  });


  // setupClickListener('changetype-all', []);
  // setupClickListener('changetype-address', ['address']);
  // setupClickListener('changetype-establishment', ['establishment']);
  // setupClickListener('changetype-geocode', ['geocode']);


}