import '../scss/application.scss';
import '../images/homepage_wave.jpg';
// import 'bootstrap';
import { AutoComplete } from './plugins/autosearch.js';

console.log("Hello from webpack!");


new AutoComplete({
    el: "#autocomplete",
    threshold: 1,
    max_results: 7,
    key: 'name',
    secondary_key: 'country',
    api_endpoint: "http://localhost:8000/api/spots/",
})

