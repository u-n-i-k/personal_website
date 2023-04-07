<template>
  <div class="locale-select" tabindex="1">
    <template v-for="locale in allLocales">
      <input type="radio" :id="locale" :value="locale" v-model="selectedLocale">
      <label :for="locale" class="locale-option"><span>{{ locale }}</span></label>
    </template>
  </div>
</template>

<script lang="ts">
import axios from 'axios';
import i18n from "@/i18n";
import store from "@/store";
enum Locale { ru = "ru", en = "en" };

function getSupportedLocales() {
  return Object.values(Locale);
}

function isLocaleSupported(locale: Locale | null) {
  return locale != null && getSupportedLocales().includes(locale)
}

function getLocaleIfSupported(locale: Locale | null) {
  return isLocaleSupported(locale) ? locale : null;
}

function getLocale() {
  const persistedLocale = store.state.locale as Locale;
  const browserLocale = window.navigator.language;

  return (
    getLocaleIfSupported(persistedLocale) ||
    getLocaleIfSupported(browserLocale as Locale) || 
    getLocaleIfSupported(browserLocale.split('-')[0] as Locale) ||
    Locale.ru
  );
}

export default {
  mounted() {
    this.setLocale(getLocale());
  },

  data() {
    return {
      selectedLocale: getLocale(),
      allLocales: getSupportedLocales()
    };
  },

  watch: {
    selectedLocale(newLocale, oldLocale) {
      this.setLocale(newLocale);
    }
  },

  methods: {
    setLocale(locale: Locale) {
      store.dispatch("change_locale", locale);
      i18n.global.locale.value = locale;
      axios.defaults.headers.common['Accept-Language'] = locale;
      document.querySelector('html')?.setAttribute('lang', locale);
      document.querySelector('html')?.setAttribute('lang', locale);
      document.title = this.$t('common.my_name') + this.$t('common.title_ending');
    }
  }
};
</script>

<style scoped>
.locale-select {
  --width: auto;
  --height: 40px;
  --radius: calc(var(--height) / 2);

  display: flex;
  flex-direction: column;
  align-items: center;
  vertical-align: middle;
  position: relative;
  width: var(--width);
  height: var(--height);

  color: var(--color-background);
  font-weight: bold;
  cursor: pointer;
}

.locale-option {
  display: flex;
  vertical-align: middle;
  align-items: center;
  margin: 0 auto;
  min-height: var(--height);
  background: var(--color-background-2);
  position: absolute;
  top: 0;
  width: var(--width);
  pointer-events: none;
  cursor: pointer;
  order: 2;
  z-index: 1;
  transition: background .4s ease-in-out;
  box-sizing: border-box;
  overflow: hidden;
  white-space: nowrap;
  border-radius: var(--radius);
}

.locale-select:focus .locale-option {
  position: relative;
  pointer-events: all;
}

input {
  opacity: 0;
  position: absolute;
  left: -99999px;
}

input:checked + label {
  order: 1;
  z-index: 2;
  background: var(--color-background-2);
  border-top: none;
  position: relative;
}

.locale-select:focus input:not(:checked) + label {
  top: 1px;
  border-radius: 0px 0px var(--radius) var(--radius);
}

/* TODO: fix for more then 2 options*/
.locale-select:focus input:checked + label {
  border-radius: var(--radius) var(--radius) 0px 0px;
}

label {
  width: 100%;
}

span {
  width: 100%;
  display: flex;
  justify-content: center;
  padding: 0 10px;
}
</style>
