document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".js-tag-input").forEach(function (el) {
    var whitelist = [];
    try {
      whitelist = JSON.parse(el.dataset.tags || "[]");
    } catch (e) {
      whitelist = [];
    }

    new Tagify(el, {
      whitelist: whitelist,
      dropdown: { enabled: 0, maxItems: 20, closeOnSelect: false },
      originalInputValueFormat: function (valuesArr) {
        return valuesArr.map(function (item) { return item.value; }).join(",");
      },
    });
  });
});
