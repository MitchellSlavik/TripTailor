
var map_styling = [
  {
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#e6ebf1"
      }
    ]
  },
  {
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#284840"
      }
    ]
  },
  {
    "elementType": "labels.text.stroke",
    "stylers": [
      {
        "color": "#f3f5f8"
      }
    ]
  },
  {
    "featureType": "administrative.locality",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#004d40"
      }
    ]
  },
  {
    "featureType": "poi",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#59691b"
      }
    ]
  },
  {
    "featureType": "poi.medical",
    "elementType": "geometry.fill",
    "stylers": [
      {
        "color": "#f1e0e3"
      }
    ]
  },
  {
    "featureType": "poi.park",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#b7d4ca"
      }
    ]
  },
  {
    "featureType": "poi.park",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#6b9a76"
      }
    ]
  },
  {
    "featureType": "poi.school",
    "elementType": "geometry.fill",
    "stylers": [
      {
        "color": "#f5ede9"
      }
    ]
  },
  {
    "featureType": "poi.school",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#af6f50"
      }
    ]
  },
  {
    "featureType": "poi.sports_complex",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#b7d4ca"
      }
    ]
  },
  {
    "featureType": "road",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#fdfef9"
      }
    ]
  },
  {
    "featureType": "road",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#9ca5b3"
      }
    ]
  },
  {
    "featureType": "road.highway",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#4db6ac"
      }
    ]
  },
  {
    "featureType": "road.highway",
    "elementType": "geometry.stroke",
    "stylers": [
      {
        "color": "#298f67"
      }
    ]
  },
  {
    "featureType": "road.highway",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#44796c"
      }
    ]
  },
  {
    "featureType": "transit",
    "elementType": "geometry.fill",
    "stylers": [
      {
        "color": "#ccd3dd"
      }
    ]
  },
  {
    "featureType": "water",
    "elementType": "geometry",
    "stylers": [
      {
        "color": "#9fb7da"
      }
    ]
  },
  {
    "featureType": "water",
    "elementType": "labels.text.fill",
    "stylers": [
      {
        "color": "#515c6d"
      }
    ]
  },
  {
    "featureType": "water",
    "elementType": "labels.text.stroke",
    "stylers": [
      {
        "color": "#17263c"
      }
    ]
  }
];

var lastSelected = {};
var trip = [];


function makeRoute(directionsService,directionsDisplay,routeList){
	var waypoints = [];
  var start = {};
  var end = {};
  
	switch(routeList.length){
  	case 0:
    	alert('uh oh no where to go');
      return;

    case 1: //start and finish are the same place
    	start = {"placeId":routeList[0].placeId};
      end = {"placeId":routeList[0].placeId};
    break;
    default: //add anything more than 2 into our waypoints
    	for(var i = 1; i < routeList.length-1; i++){
        waypoints.push({
          location: {"placeId":routeList[i].placeId},
          stopover: true
        });
      }	
    case 2:
    	start = {"placeId":routeList[0].placeId};
      end = {"placeId":routeList[routeList.length-1].placeId};
    break;
  }

  
  //request route from google maps and then display results on screen 
  directionsService.route({
    origin: start,
    destination: end,
    waypoints: waypoints,
    optimizeWaypoints: false,
    travelMode: 'DRIVING'
  }, function(response, status) {
    if (status === 'OK') {
      console.log('got here')
      directionsDisplay.setDirections(response);	//activate directions on map
      //Display table route on screen for user
      var route = response.routes[0];
      //displayRouteTable(route,routeList);
    } else {
      window.alert('Directions request failed due to ' + status);
      console.log(response);
      console.log(status);
    }
  });
}

function initMap() {
  var directionsService = new google.maps.DirectionsService();
  var directionsDisplay = new google.maps.DirectionsRenderer();
  var map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: -33.8688, lng: 151.2195},
    zoom: 13,
    styles:map_styling,
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

  directionsDisplay.setMap(map);
  var mapRenderOptions = {};
  var polyLine = {};
  polyLine.strokeColor="#ffc21c";
  mapRenderOptions.polylineOptions=polyLine;
  directionsDisplay.setOptions(directionsDisplay);

	var locationList = document.getElementById('location-list');
  $('#addLocation').click(function(){
    if (lastSelected.hasOwnProperty('placeId')){
      $("#location-list").append('<li class="collection-item"><div>'+lastSelected.address+'</div></li>');
      trip.push(lastSelected);
      makeRoute(directionsService,directionsDisplay,trip);
      //document.getElementById('pac-input').innerText = '';
      $('#pac-input').val('');
      lastSelected = {};
    }
  });
	
  
  autocomplete.addListener('place_changed', function() {
    infowindow.close();
    marker.setVisible(false);
    var place = autocomplete.getPlace();
    console.log(place);
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
    place_id = place.place_id;
    console.log(format_address);
    console.log(place_id);
    
    lastSelected = {"placeId":place_id,"address":format_address};
		
    console.log(trip);
    infowindowContent.children['place-name'].textContent = place.name;
    infowindowContent.children['place-address'].textContent = address;
    infowindow.open(map, marker);
  });
}
