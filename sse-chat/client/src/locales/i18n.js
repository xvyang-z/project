import i18next from 'i18next';
import {initReactI18next} from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector'
import en from './en.json'
import zh from './zh.json'

import {zhCN as date_pickers_zhCN, enUS as date_pickers_enUS} from "@mui/x-date-pickers/locales";
import {zhCN as data_grid_zhCN, enUS as data_grid_enUS} from "@mui/x-data-grid/locales";
import {zhCN as core_zhCN, enUS as core_enUs} from "@mui/material/locale";
import "dayjs/locale/zh.js"
import "dayjs/locale/en.js"

// 语言枚举
export const LANGUAGE = {
    zh: 'zh',
    en: 'en'
}

// 项目语言 : createTheme 时注入的语言
export const createTheme_languages = {
    [LANGUAGE.zh]: [date_pickers_zhCN, data_grid_zhCN, core_zhCN],
    [LANGUAGE.en]: [date_pickers_enUS, data_grid_enUS, core_enUs],
}

// 项目语言 : x-date-picker 中用到 dayjs 中的语言包名 (影响 x-date-picker 组件的部分文字)
export const LocalizationProvider_adapterLocale = {
    [LANGUAGE.zh]: 'zh',
    [LANGUAGE.en]: 'en',
}

// 初始化 i18n 的语言资源
const resources = {
    [LANGUAGE.zh]: {translation: zh},
    [LANGUAGE.en]: {translation: en}
}


i18next
    .use(LanguageDetector)
    .use(initReactI18next)
    .init({
        resources: resources,
        fallbackLng: "zh",
        debug: true,
        interpolation: {
            escapeValue: false,
        }
    });