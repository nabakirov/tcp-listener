'use strict';

const map = L.map('map',{
	center:[42.875752, 74.595464],
	zoom:13
});

window.map = map;

const osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
const osmAttrib = 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
const osm = new L.TileLayer(osmUrl, {attribution: osmAttrib});
map.addLayer(osm);


