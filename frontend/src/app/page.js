"use client"
import {useRouter} from 'next/navigation'
import { useEffect } from 'react';
import { routerBase } from './config/config';

function HomePage({ isAuthenticated=true }) {
  const router = useRouter();
  console.log("Logged in",isAuthenticated)
  useEffect(()=>{
    if (!isAuthenticated) {
      router.push(`${routerBase}login`);
    }
    else{
      router.push(`${routerBase}dashboard`);
    }
  },[])
  return(
    <>Home</>
  )
  
}

export default HomePage;





