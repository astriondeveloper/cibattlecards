/* Library index: filtering + keyword search over the embedded JSON index. */
(function () {
  "use strict";
  var data = JSON.parse(document.getElementById("library-data").textContent);
  var tbody = document.getElementById("rows");
  var counter = document.getElementById("count");
  var controls = {
    q: document.getElementById("f-q"),
    market: document.getElementById("f-market"),
    agency: document.getElementById("f-agency"),
    vehicle: document.getElementById("f-vehicle"),
    tier: document.getElementById("f-tier"),
    status: document.getElementById("f-status"),
    relationship: document.getElementById("f-rel"),
    stale: document.getElementById("f-stale"),
  };

  function uniques(key) {
    var seen = {};
    data.forEach(function (c) { (c[key] || []).forEach(function (v) { seen[v] = 1; }); });
    return Object.keys(seen).sort();
  }

  function fill(select, values) {
    values.forEach(function (v) {
      var o = document.createElement("option");
      o.value = v; o.textContent = v;
      select.appendChild(o);
    });
  }
  fill(controls.market, uniques("markets"));
  fill(controls.agency, uniques("agencies"));
  fill(controls.vehicle, uniques("vehicles"));

  function chip(text, cls) {
    return '<span class="chip ' + (cls || "") + '">' + text + "</span>";
  }

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"]/g, function (ch) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[ch];
    });
  }

  function matches(c) {
    if (controls.q.value &&
        c.search.indexOf(controls.q.value.toLowerCase()) === -1) return false;
    if (controls.market.value && c.markets.indexOf(controls.market.value) === -1) return false;
    if (controls.agency.value && c.agencies.indexOf(controls.agency.value) === -1) return false;
    if (controls.vehicle.value && c.vehicles.indexOf(controls.vehicle.value) === -1) return false;
    if (controls.tier.value && String(c.tier) !== controls.tier.value) return false;
    if (controls.status.value && c.status !== controls.status.value) return false;
    if (controls.relationship.value && c.relationship !== controls.relationship.value) return false;
    if (controls.stale.checked && !c.stale) return false;
    return true;
  }

  function render() {
    var shown = data.filter(matches);
    tbody.innerHTML = shown.map(function (c) {
      var status = chip(esc(c.status), c.status);
      if (c.stale) status += " " + chip("stale " + c.age_days + "d", "stale");
      if (c.example) status += " " + chip("example", "example");
      return "<tr>" +
        '<td><a href="cards/' + c.slug + '.html"><strong>' + esc(c.name) + "</strong></a>" +
        (c.relationship !== "competitor" ? " " + chip(esc(c.relationship)) : "") + "</td>" +
        "<td>" + chip("T" + c.tier) + "</td>" +
        "<td>" + c.markets.map(function (m) { return chip(esc(m)); }).join(" ") + "</td>" +
        "<td>" + c.agencies.map(function (a) { return chip(esc(a)); }).join(" ") + "</td>" +
        "<td>" + status + "</td>" +
        '<td class="mini">' + esc(c.last_reviewed || "—") + "</td>" +
        '<td class="mini"><a href="cards/' + c.slug + '.html">card</a> · ' +
        '<a href="cards/' + c.slug + '-call.html">call</a> · ' +
        '<a href="share-safe/' + c.slug + '.html">share-safe</a></td>' +
        "</tr>";
    }).join("");
    counter.textContent = shown.length + " of " + data.length + " competitors";
  }

  Object.keys(controls).forEach(function (k) {
    controls[k].addEventListener("input", render);
  });
  render();
})();
