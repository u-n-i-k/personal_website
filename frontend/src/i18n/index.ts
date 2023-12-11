import { createI18n } from 'vue-i18n'

import ru from "./locales/ru.json";
import en from "./locales/en.json";

export default createI18n({
    locale: "ru",
    fallbackLocale: "ru",
    messages: { en, ru },
    legacy: false,
    globalInjection: true
  }
)
