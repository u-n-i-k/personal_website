<template>
  <div class="toggle-theme">
    <label>
      <input
        type="checkbox"
        @change="toggleTheme"
        v-model="theme"
        true-value="light"
        false-value="dark"
      >
      <span class="slider"></span>
    </label>
  </div>
</template>

<script lang="ts">
  export default {
    mounted() {
      const initTheme = this.getTheme() || this.getMediaPreference();
      this.setTheme(initTheme);
    },

    data() {
      return {
        theme: this.getTheme(),
      };
    },

    methods: {
      toggleTheme() {
        const activeTheme = localStorage.getItem("theme");
        this.setTheme(activeTheme === "light" ? "dark" : "light");
      },

      getTheme() {
        return localStorage.getItem("theme");
      },

      setTheme(theme: string) {
        document.body.className = theme;
        localStorage.setItem("theme", theme);
      },

      getMediaPreference() {
        const prefersDark = window.matchMedia(
          "(prefers-color-scheme: dark)"
        ).matches;
        return prefersDark ? "dark" : "light";
      }
    }
  };
</script>

<style scoped>
.toggle-theme {
  --width: 80px;
  --height: calc(var(--width) / 2);
  --indent: 5px;
  --diameter: calc(var(--height) - 2 * var(--indent));

  display: block;
  height: var(--height);
  width: var(--width);
  min-width: var(--width);

  box-sizing: content-box;
}

label {
  display: block;
  width: 100%;
  height: 100%;
  background-color: var(--color-background-2);
  border-radius: calc(var(--height) / 2);
  cursor: pointer;
}

input {
  position: absolute;
  display: none;
}

.slider {
  display: block;
  width: 100%;
  height: 100%;
  border-radius: calc(var(--height) / 2);
  transition: 0.3s;
}

input:checked ~ .slider {
  background-color: var(--color-background-2);
}

.slider::before {
  content: "";
  position: absolute;
  top: var(--indent);
  left: var(--indent);
  width: var(--diameter);
  height: var(--diameter);
  border-radius: 50%;
  box-shadow: inset calc(2 * var(--indent)) calc(-1 * var(--indent)) 0px 0px var(--color-7);
  background-color: var(--color-background-2);
  transition: 0.3s;
}

input:checked ~ .slider::before {
  transform: translateX(calc(var(--width) - var(--diameter) - 2 * var(--indent)));
  background-color: var(--color-background);
  box-shadow: none;
}
</style>