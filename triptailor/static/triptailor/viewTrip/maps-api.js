
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


//these are global to make routes from other javaScriptz via makeRoute function
var ds;
var dd;
var map;
var place_Service;
var infoWindow;
var marker;
var infowindowContent;
var place;

function initMap() {
  ds = new google.maps.DirectionsService();
  dd = new google.maps.DirectionsRenderer();
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 40.7128, lng: -74.0060},
    zoom: 13,
    styles:map_styling,
    //gestureHandling:"greedy",
  });
  place_Service = new google.maps.places.PlacesService(map);

  infoWindow = new google.maps.InfoWindow();
  marker = new google.maps.Marker({
    map: map,
    anchorPoint: new google.maps.Point(0, -29)
  });

  dd.setMap(map);
  
	makeRoute(ds,dd,trip);
}


function makeRoute(directionsService,directionsDisplay,routeList){
	var waypoints = [];
  var start = {};
  var end = {};
  
  console.log('Making route for:' +JSON.stringify(trip));

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

/**
 * This will display location informaton in the map for a user. 
 * @param {String} placeId //id of location
 */
function showDetails(placeId){
  infoWindow.close();
  marker.setVisible(false);
  request = {
    "placeId":placeId
  }
  place_Service.getDetails(request,placeCallback); //async
    
}

function placeCallback(data,status){
    if (status == google.maps.places.PlacesServiceStatus.OK) {
      place = data;
    } else {
      console.log('error with place request :'+status);
      place = {};
    }
    console.log(data);

    marker.setPosition(data.geometry.location);
    marker.setVisible(true);
    //check data for our info window
    if(data.rating)
      starRating(data.rating,document.getElementById("locationRating"));

    photoUrl = typeof data.photos !== 'undefined' ? data.photos[0].getUrl({'maxWidth': 300, 'maxHeight':200}) : '';
    document.getElementById("locationPicture").src = photoUrl;

    document.getElementById("locationTitle").innerText = data.name ? data.name : '';


    infoWindow.setContent(document.getElementById("locationContent").innerHTML);
    infoWindow.open(map,marker);
    map.setCenter(marker.getPosition());
}

/**
 * 
 * @param {Number} rating //can be a decimal number to do 3.5 or 3.6 ratings. will round to nearest 1/2
 * @param {Element} location //send in the div object you would like to add a rating to
 */
function starRating(rating,location){
  location.innerHTML = '';
  if(rating < 0 || rating > 5){
    console.log('malformed star rating - default @ 3.5');
    rating = 3.5;
  }
  if(location==null){
    console.log('starRating - location to insert stars is null');
    return;
  }
  for(i = 0; i<Math.trunc(rating); i++)
    location.innerHTML += '<i class="material-icons">star</i>';
  if(rating - Math.trunc(rating) >= 0.5)
    location.innerHTML += '<i class="material-icons">star_half</i>';
  var emptyNum = 5 - Math.ceil(rating);
  for(i = 0; i<emptyNum;i++)
    location.innerHTML += '<i class="material-icons">star_border</i>';
}