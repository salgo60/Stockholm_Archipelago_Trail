import * as L from 'leaflet';

export function initMap() {
  const map = L.map('map').setView([59.3293, 18.0686], 10);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors'
  }).addTo(map);

  L.marker([59.3293, 18.0686])
    .addTo(map)
    .bindPopup('Hello from Stockholm Archipelago Trail!')
    .openPopup();
}
