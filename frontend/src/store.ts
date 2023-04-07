import { createStore } from 'vuex'

const store = createStore({
  state () {
    return {
      locale: localStorage.getItem("locale"),
      theme: localStorage.getItem("theme")
    }
  },
  mutations: {
    change_locale (state, newLocale: string) {
      localStorage.setItem("locale", newLocale);
      state.locale = newLocale;
    },
    change_theme (state, newTheme: string) {
      localStorage.setItem("theme", newTheme);
      state.theme = newTheme;
    }
  },
  actions: {
    change_locale (state, newLocale: string) {
      state.commit("change_locale", newLocale)
    },
    change_theme (state, newTheme: string) {
      state.commit("change_theme", newTheme)
    }
  },
  getters: {
    locale (state) {
      return state.locale
    },
    theme (state) {
      return state.theme
    }
  }
});

export default store;