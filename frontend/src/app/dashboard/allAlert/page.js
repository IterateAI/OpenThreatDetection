'use client'
import DataTable  from '@/app/components/DataTable';
import { API_URL } from '@/app/config/config';
import { useGlobalContext } from '@/app/context/store';
import axios from 'axios';
import Link from 'next/link'
import React, { useEffect, useState } from 'react'
import { io } from "socket.io-client";
const socket = io("http://localhost:5001");


const AllAlerts = () => {
    

    const [data, setData] = useState([]);

    useEffect(() => {
        axios.get(API_URL+'/event/events') // Replace with your API endpoint
        .then((response) => {
            console.log(response.data)
            setData(response.data.reverse());
        })
        .catch((error) => {
            console.error('Error fetching data:', error);
        });
    }, []);

    
    return (
        <div className='py-4'>
             
            <DataTable data={data} itemsPerPage={10} />
        </div>
    )
}

export default AllAlerts