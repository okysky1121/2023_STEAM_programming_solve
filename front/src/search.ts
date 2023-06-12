import { Observable } from "rxjs";

export const fromSearchInput: () => Observable<string> = () => {
  const searchElement = <HTMLInputElement>(
    document.querySelector("#search input")
  );

  return new Observable((subscriber) => {
    searchElement.addEventListener("input", () => {
      const value = searchElement.value.trim();

      if (!!value) subscriber.next(value);
    });
  });
};
