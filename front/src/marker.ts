import { Feature } from "ol";
import { Point } from "ol/geom";
import { fromLonLat } from "ol/proj";
import Style from "ol/style/Style";
import Icon from "ol/style/Icon";
import VectorLayer from "ol/layer/Vector";
import VectorSource from "ol/source/Vector";
import marker from "./assets/marker.svg";

const GlobalStyle = new Style({
  image: new Icon({
    anchor: [0.5, 24],
    anchorXUnits: "fraction",
    anchorYUnits: "pixels",
    src: marker,
    scale: 0.3,
  }),
});

export const createMarker = ([lat, lon]: [number, number]) => {
  const feature = new Feature({
    geometry: new Point(fromLonLat([lon, lat])),
  });

  return new VectorLayer({
    visible: true,
    style: GlobalStyle,
    source: new VectorSource({
      features: [feature],
    }),
  });
};
