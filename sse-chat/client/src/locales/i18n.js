import i18next from 'i18next';
import {initReactI18next} from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector'
import en from './en.json'
import zh from './zh.json'

export const Support_Language = {
    zh: 'zh',
    en: 'en'
}


const resources = {
    [Support_Language.zh]: {translation: zh},
    [Support_Language.en]: {translation: en}
}


i18next
    .use(LanguageDetector)
    .use(initReactI18next)
    .init({
        resources: resources,
        fallbackLng: "en",
        debug: true,
        interpolation: {
            escapeValue: false,
        }
    });