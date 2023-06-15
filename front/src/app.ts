import { View, Map } from "ol";
import { defaults } from "ol/control";
import TileLayer from "ol/layer/Tile";
import OSM from "ol/source/OSM";
import { fromLonLat } from "ol/proj";
import { fromWatcher, getCurrentPosition } from "./geo";
import { fromSearchInput } from "./search";
import { Location, requestNearby, requestSearch } from "./request";
import { showList } from "./list";
import { createMarker } from "./marker";
import "ol/ol.css";

const getMarkers = async (locs: Location[]) => {
  return locs.map(({ point }) => {
    return createMarker(<[number, number]>point.split(",").map(parseFloat));
  });
};

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

  const watchPosition = async (value: GeolocationPosition) => {
    const {
      coords: { longitude, latitude },
    } = value;

    const center = fromLonLat([longitude, latitude]);
    view.setCenter(center);

    const layers = await getMarkers(await requestNearby(latitude, longitude));
    for (let layer of layers) {
      map.addLayer(layer);
    }
  };
  const watchSearch = (value: string) => {
    clearTimeout(timeout);
    timeout = setTimeout(async () => {
      const result = await requestSearch(value);
      showList(result);
    }, 1500);
  };

  await navigator.permissions.query({ name: "geolocation" });
  watchPosition(await getCurrentPosition());

  fromWatcher().subscribe(watchPosition);
  fromSearchInput().subscribe(watchSearch);
};

export { runApp };
