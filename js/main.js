(function () {
  "use strict";

  var input = document.querySelector("[data-poem-search]");
  if (!input) return;

  var list = document.querySelector("[data-poem-list]");
  var items = Array.prototype.slice.call(list.querySelectorAll("li"));
  var empty = document.querySelector("[data-no-results]");

  function normalize(str) {
    return (str || "").toLowerCase();
  }

  input.addEventListener("input", function () {
    var q = normalize(input.value.trim());
    var visible = 0;

    items.forEach(function (li) {
      var haystack = normalize(li.getAttribute("data-search"));
      var match = q === "" || haystack.indexOf(q) !== -1;
      if (match) {
        li.removeAttribute("hidden");
        visible++;
      } else {
        li.setAttribute("hidden", "");
      }
    });

    if (empty) {
      empty.classList.toggle("is-visible", visible === 0);
    }
  });
})();
