// 'use client'

import AddCameraForm from '@/app/components/addCameraForm';
import EditCameraForm from '@/app/components/editCameraForm';
import axios from 'axios';
import Link from 'next/link'
import React from 'react'


export default async function Camera({params}) {
    const {id}=params
    
    
    return (
        <div className=''>
            <div className='container px-8 mt-8'>
                <EditCameraForm camId={id}/>
            </div>
        </div>
    )
}