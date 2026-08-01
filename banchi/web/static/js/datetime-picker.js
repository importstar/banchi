document.addEventListener("DOMContentLoaded", function () {
  flatpickr(".js-datetime-picker", {
    enableTime: true,
    time_24hr: true,
    dateFormat: "d/m/Y H:i",
    allowInput: true,
  });
});
