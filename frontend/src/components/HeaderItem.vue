<script setup lang="ts">
import Icon from './icons/Icon.vue';
import ThemeToggleItem from './ThemeToggleItem.vue'
import LocaleSelectItem from './LocaleSelectItem.vue';
</script>

<template>
  <header>
    <div class="wrapper">
      <input type="checkbox" name="menu-toggle" id="menu-toggle" />

      <Icon />

      <label for="menu-toggle" class="menu-hamburger">
          <span class="line line1"></span>
          <span class="line line2"></span>
          <span class="line line3"></span>
      </label>
      
      <div class="menu">
        <div class="navigation">
          <a href="/">{{ $t("header.navigation.about") }}</a>
          <a href="/other">{{ $t("header.navigation.other") }}</a>
        </div>
        <div class="row-flex"><span>{{ $t("header.choose_lang") }}</span><LocaleSelectItem /></div>
        <div class="row-flex"><span>{{ $t("header.change_theme") }}</span><ThemeToggleItem /></div>
      </div>
    </div>
  </header>
</template>

<style scoped>
header {
  --height: 90px;
  --logo-size: calc(var(--height) - 30px);
  --logo-fill: var(--color-background-2);

  --hamburger-width: 32px;
  --hamburger-height: calc(var(--hamburger-width) / 1.4142);
  --hamburger-lines-thickness: 4px;
  height: var(--height);
  width: 100%;
  background-color: var(--color-background-3);
}

header .wrapper {
  flex-direction: row;
  flex-wrap: nowrap;
  justify-content: space-between;
  align-items: center;
}

#menu-toggle {
  display: none;
}

.navigation a {
  margin: 0;
  font-weight: bold;
  color: var(--color-text);
}
.navigation a:hover {
  color: var(--color-text-3);
}

@media screen and (max-width: 719px) {
  .menu-hamburger {
    width: var(--hamburger-width);
    height: var(--hamburger-height);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    z-index: 2;
  }

  .menu-hamburger .line {
    display: block;
    height: var(--hamburger-lines-thickness);
    width: 100%;
    border-radius: 10px;
    background: var(--color-background-2);
  }

  .menu-hamburger .line {
    transition: transform 0.4s ease-in-out;
  }

  input[type="checkbox"]:checked ~ .menu-hamburger .line1 {
    transform: translateY(calc((var(--hamburger-height) - var(--hamburger-lines-thickness)) / 2)) rotate(-45deg);
  }

  input[type="checkbox"]:checked ~ .menu-hamburger .line2 {
    transform: scaleX(0);
  }

  input[type="checkbox"]:checked ~ .menu-hamburger .line3 {
    transform: translateY(calc((var(--hamburger-lines-thickness) - var(--hamburger-height)) / 2)) rotate(45deg);
  }

  div.menu {
    position: fixed;
    top: 0;
    left: 0;
    padding: 0;
    margin: 0;
    height: 100vh;
    width: 100vw;

    transform: translateX(-100vw);
    display: flex;
    flex-wrap: wrap;
    transition: transform 0.4s ease-in-out;
    text-align: center;
    justify-content: space-around;
    align-items: center;
    background: var(--color-background-3);
    z-index: 1;
  }

  input[type="checkbox"]:checked ~ .menu {
    transform: translateX(0);
  }

  .navigation {
    display: flex;
    align-items: center;
    flex-direction: column;
    padding: 0;
    flex-basis: 100%;
  }

  .navigation a {
    padding: .5rem;
  }
  .row-flex {
    display: flex;
    flex-wrap: nowrap;
    align-items: center;
  }
}

@media screen and (min-width: 720px) {
  .menu-button {
    display: none;
  }

  .locale-select {
    padding: 0 10px;
  }

  .toggle-theme {
    padding-left: 10px;
  }

  .menu {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    justify-content: space-between;
    align-items: center;
  }

  .navigation {
    --height: 40px;
  }

  .navigation a{
    display: inline;
    padding: calc((var(--height) - 1rem) / 2) 10px;
  }

  .row-flex span {
    display: none;
  }
}
</style>
