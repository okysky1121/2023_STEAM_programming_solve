import { Feature } from "ol";
import { Point } from "ol/geom";
import { fromLonLat } from "ol/proj";
import Icon from "ol/style/Icon";
import Style from "ol/style/Style";
import { Vector as SVector } from "ol/source";
import { Vector as LVector } from "ol/layer";

export const createMarker = ([lat, lon]: [number, number]) => {
  const feature = new Feature({
    geometry: new Point(fromLonLat([lon, lat])),
    style: new Style({
      image: new Icon({
        src: "",
      }),
    }),
  });

  return new LVector({
    visible: true,
    source: new SVector({
      features: [feature],
    }),
  });
};
