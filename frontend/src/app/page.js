"use client"
import {useRouter} from 'next/navigation'
import { useEffect } from 'react';

function HomePage({ isAuthenticated=true }) {
  const router = useRouter();
  console.log("Logged in",isAuthenticated)
  useEffect(()=>{
    if (!isAuthenticated) {
      router.push('/login');
      
    }
    else{
      router.push('/dashboard');
      
    }
  },[])
  return(
    <>Home</>
  )
  
}



export default HomePage;





