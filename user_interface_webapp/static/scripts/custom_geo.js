// import '../styles/style.css';
// import * as THREE from 'three';
// import ThreeGlobe from 'three-globe';
// import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
// import countries from '../json/custom.geo.json';


// let renderer, camera, scene, controls;
// let mouseX = 0, mouseY = 0;
// let windowHalfX = window.innerWidth / 2;
// let windowHalfY = window.innerHeight / 2;
// let Globe;

// function init() {
//     renderer = new THREE.WebGLRenderer({ antialias: true });
//     renderer.setPixelRatio(window.devicePixelRatio);
//     renderer.setSize(window.innerWidth, window.innerHeight);
//     document.getElementById('three-container').appendChild(renderer.domElement);

//     scene = new THREE.Scene();
//     scene.background = new THREE.Color(0x000000);
//     scene.fog = new THREE.FogExp2(0x000000, 0.0009);

//     camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
//     camera.position.z = 400;

//     let ambientLight = new THREE.AmbientLight(0x404040);
//     scene.add(ambientLight);

//     let dLight1 = new THREE.DirectionalLight(0xffffff, 0.5);
//     dLight1.position.set(-800, 2000, 400);
//     camera.add(dLight1);

//     let dLight2 = new THREE.DirectionalLight(0x7982f6, 1);
//     dLight2.position.set(-200, 500, 200);
//     camera.add(dLight2);

//     scene.add(camera);

//     controls = new OrbitControls(camera, renderer.domElement);
//     controls.enableDamping = true;
//     controls.dampingFactor = 0.01;
//     controls.enablePan = false;
//     controls.minDistance = 200;
//     controls.maxDistance = 500;
//     controls.rotateSpeed = 0.8;
//     controls.zoomSpeed = 1;
//     controls.autoRotate = false;
//     controls.minPolarAngle = Math.PI / 3.5;
//     controls.maxPolarAngle = Math.PI - Math.PI / 3;

//     window.addEventListener('resize', onWindowResize, false);
//     document.addEventListener('mousemove', onMouseMove);

//     initGlobe();
// }

// function initGlobe() {
//     Globe = new ThreeGlobe({ waitForGlobeReady: true, animateIn: true })
//         .hexPolygonsData(countries.features)
//         .hexPolygonResolution(3)
//         .hexPolygonMargin(0.7)
//         .showAtmosphere(true)
//         .atmosphereColor('rgb(0,0,0)')
//         .atmosphereAltitude(0.25);

//     Globe.rotateY(-Math.PI * (5 / 9));
//     Globe.rotateZ(-Math.PI / 6);

//     const globeMaterial = Globe.globeMaterial();
//     globeMaterial.color = new THREE.Color(0x3a228a);
//     globeMaterial.emissive = new THREE.Color(0x220038);
//     globeMaterial.emissiveIntensity = 0.1;
//     globeMaterial.shininess = 0.7;

//     scene.add(Globe);
// }

// function onMouseMove(event) {
//     mouseX = event.clientX - windowHalfX;
//     mouseY = event.clientY - windowHalfY;
// }

// function onWindowResize() {
//     camera.aspect = window.innerWidth / window.innerHeight;
//     camera.updateProjectionMatrix();
//     renderer.setSize(window.innerWidth, window.innerHeight);
// }

// function animate() {
//     requestAnimationFrame(animate);
//     camera.position.x += (mouseX - camera.position.x) * 0.05;
//     camera.position.y += (-mouseY - camera.position.y) * 0.05;
//     camera.lookAt(scene.position);
//     controls.update();
//     renderer.render(scene, camera);
// }

// export { init, animate };