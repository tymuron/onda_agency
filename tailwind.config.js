/** Tailwind production build config.
 *  Scans every served HTML page (incl. examples) so JIT emits exactly the
 *  utility + arbitrary-value classes actually used. Replaces the runtime
 *  cdn.tailwindcss.com compiler (a Core Web Vitals / render-blocking cost).
 */
module.exports = {
  content: ["./frontend/**/*.html"],
  theme: { extend: {} },
  corePlugins: { preflight: true },
};
