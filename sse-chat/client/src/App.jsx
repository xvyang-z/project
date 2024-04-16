import {useEffect, useState} from 'react'


function App() {
  const [isDark, setIsDark] = useState(false)

    useEffect(() => {
        document.documentElement.className = isDark? 'dark' : 'light'
    }, [isDark]);

  return (
      <>
          <button onClick={() => setIsDark(!isDark)}>暗黑模式: {isDark ? 'on' : 'off'}</button>
          <p>this is text</p>
          <md-slider range value-start="25" value-end="75"></md-slider>
      </>
  )
}

export default App
