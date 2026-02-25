/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./node_modules/@tremor/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        tremor: {
          brand: {
            faint: "#eff6ff",
            muted: "#bfdbfe",
            subtle: "#60a5fa",
            DEFAULT: "#3b82f6",
            emphasis: "#1d4ed8",
            inverted: "#ffffff",
          },
          background: {
            muted: "#0F1113",
            subtle: "#0B0B0C",
            DEFAULT: "#0F1113",
            emphasis: "#23262B",
          },
          border: {
            DEFAULT: "#23262B",
          },
          ring: {
            DEFAULT: "#23262B",
          },
          content: {
            subtle: "#8B8F96",
            DEFAULT: "#EAECEF",
            emphasis: "#EAECEF",
            strong: "#FFFFFF",
            inverted: "#000000",
          },
        },
      },
      borderRadius: {
        "tremor-small": "0.375rem",
        "tremor-default": "0.5rem",
        "tremor-full": "9999px",
      },
    },
  },
  plugins: [],
};

