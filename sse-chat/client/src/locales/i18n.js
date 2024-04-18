import i18next from 'i18next';
import {initReactI18next} from 'react-i18next';
import en from './en.json'
import zh from './zh.json'
import LanguageDetector from 'i18next-browser-languagedetector'


export const resources = {
    "en": {
        translation: en
    },
    "zh": {
        translation: zh
    }
}


i18next
    .use(LanguageDetector)
    .use(initReactI18next)
    .init({
        resources: resources,
        fallbackLng: "en", // use en if detected lng is not available
        debug: true,
        interpolation: {
            escapeValue: false, // not needed for react as it escapes by default
        }
    });

const key = {
    test :'test'
}
console.log(key.test);
