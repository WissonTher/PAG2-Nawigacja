// Reading edge of the AoI border
fetch('website/data/voivodeship.geojson?' + Date.now())
    .then(response => response.json())
    .then(data => {
        L.geoJSON(data, {
            style: function(feature) {
                return { 
                    color: "blue", 
                    weight: 3, 
                    fillOpacity: 0, 
                    interactive: false
                };
            }          
        }).addTo(map);
    })
    .catch(error => console.error("Błąd podczas wczytywania GeoJSON:", error));