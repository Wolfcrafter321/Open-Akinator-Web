console.log("■ hello")

document.addEventListener("DOMContentLoaded", (ev) => {
    console.log("■ DOM content loaded")
})

window.addEventListener("load", (ev) => {
    console.log("■ window loaded")
})

import { mount } from 'svelte'
import App from './App.svelte'

mount(App, {target: document.getElementById('app')})
// new App({ // This is svelte4. mount is svelte5
//   target: document.body
// })