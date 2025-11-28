// Initialization of the map
var map = L.map('map', {
    maxZoom: 20
}).setView([53.77639, 20.48778], 12);

// Base underlay definition
var osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png?{foo}', {foo: 'bar'});
osm.addTo(map);

// Projection mechanism
proj4.defs("EPSG:2180", "+proj=tmerc +lat_0=0 +lon_0=19 +k=0.9993 +x_0=500000 +y_0=-5300000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs");

var isModeRange = false;
var rangeMarker = null;
var startMarker = null;
var endMarker = null;
var algorithm = 'a_star';
var result = null; 

const MAX_COST_SECONDS = 60 * 60;
const COLORS = [
    '#67001f', // 0-5 minut
    '#b2182b', 
    '#d6604d', 
    '#f4a582', 
    '#fddbc7', 
    '#f7f7f7', 
    '#d1e5f0', 
    '#92c5de', 
    '#4393c3', 
    '#2166ac', 
    '#053061', 
    '#021029'  // 55-60 minut
];
const MAX_CLR_IDX = COLORS.length - 1;

function createIcon(url) {
    return L.icon({
        iconUrl: url,
        iconSize: [15, 15],
        iconAnchor: [7.5, 7.5],
        popupAnchor: [0, -7.5]
    });
}

var endIcon = createIcon('website/icons/endpoint.png'); 
var startIcon = createIcon('website/icons/startpoint.png'); 
var rangeIcon = createIcon('website/icons/rangepoint.png');