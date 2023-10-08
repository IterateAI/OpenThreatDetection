"use client"
import {useRouter} from 'next/navigation'

function HomePage({ isAuthenticated=true }) {
  const router = useRouter();
  console.log("Logged in",isAuthenticated)

  if (!isAuthenticated) {
    router.push('/login');
    return null;
  }
  else{
    router.push('/dashboard');
    return null;
  }
}



export default HomePage;





