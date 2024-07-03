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
// init black marble layer and await its loading in an async function.
let blackMarbleLayer;

async function loadBlackMarbleLayer() {
  blackMarbleLayer = await Cesium.ImageryLayer.fromProviderAsync(
    Cesium.IonImageryProvider.fromAssetId(3812)
  );
}

loadBlackMarbleLayer();

// Event listener for the day/night mode toggle functionality.
document.getElementById('dayNightToggle').addEventListener('change', function () {
  const label = document.getElementById('toggleLabel');
  if (this.checked) {
    viewer.scene.skyAtmosphere.hueShift = -0.8;
    viewer.scene.skyAtmosphere.saturationShift = -0.7;
    viewer.scene.skyAtmosphere.brightnessShift = -0.33;
    viewer.scene.globe.enableLighting = false;
    label.innerText = 'Day Mode';

    // Add the black marble layer for night mode.
    if (blackMarbleLayer) {
      layers.add(blackMarbleLayer);
    }
  } else {
    viewer.scene.skyAtmosphere.hueShift = 0.0;
    viewer.scene.skyAtmosphere.saturationShift = 0.0;
    viewer.scene.skyAtmosphere.brightnessShift = 0.0;
    viewer.scene.globe.enableLighting = false;
    label.innerText = 'Night Mode';

    // Remove the black marble layer.
    if (blackMarbleLayer) {
      layers.remove(blackMarbleLayer);
    }
  }
});



// BUTTON & DOUBLE LEFT CLICK TO ADD AIRCRAFT (emitter) once 4 collectors have been placed
function renderAirplane() {
const airplaneButton = document.createElement('button');
airplaneButton.id = 'renderAirplaneButton';  // Add an ID to the button for styling
airplaneButton.textContent = 'Render Airplane';
airplaneButton.disabled = true; // Start disabled
airplaneButton.addEventListener('click', function() {
  createModel("../SampleData/models/CesiumAir/Cesium_Air.glb", 5000.0);
});

// Append the button to the beginning of the Cesium viewer toolbar in top right corner of ion container
const toolbar = document.querySelector('.cesium-viewer-toolbar');
toolbar.insertBefore(airplaneButton, toolbar.firstChild);

viewer.screenSpaceEventHandler.setInputAction(renderAirplane, Cesium.ScreenSpaceEventType.LEFT_DOUBLE_CLICK);
}



// USER INTERACTIVITY TO DROP POINTS ON MAP (THIS IS DONE BY RIGHT CLICKING)
//bettereer as a function for implementation purposes? 
let pointCount = 0;
const minPoints = 3;
const maxDistance = 500000; // 500km in meters
let lastPoint = null;

viewer.screenSpaceEventHandler.setInputAction((click) => {
  const cartesian = viewer.scene.pickPosition(click.position);
  if (Cesium.defined(cartesian)) {
    if (lastPoint && Cesium.Cartesian3.distance(lastPoint, cartesian) > maxDistance) {
      alert("Points must be within 500km of each other.");
      return;
    }

    const cartographic = Cesium.Cartographic.fromCartesian(cartesian);
    const lon = Cesium.Math.toDegrees(cartographic.longitude);
    const lat = Cesium.Math.toDegrees(cartographic.latitude);
    const height = cartographic.height;
    
    viewer.entities.add({
      position: Cesium.Cartesian3.fromDegrees(lon, lat, height),
      point: {
        pixelSize: 15,
        color: Cesium.Color.RED
      }
    });
    
    lastPoint = cartesian;
    pointCount++;
    if (pointCount >= minPoints) {
      airplaneButton.disabled = false;
    }
  }
}, Cesium.ScreenSpaceEventType.RIGHT_CLICK);



// Create the instruction window
const instructionWindow = document.createElement('div');
instructionWindow.id = 'instructionWindow';

// Create the content container
const contentContainer = document.createElement('div');
contentContainer.innerHTML = `
  <h2>geoleek Simulation Sandbox</h2> 
  <h3>Instructions:</h3> <br/>
  <p>1. Using the scroll wheel on the mouse, zoom in & zoom out on the globe. To reposition to a different region, you may also click and drag.</p>
  <p>2. To begin the simulation, please place 4 receivers by right clicking. Please note the receivers need to be placed within a 500km of one another.</p>
  <p>3. Double-click or use the 'Render Airplane' button and click to place an airplane withing 500km of the placed receivers. 
        Please note, a minimum of 4 receivers must be placed before an airplane can be populated. </p>
`;

// Style the instruction window
instructionWindow.style.cssText = `
  position: absolute;
  top: 150px;
  left: 10px;
  background-color: rgba(255, 255, 255, 0.7);
  color: black;
  border-radius: 5px;
  padding: 10px;
  font-family: Times New Roman;
  font-size: 20px;
  z-index: 1000;
  max-width: 450px;
  transition: all 0.3s ease;
`;

// Create the toggle button
const toggleButton = document.createElement('button');
toggleButton.innerHTML = '−'; // Unicode minus sign
toggleButton.style.cssText = `
  position: absolute;
  top: 5px;
  right: 5px;
  background: none;
  border: none;
  font-size: 28px;
  cursor: pointer;
`;

let isMinimized = false;

function toggleInstructions() {
  if (isMinimized) {
    // Expanding the simulation instructions window - style guidelines
    contentContainer.style.display = 'block';
    instructionWindow.style.cssText = `
      position: absolute;
      top: 150px;
      left: 10px;
      background-color: rgba(255, 255, 255, 0.7);
      color: black;
      border-radius: 5px;
      padding: 10px;
      font-family: Times New Roman;
      font-size: 20px;
      z-index: 1000;
      max-width: 450px;
      transition: all 0.3s ease;
      height: auto;
      width: auto;
      display: block;
    `;
    toggleButton.style.cssText = `
      position: absolute;
      top: 5px;
      right: 5px;
      background: none;
      border: none;
      font-size: 28px;
      cursor: pointer;
      color: black;
    `;
    toggleButton.innerHTML = '−';
  } else {
    // Minimizing the simulation instruction window
    contentContainer.style.display = 'none';
    instructionWindow.style.cssText = `
      position: absolute;
      top: 150px;
      left: 10px;
      background-color: rgba(0, 0, 0, 0.7);
      color: white;
      border-radius: 50%;
      padding: 0;
      font-family: Times New Roman;
      font-size: 20px;
      z-index: 1000;
      height: 40px;
      width: 40px;
      display: flex;
      justify-content: center;
      align-items: center;
      transition: all 0.3s ease;
    `;
    toggleButton.style.cssText = `
      position: static;
      background: none;
      border: none;
      font-size: 24px;
      cursor: pointer;
      color: white;
      line-height: 1;
    `;
    toggleButton.innerHTML = '+';
  }
  isMinimized = !isMinimized;
}


toggleButton.onclick = toggleInstructions;

// Assemble the instruction window
instructionWindow.appendChild(contentContainer);
instructionWindow.appendChild(toggleButton);

// Add the instruction window to the DOM
document.getElementById('cesiumContainer').appendChild(instructionWindow);



//AIRPLANE MODEL CODE
// Function to create and show a model
function setupEmitterControls() {
  initializeEmitterControls(viewer); //viewer define at beginning
}

function initializeEmitterControls(emitter) {
  let isEmitterPlacementEnabled = false;
  let emitterEntity = null;
  let lastPoint = null;
  let pointCount = 0;
  const minPoints = 4;
  const maxDistance = 500000;


  // button for rendering the emitter
  const emitterButton = document.createElement('button');
  emitterButton.id = 'renderEmitterButton';
  emitterButton.textContent = 'Render Aircraft';
  emitterButton.disabled = true;
  emitterButton.addEventListener('click', enableEmitterPlacement);
  //style for the button that is render (check Cesium toolbar)
  emitterButton.style.backgroundColor = '#8e8ebd';
  emitterButton.style.border = 'none';
  emitterButton.style.color = 'white';
  emitterButton.style.padding = '10px 20px';
  emitterButton.style.textAlign = 'center';
  emitterButton.style.textDecoration = 'none';
  emitterButton.style.display = 'inline-block';
  emitterButton.style.fontSize = '16px';
  emitterButton.style.fontFamily = 'Times New Roman';
  emitterButton.style.margin = '4px 2px';
  emitterButton.style.cursor = 'pointer';
  emitterButton.style.borderRadius = '4px';


  // hover effect for render aircraft button
  emitterButton.addEventListener('mouseover', function() {
    this.style.backgroundColor = '#8e8ebd';
  });
  emitterButton.addEventListener('mouseout', function() {
    this.style.backgroundColor = '#474772';
  });

  // add emitterButton into the Cesium toolbar
  const toolbar = document.querySelector('.cesium-viewer-toolbar');
  toolbar.insertBefore(emitterButton, toolbar.firstChild);

  function enableEmitterPlacement() {
    isEmitterPlacementEnabled = true;
    emitterButton.textContent = 'Emitter Placement Enabled';
    emitterButton.disabled = true;
    emitter.canvas.style.cursor = 'crosshair';
  }

  function renderEmitter(event) {
    if (!isEmitterPlacementEnabled) return;

    const earthPosition = emitter.scene.pickPosition(event.position);
    if (Cesium.defined(earthPosition)) {
      emitterEntity = createModel("../SampleData/models/CesiumAir/Cesium_Air.glb", earthPosition);
      isEmitterPlacementEnabled = false;
      emitter.canvas.style.cursor = 'move';

      emitter.screenSpaceEventHandler.setInputAction(dragEmitter, Cesium.ScreenSpaceEventType.MOUSE_MOVE);
      emitter.screenSpaceEventHandler.setInputAction(dropEmitter, Cesium.ScreenSpaceEventType.LEFT_CLICK);
    }
  }

  // function createModel(url, position) {
  //   const existingEmitter = emitter.entities.getById('emitter');
  //   if (existingEmitter) {
  //     emitter.entities.remove(existingEmitter);
  //   }

  //   const heading = Cesium.Math.toRadians(135);
  //   const pitch = 0;
  //   const roll = 0;
  //   const hpr = new Cesium.HeadingPitchRoll(heading, pitch, roll);
  //   const orientation = Cesium.Transforms.headingPitchRollQuaternion(position, hpr);

  //   return emitter.entities.add({
  //     id: 'emitter',
  //     name: url,
  //     position: position,
  //     orientation: orientation,
  //     model: {
  //       uri: url,
  //       minimumPixelSize: 128,
  //       maximumScale: 20000,
  //     },
  //   });
  // }
function createModel(url, position) {
  emitter.entities.removeAll();

  const heading = Cesium.Math.toRadians(135);
  const pitch = 0;
  const roll = 0;
  const hpr = new Cesium.HeadingPitchRoll(heading, pitch, roll);
  const orientation = Cesium.Transforms.headingPitchRollQuaternion(
    position,
    hpr
  );

  const entity = emitter.entities.add({
    name: url,
    position: position,
    orientation: orientation,
    model: {
      uri: url,
      minimumPixelSize: 128,
      maximumScale: 20000,
    },
  });
  emitter.trackedEntity = entity;
  return entity;
}

  function dragEmitter(movement) {
    if (emitterEntity) {
      const newPosition = emitter.scene.pickPosition(movement.endPosition);
      if (Cesium.defined(newPosition)) {
        emitterEntity.position = newPosition;
      }
    }
  }

  function dropEmitter(event) {
    if (emitterEntity) {
      const finalPosition = emitter.scene.pickPosition(event.position);
      if (Cesium.defined(finalPosition)) {
        emitterEntity.position = finalPosition;
      }

      emitter.screenSpaceEventHandler.removeInputAction(Cesium.ScreenSpaceEventType.MOUSE_MOVE);
      emitter.screenSpaceEventHandler.removeInputAction(Cesium.ScreenSpaceEventType.LEFT_CLICK);

      emitter.canvas.style.cursor = 'default';
      emitterButton.textContent = 'Enable Emitter Placement';
      emitterButton.disabled = false;
      isEmitterPlacementEnabled = false;
      emitterEntity = null;
    }
  }

  emitter.screenSpaceEventHandler.setInputAction((click) => {
    const cartesian = emitter.scene.pickPosition(click.position);
    if (Cesium.defined(cartesian)) {
      if (lastPoint && Cesium.Cartesian3.distance(lastPoint, cartesian) > maxDistance) {
        alert("Points must be within 500km of each other.");
        return;
      }

      const cartographic = Cesium.Cartographic.fromCartesian(cartesian);
      const lon = Cesium.Math.toDegrees(cartographic.longitude);
      const lat = Cesium.Math.toDegrees(cartographic.latitude);
      const height = cartographic.height;

      emitter.entities.add({
        position: Cesium.Cartesian3.fromDegrees(lon, lat, height),
        point: {
          pixelSize: 15,
          color: Cesium.Color.RED
        }
      });

      lastPoint = cartesian;
      pointCount++;
      if (pointCount >= minPoints) {
        emitterButton.disabled = false;
      }
    }
  }, Cesium.ScreenSpaceEventType.RIGHT_CLICK);

  emitter.screenSpaceEventHandler.setInputAction(renderEmitter, Cesium.ScreenSpaceEventType.LEFT_DOUBLE_CLICK);
}

// Call this function after the page has loaded and viewer is initialized
// You can do this by adding an event listener for DOMContentLoaded
document.addEventListener('DOMContentLoaded', setupEmitterControls);



