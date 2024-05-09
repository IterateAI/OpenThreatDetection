'use client'
import { API_URL, PUBLIC_URL } from '@/app/config/config';
import { useGlobalContext } from '@/app/context/store';
import axios from 'axios';
import Link from 'next/link'
import React, { useEffect, useState } from 'react'


export default  function Camera({params}) {
    const {state,setState}=useGlobalContext()
    const [data,setData]=useState()
    console.log(params)
    const {id}=params
    useEffect(()=>{
        axios.get(API_URL+'/event/events/'+id) // Replace with your API endpoint
        .then((response) => {
            console.log(response.data)
            const newArray=response.data
            setData(newArray);
        })
        .catch((error) => {
            console.error('Error fetching data:', error);
        });
    },[])
    
    // console.log(data)
    return (
        <div className=''>
            <div className='container px-8 mt-8'>
                <Link href={"/dashboard/notifications"}>
                    <div className='flex font-semibold mb-8'>
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
  <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
</svg>Back
</div>
                    </Link>
                <div className='grid grid-cols-2 '>
                    
                <div className=' pb-4'>
                    {data ? 
                            <div className=' pb-4'>
                                
                               
                                    <img className='hover:drop-shadow-lg hover:shadow-black' src={PUBLIC_URL+"/"+data.video_name+"/"+data.image_path} />
                                    <span className='font-semibold block mt-2 '>{data.video_name}</span>
                                    <span className=' block mt-2 '>{data.datetime}</span>
                                    <span className='font-semibold block mt-2 '>{data.status}</span>

                             
                            </div>
                            

                         : ""}
                         </div>
                         {/* <video controls width={640} height={360}>
                                    <source src={'http://localhost:5000/static/9mm_fast_walk.mp4'}/>
                                </video> */}

                </div>
                
            </div>
        </div>
    )
}