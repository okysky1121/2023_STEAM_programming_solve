import { EventEmitter } from "events";
import { Observable } from "rxjs";

type Listener<T> = (arg: T) => void;

export const requestPermission = () =>
  navigator.permissions.query({ name: "geolocation" });

export const getCurrentPosition: (
  opts?: PositionOptions
) => Promise<GeolocationPosition> = (opts) => {
  return new Promise((resolve, reject) => {
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        resolve(pos);
      },
      (err) => {
        reject(err);
      },
      opts
    );
  });
};

export const fromWatcher: (
  opts?: PositionOptions
) => Observable<GeolocationPosition> = (opts) => {
  const watcher = new PositionWatcher(opts);
  watcher.watch();

  return new Observable((subscriber) => {
    watcher
      .on("change", (pos) => {
        subscriber.next(pos);
      })
      .on("error", (err) => {
        subscriber.error(err);
      });
  });
};

export declare interface PositionWatcher {
  on(eventName: "change", listener: Listener<GeolocationPosition>): this;
  on(eventName: "error", listener: Listener<GeolocationPositionError>): this;

  off(eventName: "change", listener: Listener<GeolocationPosition>): this;
  off(eventName: "error", listener: Listener<GeolocationPositionError>): this;

  emit(eventName: "change", arg: GeolocationPosition): boolean;
  emit(eventName: "error", arg: GeolocationPositionError): boolean;
}

export class PositionWatcher extends EventEmitter {
  private handler: number = -1;

  readonly options: PositionOptions;

  constructor(opts: PositionOptions = {}) {
    super();
    this.options = opts;
  }

  watch() {
    this.handler = navigator.geolocation.watchPosition(
      (pos) => this.emit("change", pos),
      (err) => this.emit("error", err),
      this.options
    );
  }

  stop() {
    if (this.handler == -1) return;

    navigator.geolocation.clearWatch(this.handler);
    this.handler = -1;
  }
}
