/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#0B0F14",
        panel: "#121821",
        line: "#232C38",
        mist: "#8A97A6",
        signal: {
          high: "#E5484D",
          medium: "#F5A524",
          low: "#3DD68C",
        },
        accent: "#5B8CFF",
      },
      fontFamily: {
        display: ["'JetBrains Mono'", "monospace"],
        body: ["'Inter'", "sans-serif"],
      },
    },
  },
  plugins: [],
};
