# Verificare una particella rispetto al Piano Paesaggistico di Palermo con QGIS

Come vedere, per qualsiasi terreno della provincia di Palermo, quale livello di tutela
gli attribuisce il Piano Paesaggistico adottato (D.A. n. 24/GAB del 10/06/2026), e per
quale motivo.

Tutto si basa su dati ufficiali e gratuiti: la cartografia catastale dell'Agenzia delle
Entrate e i servizi del Piano della Regione Siciliana (S.I.T.R.). Nessun account,
nessuna licenza.

---

## 0. Cosa serve

- QGIS (gratuito, qgis.org), versione 3.28 o successiva
- Connessione a internet — tutti i livelli si caricano in tempo reale dai server
- Foglio e numero di particella del terreno, oppure la sua posizione approssimativa

---

## 1. Aggiungere la mappa di sfondo

1. Pannello **Browser** → **XYZ Tiles** → doppio clic su **OpenStreetMap**.
2. Compare la mappa mondiale. Zoom sulla Sicilia, poi sul Comune.

Se il pannello Browser non si vede: menu **Visualizza → Pannelli → Browser**.

---

## 2. Aggiungere la cartografia catastale (Agenzia delle Entrate)

1. Nel **Browser**, tasto destro su **WMS/WMTS** → **Nuova connessione**.
2. Nome: `Catasto`
   URL: `https://wms.cartografia.agenziaentrate.gov.it/inspire/wms/ows01.php`
   → **OK**.
3. Espandere la connessione e fare doppio clic su questi livelli, in quest'ordine:
   - **CP.CadastralZoning** (bordi dei fogli, visibili da 1:200.000)
   - **CP.CadastralParcel** (particelle, visibili da 1:5.000)
   - **fabbricati** (fabbricati, da 1:5.000)
   - **codice_plla** (numeri di particella, da 1:2.000)

Le particelle restano invisibili finché non si scende sotto 1:5.000. È normale.

---

## 3. Aggiungere i livelli del Piano Paesaggistico (S.I.T.R.)

1. Nel **Browser**, tasto destro su **ArcGIS REST Servers** → **Nuova connessione**.
2. Nome: `Piano Paesaggistico Palermo`
   URL: `https://map.sitr.regione.sicilia.it/gis/rest/services/piani_paesaggistici/pa_regimi_normativi/MapServer`
   → **OK**.
3. Espandere e fare doppio clic su **regimi normativi** — scegliere la voce con il
   simbolo di *poligono*, non quella raster, altrimenti non si possono interrogare gli
   attributi.
4. Altri due servizi utili, da aggiungere allo stesso modo (stesso URL, ultima parte
   diversa):
   - `…/piani_paesaggistici/pa_componenti_paesaggio/MapServer` — componenti del
     paesaggio, comprese le linee di crinale tracciate dal Piano
   - `…/piani_paesaggistici/pa_beni_paesaggistici/MapServer` — beni paesaggistici

Il servizio lavora in **EPSG:7792 (RDN2008 / UTM 33N)**. In Sicilia è praticamente
identico a EPSG:25833: la differenza è di pochi centimetri.

---

## 4. Rendere leggibile il Piano sopra il catasto

1. Nel pannello **Livelli** trascinare **regimi normativi** in cima all'elenco.
2. Tasto destro → **Proprietà → Simbologia**. In fondo aprire
   **Visualizzazione livello** e impostare **Opacità** al 50 %.
3. La legenda mostra: **1** giallo, **2** verde, **3** rosso, più **Recupero**
   (tratteggiato).
   - livello 1 = tutela minima
   - livello 2 = in zona agricola l'edificazione è consentita, con autorizzazione
     paesaggistica
   - livello 3 = di norma esclusa ogni edificazione
4. Le aree senza colore sono fuori dal perimetro classificato.

---

## 5. Raggiungere il terreno

**Per coordinate** (il modo più rapido, se le si hanno): barra di stato in basso, campo
**Coordinata** → digitare `X,Y` (ad esempio `403799.11,4200376.07`) → Invio. Poi
impostare **Scala** su `1:5000`.

Se la barra di stato non si vede, ingrandire la finestra di QGIS: è la riga in basso con
Coordinata / Scala / Ingrandimento / Rotazione.

**A vista:** zoom sul Comune, individuare il numero del foglio nelle etichette di
**CP.CadastralZoning**, poi scendere sotto 1:2.000 finché compaiono i numeri di
particella.

---

## 6. Leggere la classificazione (il passaggio decisivo)

1. Nel pannello **Livelli** fare **un solo clic** su **regimi normativi**, in modo che la
   riga risulti evidenziata. Il doppio clic apre invece le proprietà.
2. Attivare **Informazioni elementi**: la **i** azzurra nella barra in alto, oppure menu
   **Visualizza → Informazioni elementi**, oppure `Ctrl+Maiusc+I` (`Cmd+Shift+I` su Mac).
3. Fare un clic sul poligono del Piano che copre il terreno. Il poligono si evidenzia in
   rosso e si apre il pannello **Risultati informazioni** a destra.

Campi da leggere:

| Campo | Significato |
|---|---|
| `Livello di tutela` (LIV_TUTELA) | livello di tutela: 1, 2 o 3 |
| `PL` | paesaggio locale, es. PL 21 — indica l'articolo delle NTA applicabile |
| `Contesto` | contesto all'interno del paesaggio locale, es. 21g |
| `crinali` | X = il motivo è la fascia di crinale |
| `art.142 lett. c` | X = fascia di 150 m lungo un corso d'acqua |
| `art.142 lett. g` | X = bosco |
| `art.10 archeologia`, `art.142 lett. m` | X = interesse archeologico |
| `fondi e ville storiche` | X = fondo o villa storica |
| `terrazzamento storico` | X = terrazzamenti storici |
| `art.134 lett. a` | X = area dichiarata di notevole interesse pubblico (decreto) |
| `OBJECTID`, `Shape_Area`, `Shape_Length` | id e dimensioni del poligono — utili da citare |

Il campo che riporta una **X** è la ragione del livello attribuito. Gli altri restano
vuoti.

Se non compare nulla: nel pannello Livelli è selezionato il livello sbagliato, oppure si
è cliccato fuori dal perimetro.

---

## 7. Misurare la distanza dal confine

1. Barra degli strumenti: **Misura linea** (il righello), oppure `Ctrl+Maiusc+M`.
2. Cliccare sul sedime, poi sul punto più vicino del confine tra due livelli, poi doppio
   clic per chiudere.
3. La lunghezza in metri compare nella finestra di misura.

Il dato conta: pochi metri suggeriscono una linea tracciata in modo impreciso; alcune
decine di metri no.

---

## 8. Trovare le norme applicabili

1. Scaricare le Norme di Attuazione:
   `https://www.sitr.regione.sicilia.it/wp-content/uploads/2026/08/norme_attuazione_PA.pdf`
2. Cercare (`Ctrl+F` / `Cmd+F`):
   - `Art. 20` — cosa consente in generale ciascun livello di tutela
   - il codice del contesto, es. `21g` — divieti e obiettivi specifici
   - la parola del motivo, es. `crinal`, per vedere come è trattata quella componente
   - `Art. 67` — regole per le costruzioni isolate in verde agricolo

L'art. 20 contiene anche la clausola per cui i perimetri tra i livelli possono subire
"limitate e motivate variazioni" per condizioni non verificabili alla scala del Piano, su
iniziativa dei Comuni e previa valutazione della Soprintendenza.

---

## 9. Conservare il risultato

- **Screenshot**: a sinistra la mappa con il poligono evidenziato, a destra i Risultati
  informazioni, con la scala visibile. Quell'unica immagine documenta la classificazione.
- **Salvare i dati**: tasto destro su **regimi normativi** → **Esporta → Salva elementi
  come** → GeoPackage, così restano anche se il server cambia.
- **Salvare il progetto**: `Ctrl+S` — vengono memorizzate le connessioni e i livelli, non
  i dati.

---

## 10. Interrogare il server direttamente (senza QGIS)

Utile per una controprova o quando QGIS non è a portata di mano. Aprire questo indirizzo
in un browser, sostituendo LON e LAT con longitudine e latitudine del punto:

```
https://map.sitr.regione.sicilia.it/gis/rest/services/piani_paesaggistici/pa_regimi_normativi/MapServer/2/query?geometry=LON,LAT&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=*&returnGeometry=false&f=html
```

Il server restituisce gli stessi campi del pannello informazioni, in una pagina web.
`/MapServer/0/query` dà il paesaggio locale, `/MapServer/1/query` il contesto.

---

## Problemi frequenti

| Sintomo | Causa / soluzione |
|---|---|
| Schermo bianco | Nulla caricato o inquadratura sbagliata: tasto destro su OpenStreetMap → Zoom sul livello |
| Particelle invisibili | Sopra 1:5.000 — avvicinarsi |
| Numeri di particella invisibili | Sopra 1:2.000 — avvicinarsi |
| I colori del Piano coprono il catasto | Opacità al 50 % e livello in cima all'elenco |
| Il clic non restituisce nulla | Livello sbagliato selezionato nel pannello Livelli |
| Si apre la finestra Proprietà | Doppio clic sul livello; farne uno solo |
| La tabella attributi non finisce di caricare | Scarica tutti i 70.499 poligoni — annullare e usare Informazioni elementi |
| Il salto alle coordinate porta altrove | Cifre mancanti nel campo: svuotarlo e incollare il valore completo |
