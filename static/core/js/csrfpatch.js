// Patches window.fetch to automatically include the CSRF token header
// on all non-safe HTTP methods. Loaded as an external script so it can
// be referenced by a nonce in the Content-Security-Policy.
(function () {
  var _f = window.fetch;
  window.fetch = function (u, o) {
    o = o || {};
    var m = (o.method || 'GET').toUpperCase();
    if (m !== 'GET' && m !== 'HEAD') {
      var c = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
      if (c) {
        o.headers = Object.assign({}, o.headers, {
          'X-CSRFToken': decodeURIComponent(c[1]),
        });
      }
    }
    return _f.call(this, u, o);
  };
})();
