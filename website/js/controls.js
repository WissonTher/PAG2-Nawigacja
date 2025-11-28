// Proper handling of map click event
map.on('click', onMapClick);

// A dedicated panel for mode toggling
var modeControl = L.control({position: 'topleft'});
modeControl.onAdd = function(map) {
    var div = L.DomUtil.create('div', 'mode-toggle');
    div.innerHTML = `
        <div class="mode-label">Trasa | Zasięg</div>
        <div id="activeModeText" style="font-size: 10px; margin-bottom: 5px;"></div>
        <label class="switch">
            <input type="checkbox" id="modeCheckbox">
            <span class="slider"></span>
        </label>
    `;
    
    var checkbox = div.querySelector("#modeCheckbox");
    L.DomEvent.on(checkbox, 'change', function(e) {
        L.DomEvent.stopPropagation(e);
        L.DomEvent.preventDefault(e);
        isModeRange = e.target.checked; 
        clearMarkers();
        clearResults();
        updateMode(); 
        rangeMarker = null;
        startMarker = null;
        endMarker = null;
    });
    L.DomEvent.disableClickPropagation(div); 
    setTimeout(updateMode, 0);
    return div;
};
modeControl.addTo(map);

// A simple button for running the computations 
var runControl = L.control({position: 'topleft'});
runControl.onAdd = function(map) {
    var div = L.DomUtil.create('div', 'leaflet-bar custom-run-control');
    div.innerHTML = '<button id="runButton" class="custom-leaflet-button">Wyznacz</button>';
    var runButton = div.querySelector("#runButton");
    L.DomEvent.on(runButton, 'click', function (e) {
        L.DomEvent.stopPropagation(e);
        L.DomEvent.preventDefault(e);  
        handleAnalysis();
    });
    L.DomEvent.disableClickPropagation(div);
    return div;
};
runControl.addTo(map);

/* [ROUTE MODE ONLY] */
// A panel for displaying coordinates after user click on map
var coordsControl = L.control({position: 'topleft'});
coordsControl.onAdd = function(map) {
    var div = L.DomUtil.create('div', 'mode-toggle coord-panel-container'); 
    div.id = 'coordPanel'; 
    div.innerHTML = `
        <div style="margin-bottom: 4px;">
            <label>Start:</label>
            <input type="text" id="startCoords" readonly style="width: 100px; border: 1px solid #ddd; padding: 2px;">
        </div>
        <div>
            <label>Koniec:</label>
            <input type="text" id="endCoords" readonly style="width: 100px; border: 1px solid #ddd; padding: 2px;">
        </div>
    `;
    L.DomEvent.disableClickPropagation(div);
    setTimeout(updateCoordinatePanel, 0); 
    return div;
};
coordsControl.addTo(map);

/* [ROUTE MODE ONLY] */
// A panel with checkboxes for choosing computation algorithm
var algControl = L.control({position: 'topleft'});
algControl.onAdd = function(map) {
    var div = L.DomUtil.create('div', 'mode-toggle algo-panel-container'); 
    div.id = 'algPanel'; 
    
    div.innerHTML = `
        <div class="mode-label">Algorytm</div>
        <div style="margin-top: 5px;">
            <label style="font-size: 11px; font-weight: normal; display: block;">
                <input type="radio" name="algorithm" value="a_star" checked> A*
            </label>
            <label style="font-size: 11px; font-weight: normal; display: block;">
                <input type="radio" name="algorithm" value="djikstratarget"> Dijkstra
            </label>
        </div>
    `;
    
    // Listing possible options [A* / Dijkstra]
    var radios = div.querySelectorAll("input[name='algorithm']");
    radios.forEach(radio => {
        L.DomEvent.on(radio, 'change', function(e) {
            L.DomEvent.stopPropagation(e);
            algorithm = e.target.value;
            clearResults();
        });
    });

    L.DomEvent.disableClickPropagation(div);
    return div;
};
algControl.addTo(map);

/* [RANGE MODE ONLY] */
// A slider for determining the maximum time of range analysis
var timeRangeControl = L.control({position: 'topleft'});
timeRangeControl.onAdd = function(map) {
    var div = L.DomUtil.create('div', 'leaflet-bar custom-range-control');
    div.id = 'rangePanel';
    div.innerHTML = `
        <div style="padding: 5px 8px; font-size: 12px; font-weight: bold;">
            Podaj maksymalny czas: <span id="rangeTimeValue">30 min</span>
        </div>
        <div style="padding: 0 8px 5px 8px">
            <input type="range" id="maxTimeSlider" min="5" max="60" step="5" value="30" style="width: 100%;">
        </div>
    `;
    var slider = div.querySelector("#maxTimeSlider");
    L.DomEvent.on(slider, 'input', function(e) {
        L.DomEvent.stopPropagation(e);
        updateRangeSliderLabel(e.target.value);
    });
    L.DomEvent.disableClickPropagation(div);
    setTimeout(() => updateRangeSliderLabel(slider.value), 0);
    return div;
};
timeRangeControl.addTo(map);