/*
 * 表示テーマの切替(自動 / ライト / ダーク)。
 * 自動は OS の設定に追従し、<html> に data-theme を付けない。選択は localStorage に保存する。
 * ちらつきを避けるため <head> で同期的に読み込む。
 */
(function () {
  var KEY = "ukatech-theme";
  var root = document.documentElement;

  function load() {
    try {
      var v = localStorage.getItem(KEY);
      return v === "light" || v === "dark" ? v : "auto";
    } catch (e) {
      return "auto";
    }
  }

  function save(value) {
    try {
      if (value === "auto") localStorage.removeItem(KEY);
      else localStorage.setItem(KEY, value);
    } catch (e) {}
  }

  function apply(value) {
    if (value === "auto") root.removeAttribute("data-theme");
    else root.setAttribute("data-theme", value);
  }

  apply(load());

  document.addEventListener("DOMContentLoaded", function () {
    var buttons = document.querySelectorAll("[data-theme-choice]");
    var group = document.querySelector(".theme-switch");
    if (group) group.hidden = false;

    function mark(value) {
      for (var i = 0; i < buttons.length; i++) {
        var on = buttons[i].getAttribute("data-theme-choice") === value;
        buttons[i].setAttribute("aria-pressed", on ? "true" : "false");
      }
    }

    mark(load());
    for (var i = 0; i < buttons.length; i++) {
      buttons[i].addEventListener("click", function () {
        var value = this.getAttribute("data-theme-choice");
        apply(value);
        save(value);
        mark(value);
      });
    }
  });
})();
