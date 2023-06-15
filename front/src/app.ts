import { View, Map } from "ol";
import { defaults } from "ol/control";
import TileLayer from "ol/layer/Tile";
import OSM from "ol/source/OSM";
import { fromLonLat } from "ol/proj";
import { fromWatcher } from "./geo";
import { fromSearchInput } from "./search";
import { requestSearch } from "./request";
import { showList } from "./list";
import "ol/ol.css";

const runApp = async () => {
  const view = new View({ zoom: 16 });
  const map = new Map({
    target: "app",
    layers: [
      new TileLayer({
        source: new OSM(),
      }),
    ],
    controls: defaults({
      zoom: false,
    }),
    view,
  });

  let timeout = -1;

  const watchPosition = (value: GeolocationPosition) => {
    const {
      coords: { longitude, latitude },
    } = value;

    view.setCenter(fromLonLat([longitude, latitude]));
  };
  const watchSearch = (value: string) => {
    clearTimeout(timeout);
    timeout = setTimeout(async () => {
      const result = await requestSearch(value);
      showList(result);
    }, 1500);
  };

  await navigator.permissions.query({ name: "geolocation" });

  fromWatcher().subscribe(watchPosition);
  fromSearchInput().subscribe(watchSearch);
};

export { runApp };
