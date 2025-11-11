/* globals bootstrap:false, Prism:false */

(function () {
  'use strict';

  // //  Helper functions
  // function escapeHtml(html) {
  //   return html.replace(/×/g, '&times;')
  //              .replace(/«/g, '&laquo;')
  //              .replace(/»/g, '&raquo;')
  //              .replace(/←/g, '&larr;')
  //              .replace(/→/g, '&rarr;');
  // }

  // function cleanSource(html) {
  //   // Escape HTML, split the lines to an Array, remove empty elements
  //   // and finally remove the last element
  //   let lines = escapeHtml(html).split('\n').filter(Boolean).slice(0, -1);
  //   const indentSize = lines[0].length - lines[0].trim().length;
  //   const re = new RegExp(' {' + indentSize + '}');

  //   lines = lines.map(line => {
  //     return re.test(line) ? line.slice(Math.max(0, indentSize)) : line;
  //   });

  //   return lines.join('\n');
  // }

  // Add/remove `.navbar-transparent` on scroll; should probably be throttled later
  // function addNavbarTransparentClass() {
  //   const navBarElement = document.querySelector('#home > .navbar');

  //   if (!navBarElement) {
  //     return;
  //   }

  //   window.addEventListener('scroll', () => {
  //     const scroll = document.documentElement.scrollTop;

  //     if (scroll > 50) {
  //       navBarElement.classList.remove('navbar-transparent');
  //     } else {
  //       navBarElement.classList.add('navbar-transparent');
  //     }
  //   });
  // }



  // Toggle light and dark themes
  function toggleThemeMenu() {
    let themeMenu = document.querySelector('#theme-menu');

    if (!themeMenu) return;

    document.querySelectorAll('[data-bs-theme-value]').forEach(value => {
      value.addEventListener('click', () => {
        const theme = value.getAttribute('data-bs-theme-value');
        document.documentElement.setAttribute('data-bs-theme', theme);
      });
    });
  }




  toggleThemeMenu();

})();
