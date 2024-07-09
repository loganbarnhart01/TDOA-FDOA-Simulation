// This example showcases the ability to overlay labels
// on top of unlabeled imagery.
//
// On the left side is Bing Maps Aerial With Labels + unlabeled high
// resolution Washington DC imagery. The labels are obscured by the
// DC imagery and can not be turned on or off independently.
//
// On the right side is Bing Maps Aerial + unlabeled high resolution
// Washington DC imagery + Bing Maps Labels Only. The labels
// are now on top of all imagery in the scene and can be independently
// shown or hidden based on app configuration and/or camera zoom level.


// RENDERING OF CESIUM ION CONTAINER in GLOBE page. 
const viewer = new Cesium.Viewer("cesiumContainer", {
    baseLayer: false,
    baseLayerPicker: false,
    infoBox: false,
  });
  
  const layers = viewer.imageryLayers;
  
  // Add Bing Maps Aerial with Labels to the left panel
  const bingMapsAerialWithLabels = Cesium.ImageryLayer.fromProviderAsync(
    Cesium.IonImageryProvider.fromAssetId(3)
  );
  bingMapsAerialWithLabels.splitDirection = Cesium.SplitDirection.LEFT;
  layers.add(bingMapsAerialWithLabels);
  
  // Add Bing Maps Aerial (unlabeled) to the right panel
  const bingMapsAerial = Cesium.ImageryLayer.fromProviderAsync(
    Cesium.IonImageryProvider.fromAssetId(2)
  );
  bingMapsAerial.splitDirection = Cesium.SplitDirection.RIGHT;
  layers.add(bingMapsAerial);
  
  // Add high resolution Washington DC imagery to both panels.
  const imageryLayer = Cesium.ImageryLayer.fromProviderAsync(
    Cesium.IonImageryProvider.fromAssetId(3827)
  );
  viewer.imageryLayers.add(imageryLayer);
  
  // Add Bing Maps Labels Only to the right panel
  const bingMapsLabelsOnly = Cesium.ImageryLayer.fromProviderAsync(
    Cesium.IonImageryProvider.fromAssetId(2411391)
  );
  bingMapsLabelsOnly.splitDirection = Cesium.SplitDirection.RIGHT; // Only show to the left of the slider.
  layers.add(bingMapsLabelsOnly);
  
  
  // DARK MODE IMPLEMENTATION - note that the map renders in night mode but the city & road features are no longer visible. 
  
let blackMarbleLayer = null;  // Initialize the layer variable but do not load until needed.

async function ensureBlackMarbleLayer() {
    if (!blackMarbleLayer) {  // Only load if not already loaded.
        blackMarbleLayer = await Cesium.ImageryLayer.fromProviderAsync(
            Cesium.IonImageryProvider.fromAssetId(3812)
        );
    }
}

document.getElementById('dayNightToggle').addEventListener('change', async function () {
    const label = document.getElementById('toggleLabel');
    await ensureBlackMarbleLayer();  // Ensure layer is loaded before toggling.
    
    if (this.checked) {
        viewer.scene.skyAtmosphere.hueShift = -0.8;
        viewer.scene.skyAtmosphere.saturationShift = -0.7;
        viewer.scene.skyAtmosphere.brightnessShift = -0.33;
        viewer.scene.globe.enableLighting = false;
        label.innerText = 'Night Mode';

        // Add the black marble layer for night mode.
        viewer.imageryLayers.add(blackMarbleLayer);
    } else {
        viewer.scene.skyAtmosphere.hueShift = 0.0;
        viewer.scene.skyAtmosphere.saturationShift = 0.0;
        viewer.scene.skyAtmosphere.brightnessShift = 0.0;
        viewer.scene.globe.enableLighting = false;
        label.innerText = 'Day Mode';

        // Remove the black marble layer if previously added.
        viewer.imageryLayers.remove(blackMarbleLayer, true);  // Use `true` for destroy to properly clean up.
        blackMarbleLayer = null;  // Reset the layer variable.
    }
});

console.log("flightData Type:", flightData)
console.log(Array.isArray(flightData))

// This function uses embedded flight data to plot points
function addFlightDataToGlobe() {
    if (typeof flightData === "string") {
        flightData = JSON.parse(flightData);
    }

    // Group data by TIME to synchronize all flight updates
    const groupedByTime = groupBy(flightData, 'TIME');
    const timestamps = Object.keys(groupedByTime).sort((a, b) => a - b);

    let currentTimestampIndex = 0;
    let flightEntities = {};

    function updateEntities() {
        const currentTime = timestamps[currentTimestampIndex];
        const flightsAtCurrentTime = groupedByTime[currentTime];

        flightsAtCurrentTime.forEach(flight => {
            const icao = flight.ICAO;
            const position = Cesium.Cartesian3.fromDegrees(parseFloat(flight.LON), parseFloat(flight.LAT));

            if (!flightEntities[icao]) {
                // First occurrence of this ICAO; create new entities
                flightEntities[icao] = {
                    positions: [position],
                    polyline: viewer.entities.add({
                        polyline: {
                            positions: new Cesium.CallbackProperty(() => flightEntities[icao].positions, false),
                            width: 3,
                            material: Cesium.Color.YELLOW.withAlpha(0.75)
                        }
                    }),
                    point: viewer.entities.add({
                        position: position,
                        point: {
                            pixelSize: 10,
                            color: Cesium.Color.ORANGE,
                            outlineColor: Cesium.Color.WHITE,
                            outlineWidth: 2
                        },
                        label: {
                            text: `ICAO: ${icao}`,
                            font: '14pt monospace',
                            style: Cesium.LabelStyle.FILL_AND_OUTLINE,
                            outlineWidth: 2,
                            verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
                            pixelOffset: new Cesium.Cartesian2(0, -9)
                        }
                    })
                };
            } else {
                // Update existing polyline and point
                flightEntities[icao].positions.push(position);
                flightEntities[icao].point.position = position;
                flightEntities[icao].point.label.text = `ICAO: ${icao}`;
            }
        });

        currentTimestampIndex++;
        if (currentTimestampIndex >= timestamps.length) {
            currentTimestampIndex = 0;  // Reset for looping
            Object.keys(flightEntities).forEach(icao => {
                flightEntities[icao].positions = [];
            });
        }
        setTimeout(updateEntities, 1000);  // Adjust timing as necessary
    }

    updateEntities();  // Start the update process
}

// Helper function to group by a key
function groupBy(array, key) {
    return array.reduce((result, currentValue) => {
        (result[currentValue[key]] = result[currentValue[key]] || []).push(currentValue);
        return result;
    }, {});
}
// Call the function to add data to the globe as part of the page loading process
document.addEventListener('DOMContentLoaded', addFlightDataToGlobe);