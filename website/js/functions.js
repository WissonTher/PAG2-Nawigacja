/* UI MANAGEMENT */

// Updates UI panel with coordinates from clicked location
function updateCoordinatePanel() {
    var startLat = '', startLng = '', endLat = '', endLng = '';

    if (startMarker) {
        var pos = startMarker.getLatLng();
        startLat = pos.lat.toFixed(5);
        startLng = pos.lng.toFixed(5);
    }
    if (endMarker) {
        var pos = endMarker.getLatLng();
        endLat = pos.lat.toFixed(5);
        endLng = pos.lng.toFixed(5);
    }

    // Overwriting the existing value
    const start = document.getElementById('startCoords');
    const end = document.getElementById('endCoords');
    if(start) start.value = startLat ? `${startLat}, ${startLng}` : '';
    if(end) end.value = endLat ? `${endLat}, ${endLng}` : '';
}

// Enables to display items depending on the mode
function updateMode() {
    var coordPanel = document.getElementById('coordPanel');
    var rangePanel = document.getElementById('rangePanel');
    var algPanel = document.getElementById('algPanel');

    if (coordPanel) coordPanel.style.display = isModeRange ? 'none' : 'block';
    if (algPanel) algPanel.style.display = isModeRange ? 'none' : 'block';
    if (rangePanel) rangePanel.style.display = isModeRange ? 'block' : 'none';
}

// Performs value update on slider connected with time value
function updateRangeSliderLabel(value) {
    const label = document.getElementById('rangeTimeValue');
    if (label) { label.textContent = `${value} min`; }
}

/* MARKERS MANAGEMENT */

// Clears range buffer or route
function clearResults() {
    if (result) {
        map.removeLayer(result);
        result = null;
    }
}

// Clears all visible markers
function clearMarkers() {
    if (rangeMarker) { map.removeLayer(rangeMarker); rangeMarker = null; }
    if (startMarker) { map.removeLayer(startMarker); startMarker = null; }
    if (endMarker) { map.removeLayer(endMarker); endMarker = null; }
    updateCoordinatePanel();
}

// Logic associated with dragging the popup
function onDragEnd(event) {
    clearResults();
    var marker = event.target;
    var position = marker.getLatLng();
    marker.setLatLng(new L.LatLng(position.lat, position.lng), {draggable:'true'});
    map.panTo(new L.LatLng(position.lat, position.lng));
    updateCoordinatePanel();
}

// Adding new marker to the map
function addMarker(latlng, icon) {
    clearResults();
    var marker = new L.marker(latlng, {icon: icon, draggable:'true'});
    marker.on('dragend', onDragEnd);
    map.addLayer(marker);
    return marker;
}

// Conditional map click handling different modes
function onMapClick(e) {
    if (isModeRange) {
        clearMarkers();
        rangeMarker = addMarker(e.latlng, rangeIcon);
        rangeMarker.bindPopup("Wyjściowy punkt dla <b>zasięgów</b>.<br>Kliknij ponownie, aby przenieść.").openPopup();
    } else {
        if (startMarker === null) {
            clearMarkers();
            startMarker = addMarker(e.latlng, startIcon);
            startMarker.bindPopup("Ustawiono <b>punkt startowy</b>.").openPopup();
        } else if (endMarker === null) {
            endMarker = addMarker(e.latlng, endIcon);
            startMarker.closePopup(); 
            endMarker.bindPopup("Ustawiono <b>punkt końcowy</b>.").openPopup();
        } else {
            clearMarkers();
            startMarker = addMarker(e.latlng, startIcon);
            startMarker.bindPopup("Ustawiono <b>punkt startowy</b>.").openPopup();
        }
    }
    updateCoordinatePanel();
}

// Fetches and styles data from URL into the map
function fetchData(url) {
    clearResults(); 
    const runButton = document.getElementById('runButton');
    if (runButton) runButton.textContent = "Ładowanie...";
    
    fetch(url)
        .then(response => {
            if (!response.ok) {
                let errorMessage = `Błąd serwera: ${response.status}`;
                if (response.status === 500) errorMessage = "Nie udało się obliczyć trasy/zasięgu.";
                throw new Error(errorMessage);
            }
            return response.json();
        })
        .then(data => {
            console.log("Odebrano dane GeoJSON:", data);
            
            if (data && data.type === "FeatureCollection") {
                // Sorting from closests to farthests
                data.features.sort((a, b) => b.properties.cost - a.properties.cost);

                result = L.geoJSON(data, {
                    coordsToLatLng: function(coords) {
                        // Transformation to Leaflet CRS
                        var wgs84Coords = proj4('EPSG:2180', 'EPSG:4326', coords);
                        return L.latLng(wgs84Coords[1], wgs84Coords[0]);
                    },
                    style: function(feature) {
                        const isPolygon = feature.geometry.type === "Polygon" || feature.geometry.type === "MultiPolygon";
                        
                        if (isPolygon) {
                            // Color determination
                            const cost = feature.properties.cost;
                            const ratio = cost / MAX_COST_SECONDS;
                            let colorIndex = Math.floor(ratio * MAX_CLR_IDX);
                            if (colorIndex > MAX_CLR_IDX) colorIndex = MAX_CLR_IDX;
                            
                            return { 
                                color: '#444444', 
                                weight: 1, 
                                opacity: 1, 
                                fillColor: COLORS[colorIndex],
                                fillOpacity: 0.8 
                            }; 
                        } else {
                            return { color: 'red', weight: 4, opacity: 0.9, fillOpacity: 0 };
                        }
                    },
                    onEachFeature: function(feature, layer) {
                        if (feature.properties && feature.properties.cost) {
                            const totalSeconds = feature.properties.cost;
                            const totalDistance = feature.properties.distance || 0;
                            const totalDistanceKm = (totalDistance / 1000).toFixed(2);
                            let popupContent = "";

                            if (isModeRange) {
                                const maxMin = Math.round(totalSeconds / 60);
                                popupContent = `
                                    <h4>Zasięg dojazdu</h4>
                                    <p>Maksymalny czas dotarcia: <b>~${maxMin} min</b></p>
                                `;
                            } else {
                                const h = Math.floor(totalSeconds / 3600);
                                const m = Math.floor(totalSeconds / 60) % 60;
                                const s = Math.round(totalSeconds % 60);
                                const timeDisplay = `${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`;
                                
                                popupContent = `
                                    <h4>Wyznaczona trasa</h4>
                                    <p>Czas: <b>${timeDisplay}</b><br>
                                    Długość: <b>${totalDistanceKm} km</b></p>
                                `;
                            }
                            layer.bindPopup(popupContent);
                        }
                    }
                }).addTo(map);
                
                map.fitBounds(result.getBounds());
            } else {
                alert("Odebrano niepoprawne dane GeoJSON.");
            }
        })
        .catch(error => {
            console.error("Błąd:", error);
            L.popup({ closeButton: true, autoClose: true, className: 'error-popup' })
                .setLatLng(map.getCenter())
                .setContent(`
                    <h4 style="color: darkred; margin:0;">Błąd Analizy</h4>
                    <p>${error.message}</p>
                `)
                .openOn(map);
        })
        .finally(() => {
            if (runButton) runButton.textContent = "Wyznacz";
        });
}

// Asks server for data
function handleAnalysis() {
    const baseUrl = 'https://gar57-pag2nawi.hf.space/';
    let url = '';
    
    if (isModeRange) {
        if (!rangeMarker) {
            alert("Błąd: Ustaw punkt początkowy dla trybu Zasięg.");
            return;
        }
        const pos = rangeMarker.getLatLng();
        const maxCost = parseInt(document.getElementById('maxTimeSlider').value, 10);
        const maxCostSeconds = maxCost * 60;
        const buffer = 150;
        
        url = `${baseUrl}djikstrarange/${pos.lng}/${pos.lat}/${maxCostSeconds}/${buffer}/10/True`;
        console.log("Uruchamiam zasięg:", url);
    } else {
        if (!startMarker || !endMarker) {
            alert("Błąd: Ustaw punkty startowy i końcowy dla trybu Trasa.");
            return;
        }
        const startPos = startMarker.getLatLng();
        const endPos = endMarker.getLatLng();
        
        url = `${baseUrl}${algorithm}/${startPos.lng}/${startPos.lat}/${endPos.lng}/${endPos.lat}`;
        console.log(`Uruchamiam trasę (${algorithm}):`, url);
    }
    
    if (url) fetchData(url);
}