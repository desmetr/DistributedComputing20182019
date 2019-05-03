function checkRadius(centerLat, centerLng, newLat, newLng, zoomLevel)
{
	var km = 5;

	var kX = Math.cos(Math.PI * centerLat / 180.0) * kY;
	var kY = 40000 / 360;

	var dX = Math.abs(centerLng - newLng) * kX;
	var dY = Math.abs(centerLat - newLat) * kY;

	return Math.sqrt(dX * dX + dY * dY) <= km;
}

function initMap()
{
	var map, yourMarker;
	var zoomLevel = 15;
	var defaultLocation = {lat: 51.219, lng: 4.402}; // Default location is Antwerp
	var currentPos = defaultLocation;

	map = new google.maps.Map(document.getElementById('geolocation'), {
		center: defaultLocation,
		zoom: zoomLevel,
		gestureHandling: 'cooperative'});

	yourMarker = new google.maps.Marker({
 		position: defaultLocation,
 		map: map,
 		label: 'Your position'});

	// Try HTML5 geolocation
	if (navigator.geolocation)
	{
	    navigator.geolocation.getCurrentPosition(function(position)
	    {
	        currentPos = 
	        {
	            lat: position.coords.latitude,
	            lng: position.coords.longitude
	        };

	        map.setCenter(currentPos);
	        yourMarker.setPosition(currentPos);
	    },

    function()
    {
        handleLocationError(true, infoWindow, map.getCenter());
    });

	function callbackToServer(id) 
	{
		$.ajax({
			type: "GET",
			contentType: "application/json;charset=utf-8",
			// url: "http://localhost:5005/garden",
			url: "http://localhost:5001/callback/" + encodeURIComponent(id),
			traditional: "true",
			data: JSON.stringify(id),
			dataType: "json"
		})
	}
			var contentString = 
		'<div id="content">' +
		'User: <b>a</b>' +
		'<br>Vegetables:' +
		'<ul>' +
		'<li><b>potato</b></li>'+'<li><b>tomato</b></li>'+
		'</ul>'+
		'Fruits:'+
		'<ul>'+
	'<li><b>apple</b></li>'+'<li><b>strawberry</b></li>'+
		'</ul>'+
		'Herbs:'+
		'<ul>'+
	'<li><b>basilicum</b></li>'+'</ul>'+'	<a href="http://localhost:5005/garden">Go To Garden</a> '+'<a href="http://localhost:5006/chat">Chat With User</a>'+'</div>';
			var infoWindow1 = new google.maps.InfoWindow({
				position: {lat: 51.216948, lng: 4.696734999999999},
				content: contentString,
				map: map
			})

			
			var contentString = 
		'<div id="content">' +
		'User: <b>b</b>' +
		'<br>Vegetables:' +
		'<ul>' +
		'<li><b>potato</b></li>'+'<li><b>tomato</b></li>'+
		'</ul>'+
		'Fruits:'+
		'<ul>'+
	'<li><b>apple</b></li>'+'<li><b>strawberry</b></li>'+
		'</ul>'+
		'Herbs:'+
		'<ul>'+
	'<li><b>basilicum</b></li>'+'</ul>'+'	<a href="http://localhost:5005/garden">Go To Garden</a> '+'<a href="http://localhost:5006/chat">Chat With User</a>'+'</div>';
			var infoWindow2 = new google.maps.InfoWindow({
				position: {lat: 51.1845547, lng: 4.4212374},
				content: contentString,
				map: map
			})

			
			var contentString = 
		'<div id="content">' +
		'User: <b>g</b>' +
		'<br>Vegetables:' +
		'<ul>' +
		'<li><b>potato</b></li>'+'<li><b>tomato</b></li>'+
		'</ul>'+
		'Fruits:'+
		'<ul>'+
	'<li><b>apple</b></li>'+'<li><b>strawberry</b></li>'+
		'</ul>'+
		'Herbs:'+
		'<ul>'+
	'<li><b>basilicum</b></li>'+'</ul>'+'	<a href="http://localhost:5005/garden">Go To Garden</a> '+'<a href="http://localhost:5006/chat">Chat With User</a>'+'</div>';
			var infoWindow3 = new google.maps.InfoWindow({
				position: {lat: 51.1845547, lng: 4.4212374},
				content: contentString,
				map: map
			})

				}
	else
	{
		// Browser doesn't support Geolocation
		handleLocationError(false, infoWindow, map.getCenter());
	}
}

function handleLocationError(browserHasGeoLocation, infoWindow, pos)
{
	infoWindow.setPosition(pos);
	infoWindow.setContent(browserHasGeoLocation ? 'Error: The Geolocation service failed.' : 'Error: Your browser does not support geolocation.');
	infoWindow.open(map);
}