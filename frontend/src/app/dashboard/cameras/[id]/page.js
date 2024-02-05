'use client'
import RTSPPlayer from '@/app/components/RTSPPlayer';
import { API_URL, routerBase } from '@/app/config/config';
import { useGlobalContext } from '@/app/context/store';
import axios from 'axios';
import Link from 'next/link'
import { useParams } from 'next/navigation';
import React, { useEffect, useState } from 'react'


export default function Camera() {
    const [camData, setCamData] = useState()
    const {state,setState}=useGlobalContext()
    const params=useParams()
    console.log("Router",params)
    const {id}  = params

    useEffect(() => {
        axios.get(API_URL + '/camera/cameras/' + id) // Replace with your API endpoint
            .then((response) => {
                console.log(response.data)
                const resData=response.data
                const updateData=state
                updateData.selectedCamera=resData
                setCamData(resData)
                setState(updateData)
            })
            .catch((error) => {
                console.error('Error fetching data:', error);
            });
    }, []);
    console.log(state)
    return (
        <div className=''>
            <div className='max-w-sm md:container px-8 mt-8'>

                {camData ?
                <>
                            <h1 className='text-3xl py-2 font-semibold text-gray'>{camData.name}</h1>

                    <div className='grid grid-cols-2 gap-4'>
                        <div>
                            <RTSPPlayer url={camData.video_link} />
                        </div>
                        <div>
                            <h2 className='text-xl py-2 font-semibold text-gray'>Camera Name:<span className='pl-4 text-black'> {camData.name}</span></h2>
                            <h2 className='text-xl py-2 font-semibold text-gray'>Link:<span className='pl-4 text-black'> {camData.video_link}</span></h2>
                            <h2 className='text-xl py-2 font-semibold text-gray'> Location:<span className='pl-4 text-black'> {camData.location}</span></h2>
                            <h2 className='text-xl py-2 font-semibold text-gray'> Address:<span className='pl-4 text-black'> {camData.name}</span></h2>
                            <div className='flex gap-4'>
                                <Link
                                    href={routerBase+"dashboard/cameras/edit/"+camData.id}
                                    className="flex w-full justify-center rounded-md bg-black px-3 py-3.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-black-600  "
                                >
                                    EDIT 
                                </Link>
                                <Link
                                    href={routerBase+"dashboard/cameras"}
                                    className="flex w-full justify-center rounded-md bg-white px-3 py-3.5 text-sm font-semibold leading-6 border-2 text-black shadow-sm hover:bg-black-600  "
                                >
                                    CANCEL 
                                </Link>
                            </div>
                        </div>

                    </div>
                    </>
                    : ""}

            </div>
        </div>
    )
}