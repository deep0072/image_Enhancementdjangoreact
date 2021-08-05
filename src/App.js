import logo from './logo.svg';

import './App.css';
import React, { useCallback, useEffect, useState } from 'react';
import axios from 'axios';

export default function App(){
  

  const [hist,setHist] = useState(0)

  const [filter, setfilter] = useState("")

  const [data,setData]= useState("")

  const fetchData = useCallback(()=>{
    axios.post("http://127.0.0.1:8000",
    {
      "image_path":"image.png",
      "attr": filter,
      "attr_val":hist
    })
    .then(res=>{
      // console.log(/res, "response")
      const data  = res.data;
      // console.log(data);
      setData(data)
    
      
    })

    
  
      // bfdjb

  })
// // 
// useEffect(()=>{
//   if(hist){
//   fetchData()
//   }
// }, [hist])



// clicking on button will call the fetch data
const CLicked = ()=>{

  fetchData()

}





return(
  <div>
    <h1>hello</h1>

    <img src={ `data:image/jpeg;base64,${data}`} style={{width:400,height:"auto"}} />

    {hist}

    <button onClick={CLicked}>press me</button>
    
    <input type="range" value={hist} onChange={e=>{setHist(e.target.value); setfilter("hist")}} min={0} max={20}/>
    <input type="range" value={hist} onChange={e=>{setHist(e.target.value); setfilter("gamma")}} min={0} max={20}/>
    <input type="range" value={hist} onChange={e=>{setHist(e.target.value); setfilter("contrast")}} min={0} max={20}/>
  </div>
)

}
