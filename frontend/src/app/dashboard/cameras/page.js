'use client'
import { API_URL, routerBase } from '@/app/config/config';
import { useGlobalContext } from '@/app/context/store';
import axios from 'axios';
import Link from 'next/link'
import React, { useEffect, useState } from 'react'


export default function AllCamera() {
    const [data, setData] = useState([]);
    const {state,setState}=useGlobalContext()
   
    useEffect(()=>{
        axios.get(API_URL+'/camera/cameras') // Replace with your API endpoint
        .then((response) => {
            console.log(response.data)
            const updateData=state
            updateData.cameras=response.data
            setState(updateData)
            setData(response.data);
        })
        .catch((error) => {
            console.error('Error fetching data:', error);
        });
    }, []);
    console.log("Global State",state)
    return (
        <div className=''>
            <div className='container px-8 mt-8'>
                <h1 className='text-3xl py-2 font-semibold mb-8'>All Cameras</h1>
                <ul className='grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4'>
                   
                    {state.cameras ? state.cameras.map((item, key) => {
                        return (
                            <li key={key} className=''>
                                <Link href={routerBase+"dashboard/cameras/"+item.id} className=''>
                                   <div className='bg-white drop-shadow-md  hover:text-black-600 hover:drop-shadow-lg hover:shadow-black px-2 pb-4 p-2'> <img className='rounded-lg ' src={routerBase+"images/cam1.png"} />
                                    <div className='pl-2'>
                                    <span className='font-semibold block mt-2 '>{item.name}</span>
                                    <span className=' block mt-2 '>{item.location}</span>
                                    </div>
                                    </div>
                                </Link>
                            </li>

                        )
                    }) : ""}
                </ul>
            </div>
        </div>
    )
}