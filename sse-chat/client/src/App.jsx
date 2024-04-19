import {useState} from 'react'
import {Button, createTheme, CssBaseline, ThemeProvider} from "@mui/material"
import {themes} from "./themes/theme.js";
import {useTranslation} from "react-i18next";
import {Support_Language} from "./locales/i18n.js"
import i18n, {t} from "i18next";
import {zhCN as core_zhCN, enUS as core_enUs} from "@mui/material/locale"
import { DataGrid } from '@mui/x-data-grid';
import {AdapterDayjs} from '@mui/x-date-pickers/AdapterDayjs';
import {LocalizationProvider} from "@mui/x-date-pickers/LocalizationProvider";

import {zhCN as dp_zhCN, enUS as dp_enUS} from "@mui/x-date-pickers/locales";
import {DatePicker} from '@mui/x-date-pickers/DatePicker';

import "dayjs/locale/zh.js"
import "dayjs/locale/en.js"

import {DateTimePicker} from "@mui/x-date-pickers";
import {zhCN as dg_zhCN, enUS as dg_enUS} from "@mui/x-data-grid/locales"


export default function App() {
    useTranslation()  // 需要在最頂層

    return (
        <Init>
            <Test/>
        </Init>
    )
}

// eslint-disable-next-line react/prop-types
function Init({children}) {
    const [lng, setLng] = useState(Support_Language[i18n.language])
    const [theme, setTheme] = useState(themes.light)

    const theme_lng = {
        [Support_Language.zh]: [dp_zhCN, dg_zhCN, core_zhCN],
        [Support_Language.en]: [dp_enUS, dg_enUS, core_enUs],
    }[lng]
    const themeWithLng = createTheme({...theme}, ...theme_lng)

    const lp_adapterLocale = {
        [Support_Language.zh]: 'zh',
        [Support_Language.en]: 'en',
    }[lng]

    // opt
    const lp_localText = {
        [Support_Language.zh]: dp_zhCN.components.MuiLocalizationProvider.defaultProps.localeText,
        [Support_Language.en]: dp_enUS.components.MuiLocalizationProvider.defaultProps.localeText,
    }[lng]


    return (
        <>
            <ThemeProvider theme={themeWithLng}>
            <CssBaseline enableColorScheme/>

                <LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale={lp_adapterLocale} localeText={lp_localText}>
                    {children}
                </LocalizationProvider>

                {Object.entries(themes).map(([themeName, theme]) =>
                    <Button key={themeName} onClick={() => setTheme(theme)}>{themeName}</Button>
                )}

                {/* eslint-disable-next-line no-unused-vars */}
                {Object.entries(Support_Language).map(([_, lng]) =>
                    <Button key={lng} onClick={() => {
                        setLng(lng)
                        i18n.changeLanguage(lng);
                    }}>{lng}</Button>
                )}

            </ThemeProvider>
        </>
    )

}

function Test() {

    const columns = [
        { field: 'col1', headerName: 'Column 1', width: 150 },
        { field: 'col2', headerName: 'Column 2', width: 150 },
    ];

    return <>
        <p>{t('test')}</p>
        <DatePicker/>
        <DateTimePicker />

        <DataGrid  columns={columns}/>
    </>
}
