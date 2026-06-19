"use strict";

const MENU_URL = "menu_bilingual.json";
const LANGUAGE = document.documentElement.dir === "rtl" ? "ar" : "en";
const categoryLinks = document.getElementById("category-links");
const categoriesContainer = document.getElementById("categories");
const menuStatus = document.getElementById("menu-status");
const imageDialog = document.getElementById("image-dialog");
const enlargedImage = document.getElementById("enlarged-image");
let activeCategoryId = "";

function slugify(value) {
  return String(value)
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9\u0600-\u06ff]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

function localized(record, field) {
  return record?.[field]?.[LANGUAGE] || record?.[field]?.en || "";
}

function formatPrices(price) {
  const values = Array.isArray(price) ? price : [price];
  const fragment = document.createDocumentFragment();

  values.forEach((value, index) => {
    if (index > 0) {
      const separator = document.createElement("span");
      separator.className = "price-separator";
      separator.textContent = "–";
      fragment.append(separator);
    }

    const amount = document.createElement("span");
    amount.textContent = String(value);
    fragment.append(amount);

    const currency = document.createElement("span");
    currency.className = "riyal";
    currency.setAttribute("aria-label", "ريال سعودي");
    fragment.append(currency);
  });

  return fragment;
}

function createProductCard(product) {
  const article = document.createElement("article");
  article.className = "product-card";

  const button = document.createElement("button");
  button.className = "product-button";
  button.type = "button";

  const titleText = localized(product, "title");
  const descriptionText = localized(product, "description");
  button.setAttribute("aria-label", `عرض صورة ${titleText}`);

  const info = document.createElement("div");
  info.className = "product-info";

  const title = document.createElement("h3");
  title.textContent = titleText;

  const description = document.createElement("p");
  description.className = "product-description";
  description.textContent = descriptionText;

  const price = document.createElement("div");
  price.className = "product-price";
  price.append(formatPrices(product.price));

  info.append(title, description, price);

  const image = document.createElement("img");
  image.className = "product-image";
  image.src = product.imageCard || product.imageSmall || product.image;
  image.alt = titleText;
  image.width = 480;
  image.height = 360;
  image.loading = "lazy";
  image.decoding = "async";

  if (product.imageCard && product.imageSmall && product.image) {
    image.srcset = `${product.imageCard} 256w, ${product.imageSmall} 480w, ${product.image} 960w`;
    image.sizes = "(max-width: 480px) 122px, 148px";
  }

  image.addEventListener("error", () => {
    image.classList.add("is-broken");
  }, { once: true });

  button.addEventListener("click", () => {
    enlargedImage.src = product.imageLarge || product.image;
    enlargedImage.alt = titleText;
    imageDialog.showModal();
  });

  button.append(info, image);
  article.append(button);
  return article;
}

function createCategorySection(category, index) {
  const englishName = category?.category?.en || `category-${index + 1}`;
  const id = `category-${slugify(englishName) || index + 1}`;

  const section = document.createElement("section");
  section.className = "category-section";
  section.id = id;
  section.dataset.categoryIndex = String(index);

  const title = document.createElement("h2");
  title.className = "category-title";
  title.textContent = category?.category?.[LANGUAGE] || englishName;

  const list = document.createElement("div");
  list.className = "product-list";

  if (Array.isArray(category.products)) {
    const productFragment = document.createDocumentFragment();
    category.products.forEach((product) => {
      productFragment.append(createProductCard(product));
    });
    list.append(productFragment);
  }

  section.append(title, list);
  return { section, id, title: title.textContent };
}

function setActiveCategory(id) {
  if (id === activeCategoryId) {
    return;
  }
  activeCategoryId = id;

  categoryLinks.querySelectorAll(".category-link").forEach((link) => {
    const active = link.getAttribute("href") === `#${id}`;
    link.classList.toggle("is-active", active);
    link.setAttribute("aria-current", active ? "true" : "false");

  });
}

function observeCategories(sections) {
  if (!("IntersectionObserver" in window)) {
    return;
  }

  const observer = new IntersectionObserver((entries) => {
    const visible = entries
      .filter((entry) => entry.isIntersecting)
      .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];

    if (visible) {
      setActiveCategory(visible.target.id);
    }
  }, {
    rootMargin: "-72px 0px -55% 0px",
    threshold: [0.05, 0.25, 0.5],
  });

  sections.forEach((section) => observer.observe(section));
}

function renderMenu(menu) {
  const navFragment = document.createDocumentFragment();
  const categoryFragment = document.createDocumentFragment();
  const sections = [];

  menu.forEach((category, index) => {
    const rendered = createCategorySection(category, index);
    sections.push(rendered.section);
    categoryFragment.append(rendered.section);

    const link = document.createElement("a");
    link.className = "category-link";
    link.href = `#${rendered.id}`;
    link.textContent = rendered.title;
    link.setAttribute("aria-current", index === 0 ? "true" : "false");
    if (index === 0) {
      link.classList.add("is-active");
    }
    navFragment.append(link);
  });

  categoryLinks.replaceChildren(navFragment);
  categoriesContainer.replaceChildren(categoryFragment);
  menuStatus.hidden = true;
  observeCategories(sections);
}

async function loadMenu() {
  try {
    if (Array.isArray(window.ZALATAH_MENU_DATA) && window.ZALATAH_MENU_DATA.length > 0) {
      renderMenu(window.ZALATAH_MENU_DATA);
      return;
    }

    const response = await fetch(MENU_URL);
    if (!response.ok) {
      throw new Error(`Menu request failed with ${response.status}`);
    }

    const menu = await response.json();
    if (!Array.isArray(menu) || menu.length === 0) {
      throw new Error("Menu data is empty");
    }

    renderMenu(menu);
  } catch {
    categoryLinks.replaceChildren();
    menuStatus.hidden = false;
    menuStatus.classList.add("is-error");
    menuStatus.textContent = "تعذّر تحميل القائمة. فضلاً أعد المحاولة بعد قليل.";
  }
}

function closeDialog(dialog) {
  if (dialog?.open) {
    dialog.close();
  }
}

document.addEventListener("click", (event) => {
  const openButton = event.target.closest("[data-open-dialog]");
  if (openButton) {
    document.querySelectorAll("dialog[open]").forEach(closeDialog);
    document.getElementById(openButton.dataset.openDialog)?.showModal();
    return;
  }

  const closeButton = event.target.closest("[data-close-dialog]");
  if (closeButton) {
    closeDialog(closeButton.closest("dialog"));
  }
});

document.querySelectorAll("dialog").forEach((dialog) => {
  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) {
      closeDialog(dialog);
    }
  });
});

imageDialog.addEventListener("close", () => {
  enlargedImage.removeAttribute("src");
  enlargedImage.alt = "";
});

loadMenu();
