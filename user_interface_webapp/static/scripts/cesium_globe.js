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

// For this demo, start with all imagery disabled.
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

// Zoom to the Washington DC imagery
// viewer.zoomTo(imageryLayer);

// Add a button to toggle the display of the Bing Maps Labels Only layer
// Sandcastle.addToggleButton(
//   "Show Bing Maps Labels Only",
//   true,
//   (checked) => {
//     bingMapsLabelsOnly.show = checked;
//   }
// );

// The remaining code synchronizes the position of the slider with the split position
const slider = document.getElementById("slider");
viewer.scene.splitPosition =
  slider.offsetLeft / slider.parentElement.offsetWidth;

const handler = new Cesium.ScreenSpaceEventHandler(slider);

let moveActive = false;

function move(movement) {
  if (!moveActive) {
    return;
  }

  const relativeOffset = movement.endPosition.x;
  const splitPosition =
    (slider.offsetLeft + relativeOffset) /
    slider.parentElement.offsetWidth;
  slider.style.left = `${100.0 * splitPosition}%`;
  viewer.scene.splitPosition = splitPosition;
}

handler.setInputAction(function () {
  moveActive = true;
}, Cesium.ScreenSpaceEventType.LEFT_DOWN);
handler.setInputAction(function () {
  moveActive = true;
}, Cesium.ScreenSpaceEventType.PINCH_START);

handler.setInputAction(move, Cesium.ScreenSpaceEventType.MOUSE_MOVE);
handler.setInputAction(move, Cesium.ScreenSpaceEventType.PINCH_MOVE);

handler.setInputAction(function () {
  moveActive = false;
}, Cesium.ScreenSpaceEventType.LEFT_UP);
handler.setInputAction(function () {
  moveActive = false;
}, Cesium.ScreenSpaceEventType.PINCH_END);


//AIRPLANE MODEL CODE
// Function to create and show a model
function createModel(url, height) {
  viewer.entities.removeAll();

  const position = Cesium.Cartesian3.fromDegrees(
      -123.0744619,
      44.0503706,
      height
  );
  const heading = Cesium.Math.toRadians(135);
  const pitch = 0;
  const roll = 0;
  const hpr = new Cesium.HeadingPitchRoll(heading, pitch, roll);
  const orientation = Cesium.Transforms.headingPitchRollQuaternion(
      position,
      hpr
  );

  const entity = viewer.entities.add({
      name: url,
      position: position,
      orientation: orientation,
      model: {
          uri: url,
          minimumPixelSize: 128,
          maximumScale: 20000,
      },
  });
  viewer.trackedEntity = entity;
}

// Example button to trigger the airplane model
const airplaneButton = document.createElement('button');
airplaneButton.textContent = 'Show Airplane';
airplaneButton.addEventListener('click', function() {
  createModel("../SampleData/models/CesiumAir/Cesium_Air.glb", 5000.0);
});
document.getElementById('toolbar').appendChild(airplaneButton);



//TOGGLE SWITCH FOR DAY?NIGHT MODE
// Add the day/night mode toggle functionality
// document.getElementById('dayNightToggle').addEventListener('change', function() {
//   const label = document.getElementById('toggleLabel');
//   if (this.checked) {
//     viewer.scene.skyAtmosphere.hueShift = -0.8;
//     viewer.scene.skyAtmosphere.saturationShift = -0.7;
//     viewer.scene.skyAtmosphere.brightnessShift = -0.33;
//     viewer.scene.globe.enableLighting = true;
//     label.innerText = 'Day Mode';
//   } else {
//     viewer.scene.skyAtmosphere.hueShift = 0.0;
//     viewer.scene.skyAtmosphere.saturationShift = 0.0;
//     viewer.scene.skyAtmosphere.brightnessShift = 0.0;
//     viewer.scene.globe.enableLighting = false;
//     label.innerText = 'Night Mode';
//   }
// });