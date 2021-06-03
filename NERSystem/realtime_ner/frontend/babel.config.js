const env = require("./env.config");

module.exports = {
  presets: ["next/babel"],
  plugins: [
    ["styled-components", { ssr: true, displayName: true, preprocess: false }],
    ["transform-define", env]
  ]
};
