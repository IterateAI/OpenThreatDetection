'use client'
import DataTable  from '@/app/components/DataTable';
import { API_URL, PUBLIC_URL } from '@/app/config/config';
import { useGlobalContext } from '@/app/context/store';
import { getTimeDelay } from '@/app/utils/utils';

import axios from 'axios';
import Link from 'next/link'
import React, { useEffect, useState } from 'react'
import { io } from "socket.io-client";
const socket = io("http://localhost:5001");

const threat_data = {
    location: "Main Entrance",
    weapon: "Gun",
    detection_accuracy: "89%",
    date: "April 14, 2023",
    cameraId: "N-234-5581"
}

const threat_list = [
    {
        location: "Main Entrance",
        thumbnail: "/images/Gunman.png",
        time: "30 Seconds",
        duration: "0.1:24",
        id: "N-234-5581"
    },
    {
        location: "Main Entrance",
        thumbnail: "/images/cam1.png",
        time: "30 Seconds",
        duration: "0.1:24",
        id: "N-234-5581"
    },
    {
        location: "Main Entrance",
        thumbnail: "/images/cam2.png",
        time: "30 Seconds",
        duration: "0.1:24",
        id: "N-234-5581"
    }
]

const Notifications = () => {
    const [threatSate, setThreatState] = useState(false)
    const {alerts,setAlerts}=useGlobalContext()
    const [notification, setNotification] = useState();
    


    const [data, setData] = useState([]);
    

    useEffect(() => {
        axios.get(API_URL+'/event/events') // Replace with your API endpoint
        .then((response) => {
            console.log(response.data)
            const newArray = response.data.reverse().slice(0, 6);
            setData(newArray);
        })
        .catch((error) => {
            console.error('Error fetching data:', error);
        });
    }, []);

    
    return (
        <div className=''>
            
            {alerts.length!=0 ?
                <div className=''>
                    <div className='text-lg border-b-2 border-red font-semibold text-center  flex justify-center items-center py-4'><img className='w-5 mx-2 h-4' src="/images/Warning.png" />Threat Detected</div>
                    <div className='md:grid px-4 py-4 gap-4 grid-cols-2'>
                        <div className='max-w-2xl'>
                            {/* <Link href={"/dashboard/notifications/"+0}> */}
                            <img src={PUBLIC_URL+"/"+ alerts.video_name+"/"+ alerts.image_path} alt='thumbnail' />
                            {/* </Link> */}
                        </div>
                        <div className='px-4 py-4 '>
                            <div className='font-semibold text-lg'>{alerts.datetime}</div>
                            <div className='font-semibold text-lg'>{alerts.video_name}</div>
                            <div>Weapon: {alerts.Threat_status}</div>
                            {/* <div>Detection Accuracy: {notification.detection_accuracy}</div> */}
                            {/* <div>Date: {notification.date}</div>
                            <div>Camera ID: {notification.cameraId}</div> */}
                            <div className='relative hidden md:block mt-12'>
                                <button
                                    type="submit"
                                    className="flex w-full justify-center rounded-md bg-red px-3 py-3.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-black  "
                                >
                                    CALL POLICE
                                </button>

                            </div>
                        </div>
                    </div>
                </div>
                :
                <div>
                    <div className='text-lg border-b-2 border-red font-semibold text-center  flex justify-center items-center py-4'>No Threat Detected</div>
                    <div className='md:grid grid-cols-6'>

                    </div>
                </div>
            }
            <div className='fixed block md:hidden w-screen md:w-80 z-50  px-4 py-4 bottom-0 right-0 bg-black-100 md:bg-white drop-shadow-lg md:drop-shadow-none'>
                <button
                    type="submit"
                    className="flex w-full justify-center rounded-md bg-red px-3 py-3.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-black  "
                >
                    CALL POLICE
                </button>

            </div>

            
            
            <div className=' bg-black-100 px-4 py-4 md:py-8  mb-20 md:mb-0'>
                <h3 className='font-semibold py-4'>Threat Recordings</h3>
                <div className='grid grid-cols-1 md:grid-cols-3 gap-4'>
                    {data.map((item, key) => (
                        <div key={key} className='grid grid-cols-2 '>
                            <Link href={"/dashboard/notifications/"+item.id} className='flex justify-center items-center'>
                                <img src={PUBLIC_URL+"/"+item.video_name+"/"+item.image_path} />
                                {/* <img className='absolute ' src='/app/images/play_icon.png' /> */}
                            </Link>

                            <div className='px-3.5 pt-2'>
                                <p className='font-semibold text-sm'>{getTimeDelay(item.date_time)} Ago</p>
                                <h5 className='font-semibold text-lg'>{item.video_name}</h5>
                                <h6 className='font-semibold text-sm text-black-600'>{item.duration}</h6>
                            </div>

                        </div>
                    ))}
                </div>
            </div>
            
        </div>
    )
}

export default Notifications