 'use client'

 import { createContext,useContext,Dispatch,SetStateAction,useState } from "react"

 const GlobalContext=createContext({
    state:[],
    setState:()=>[],
    alerts:[],
    setAlerts:()=>[]
    
 })

 export const GlobalContextProvider=({children})=>{
    const [state,setState]=useState(
        {
            cameras:[],
            selectedCamera:{},
        }
    )
    const [alerts,setAlerts]=useState([])
    return(
        <GlobalContext.Provider value={{state,setState,alerts,setAlerts}}>
            {children}
        </GlobalContext.Provider>
    )
 }

 export const useGlobalContext=()=>useContext(GlobalContext);