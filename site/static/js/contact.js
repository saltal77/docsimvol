	
   var map;
    map = new GMaps({
        el: '#map',
        lat: 67.511533,
        lng: 45.287813,
        scrollwheel: false
    });

    map.addMarker({
        lat: 43.511533,
        lng: 45.287813,
        title: 'Marker with InfoWindow',
        infoWindow: {
            content: '<p>SPY Hosting Victoria Hall, Merrick Way, <br>FL 12345 Australia<a href="https://themeforest.net/user/99_design"  target="_blank">Themeforest</a></p>'
        }
    });    