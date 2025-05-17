document.addEventListener("DOMContentLoaded", () => {
  const map = L.map("map").setView([45.4642, 9.19], 12);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "Map data © OpenStreetMap contributors",
  }).addTo(map);

  fetch("/api/alloggi_geo")
    .then((response) => response.json())
    .then((data) => {
      L.geoJSON(data, {
        onEachFeature: function (feature, layer) {
          const p = feature.properties;
          if (p) {
            const popupHTML = `
              <div style="min-width: 200px;">
                <h4>${p.titolo}</h4>
                <p><b>Zona:</b> ${p.zona}</p>
                <p><b>Tipo:</b> ${p.tipologia_alloggio} - ${p.tipo_stanza}</p>
                <p><b>Prezzo:</b> ${p.prezzo_base}€</p>
                <p><b>Rating:</b> ⭐ ${p.rating} (${p.recensioni_totali} recensioni)</p>
                <a href="/host/${p.host_id}" class="btn">🔍 Vai all'host</a>
              </div>
            `;
            layer.bindPopup(popupHTML);
          }
        }
      }).addTo(map);
    })
    .catch((error) => {
      console.error('Errore nel caricamento dei dati GeoJSON:', error);
    });
});
