//globe rendering page
import * as THREE from 'three';

//renders all the 3D stuff we are going to make
// const renderer = new THREE.WebGLRenders(); 

//set the height and width properites for 3d rendering
// renderer.setSize(window.innerWidth, window.innerHeight); 

const scene = new THREE.Scene()
const camera = new THREE.
    PerspectiveCamera (75, window.innerWidth / window.innerHeight, 0.1, 1000)

const renderer = new THREE.WebGLRenderer();
CanvasRenderingContext2D.setSize(innerWidth, innerHeight)
document,body.appendChild(renderer.domElement)
