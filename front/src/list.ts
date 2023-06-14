import { Location } from "./request";

const list = document.getElementById("list")!;

export const toggleList = () => list.classList.toggle("hide");

export const createListItem = (loc: Location) => {
  const item = document.createElement("div");
  item.classList.add("item");

  const name = document.createElement("span");
  name.classList.add("name");
  name.textContent = loc.name;

  const address = document.createElement("span");
  address.classList.add("address");
  address.textContent = loc.address;

  item.replaceChildren(name, address);

  return item;
};

export const showList = (locs: Location[]) => list.replaceChildren(...locs.map(createListItem));