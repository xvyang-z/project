import {createTheme} from "@mui/material";

// 主题枚举
export const THEME = {
    light: 'light',
    dark: 'dark'
}

const darkTheme = createTheme({
    palette: {
        mode: 'dark',
    },
});

const lightTheme = createTheme({
    palette: {
        mode: 'light',
    },
});

export const themes = {
    'light': lightTheme,
    'dark': darkTheme
}