# Checking a parcel against the Palermo Landscape Plan in QGIS

How to see, for any plot in the province of Palermo, which protection level the adopted
Landscape Plan (D.A. n. 24/GAB of 10/06/2026) assigns to it, and why.

Everything here uses free, official data: the cadastral map of the Agenzia delle Entrate
and the plan layers of the Regione Siciliana (S.I.T.R.). No account, no licence.

---

## 0. What you need

- QGIS (free, qgis.org), version 3.28 or newer
- An internet connection — all layers are loaded live from the servers
- The sheet (foglio) and parcel numbers of the plot, or its approximate position

---

## 1. Add the background map

1. Left panel **Browser** → **XYZ Tiles** → double-click **OpenStreetMap**.
2. The world map appears. Zoom to Sicily, then to the municipality.

If the Browser panel is not visible: menu **View → Panels → Browser**.

---

## 2. Add the cadastral map (Agenzia delle Entrate)

1. In **Browser**, right-click **WMS/WMTS** → **New Connection**.
2. Name: `Catasto`
   URL: `https://wms.cartografia.agenziaentrate.gov.it/inspire/wms/ows01.php`
   → **OK**.
3. Expand the connection and double-click these layers, in this order:
   - **CP.CadastralZoning** (sheet boundaries, visible from 1:200,000)
   - **CP.CadastralParcel** (parcels, visible from 1:5,000)
   - **fabbricati** (buildings, from 1:5,000)
   - **codice_plla** (parcel numbers, from 1:2,000)

The parcels stay invisible until you zoom in past 1:5,000. That is normal.

---

## 3. Add the Landscape Plan layers (S.I.T.R.)

1. In **Browser**, right-click **ArcGIS REST Servers** → **New Connection**.
2. Name: `Piano Paesaggistico Palermo`
   URL: `https://map.sitr.regione.sicilia.it/gis/rest/services/piani_paesaggistici/pa_regimi_normativi/MapServer`
   → **OK**.
3. Expand it. Double-click **regimi normativi** — take the entry with the *polygon*
   symbol, not the raster one, so that you can query the attributes.
4. Two more useful services, added the same way (same URL, last part changed):
   - `…/piani_paesaggistici/pa_componenti_paesaggio/MapServer` — landscape components,
     including the ridge lines (crinali) the plan has drawn
   - `…/piani_paesaggistici/pa_beni_paesaggistici/MapServer` — listed landscape assets

The service works in **EPSG:7792 (RDN2008 / UTM 33N)**. For Sicily this is practically
identical to EPSG:25833; the difference is a few centimetres.

---

## 4. Make the plan readable on top of the cadastre

1. In the **Layers** panel drag **regimi normativi** to the top of the list.
2. Right-click it → **Properties → Symbology**. At the bottom open
   **Layer Rendering** and set **Opacity** to 50 %.
3. The legend now shows: **1** yellow, **2** green, **3** red, plus **Recupero**
   (hatched).
   - level 1 = lowest protection
   - level 2 = building in agricultural zones allowed, with a landscape authorisation
   - level 3 = as a rule no new building
4. Areas with no colour at all are outside the classified perimeter.

---

## 5. Go to the plot

**By coordinates** (fastest, if you have them): status bar at the bottom, field
**Coordinate** → type `X,Y` (for example `403799.11,4200376.07`) → Enter. Then set
**Scale** to `1:5000`.

If the status bar is hidden, enlarge the QGIS window; the bar is the bottom line with
Coordinate / Scale / Magnifier / Rotation.

**By eye:** zoom to the municipality, find the sheet number in the
**CP.CadastralZoning** labels, then zoom below 1:2,000 until the parcel numbers appear.

---

## 6. Read the classification (the important step)

1. In the **Layers** panel click **once** on **regimi normativi** so the row is
   highlighted. A double-click opens the properties instead — not what you want.
2. Activate **Identify Features**: the blue **i** in the top toolbar, or
   menu **View → Identify Features**, or `Ctrl+Shift+I` (`Cmd+Shift+I` on Mac).
3. Click once on the plan polygon covering the plot. The polygon is highlighted in red
   and the **Identify Results** panel opens on the right.

Read these fields:

| Field | Meaning |
|---|---|
| `Livello di tutela` (LIV_TUTELA) | protection level: 1, 2 or 3 |
| `PL` | local landscape unit, e.g. PL 21 — the article of the plan rules that applies |
| `Contesto` | context inside that unit, e.g. 21g |
| `crinali` | X = the reason is a ridge strip |
| `art.142 lett. c` | X = 150 m strip along a watercourse |
| `art.142 lett. g` | X = woodland |
| `art.10 archeologia`, `art.142 lett. m` | X = archaeological interest |
| `fondi e ville storiche` | X = historic estate or villa |
| `terrazzamento storico` | X = historic terracing |
| `art.134 lett. a` | X = area under a declaration of public interest (an older decree) |
| `OBJECTID`, `Shape_Area`, `Shape_Length` | id and size of the polygon — useful to cite |

The field that carries an **X** is the reason your plot has that level. Everything else
is empty.

If nothing is returned: the wrong layer is selected in the Layers panel, or you clicked
outside the perimeter.

---

## 7. Measure the distance to the boundary

1. Toolbar: **Measure Line** (the ruler), or `Ctrl+Shift+M`.
2. Click on the building site, then on the nearest point of the boundary between two
   levels, then double-click to finish.
3. The length in metres appears in the measurement window.

This number matters: a few metres suggests a line drawn imprecisely; several tens of
metres does not.

---

## 8. Find the rules that apply

1. Download the plan rules (Norme di Attuazione):
   `https://www.sitr.regione.sicilia.it/wp-content/uploads/2026/08/norme_attuazione_PA.pdf`
2. Search (`Ctrl+F` / `Cmd+F`) for:
   - `Art. 20` — what each protection level allows in general
   - your context code, e.g. `21g` — the specific bans and objectives
   - the reason word, e.g. `crinal`, to see how that component is treated
   - `Art. 67` — design rules for isolated houses in agricultural land

Art. 20 also contains the clause that boundaries between levels may undergo
"limitate e motivate variazioni" for conditions that cannot be verified at the scale of
the plan, on the Comune's initiative, with the Soprintendenza's evaluation.

---

## 9. Save what you found

- **Screenshot**: map with the highlighted polygon on the left, Identify Results on the
  right, scale visible. That single image documents the classification.
- **Keep the data**: right-click **regimi normativi** → **Export → Save Features As** →
  GeoPackage, so you still have it if the server changes.
- **Save the project**: `Ctrl+S` — the connections and layers are stored, not the data.

---

## 10. Query the server directly (no QGIS)

Useful for a second opinion or when QGIS is not at hand. Open this in a browser,
replacing LON and LAT with the longitude and latitude of the point:

```
https://map.sitr.regione.sicilia.it/gis/rest/services/piani_paesaggistici/pa_regimi_normativi/MapServer/2/query?geometry=LON,LAT&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=*&returnGeometry=false&f=html
```

The server returns the same fields as the Identify panel, in a plain web page.
`/MapServer/0/query` gives the local landscape unit, `/MapServer/1/query` the context.

---

## Common problems

| Symptom | Cause / fix |
|---|---|
| White screen | Nothing loaded or wrong extent: right-click OpenStreetMap → Zoom to Layer |
| Parcels invisible | Above 1:5,000 — zoom in further |
| Parcel numbers invisible | Above 1:2,000 — zoom in further |
| Plan colours hide the cadastre | Opacity 50 %, and move the layer to the top |
| Click returns nothing | Wrong layer selected in the Layers panel |
| Properties window opens instead | You double-clicked the layer; click once |
| Attribute table loads forever | It downloads all 70,499 polygons — abort, use Identify instead |
| Coordinate jump lands elsewhere | Digits missing in the field: clear it and paste the full value |
