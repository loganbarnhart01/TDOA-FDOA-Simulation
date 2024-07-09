// view intialization is done in main file, code to make the airplane model
function createModel(url, height, longitude, latitude) {
  // remove all existing entities from the viewer
  viewer.entities.removeAll();

  // calculate the Cartesian position from given longitude, latitude, and height
  const position = Cesium.Cartesian3.fromDegrees(
    longitude,
    latitude,
    height
  );

  // define heading, pitch, and roll for orientation (heading set to 135 degrees)
  const heading = Cesium.Math.toRadians(135);
  const pitch = 0;
  const roll = 0;
  const hpr = new Cesium.HeadingPitchRoll(heading, pitch, roll);

  // calculate quaternion orientation from heading-pitch-roll angles
  const orientation = Cesium.Transforms.headingPitchRollQuaternion(
    position,
    hpr
  );

  // create an entity with the specified URL, position, orientation, and model properties
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

  // set the tracked entity of the viewer to the created entity
  viewer.trackedEntity = entity;

  // return the created entity
  return entity;
}

// function to render the airplane
function renderAirplane(longitude, latitude, height) {
  // render the airplane model using the createModel function with specific parameters
  return createModel(
    "static/models/cirrus_sr22.glb",
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
