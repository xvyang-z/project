import {useEffect, useState} from 'react';

export default function CatFriends() {
    const [show, setShow] = useState(false);
    const [text, setText] = useState('')


    return (
        <div>

            <button onClick={() => setShow(!show)}>{show ? '取消挂载' : '挂载'}</button>
            <hr/>
            {show && <Test text={text}/>}
            <button onClick={() => setText(text+'1')}>settext</button>

        </div>
    )
}

function Test({text}) {

    useEffect(
        () => {  // Effect 函数
            console.log('输入框值')
        },
        [text]  // 依赖项
    )
    useEffect(
        ()=>{
            console.log('[]')
        }, []
    )
    return <input value={text} onChange={e => setText(e.target.value)}></input>
}
