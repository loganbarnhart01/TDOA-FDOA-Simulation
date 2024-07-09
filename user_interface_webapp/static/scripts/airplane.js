//view intialization is done in main file, code to make the airplane model
function createModel(url, height, longitude, latitude) {
  viewer.entities.removeAll();

  const position = Cesium.Cartesian3.fromDegrees(
    longitude,
    latitude,
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
  return entity;
}

// function to render the airplane
function renderAirplane(longitude, latitude, height) {
  return createModel(
    "../SampleData/models/CesiumAir/Cesium_Air.glb",
    height,
    longitude,
    latitude
  );
}

// export the function so it can be used in other files
if (typeof module !== 'undefined' && typeof module.exports !== 'undefined') {
  module.exports = {
    renderAirplane: renderAirplane
  };
}