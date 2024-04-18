import {useState} from 'react'
import {Button, CssBaseline, ThemeProvider} from "@mui/material"
import {themes} from "./themes/theme.js";
import {useTranslation} from "react-i18next";
import {resources} from "./locales/i18n.js"
import i18next from "i18next";


function App () {
    const [theme, setTheme] = useState(themes.light)
    useTranslation()

    return (
        <>
            <ThemeProvider theme={theme}>
                <CssBaseline enableColorScheme/>
                <Text/>
                {Object.entries(themes).map(([themeName, theme]) =>
                    <Button key={themeName} onClick={() => setTheme(theme)}>{themeName}</Button>
                )}
                {Object.entries(resources).map(([lng]) =>
                    <Button key={lng} onClick={() => {
                        i18next.changeLanguage(lng);
                    }}>{lng}</Button>
                )}

            </ThemeProvider>
        </>
    )
}

const Text = () => {
    return <p>{i18next.t('test')}</p>
}


export default App
