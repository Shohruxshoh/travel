/**
 * vue-i18n Configuration
 * Supports three languages: Russian (RU), English (EN), French (FR).
 * Default locale is English.
 */

import { createI18n } from 'vue-i18n'
import ru from './ru.json'
import en from './en.json'
import fr from './fr.json'

const i18n = createI18n({
    legacy: false,              // Use Composition API mode
    locale: 'en',               // Default language
    fallbackLocale: 'en',       // Fallback if translation is missing
    messages: { ru, en, fr },
})

export default i18n
