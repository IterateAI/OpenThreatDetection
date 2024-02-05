// 'use client'

import AddCameraForm from '@/app/components/addCameraForm';
import axios from 'axios';
import Link from 'next/link'
import React from 'react'


export default async function Camera({params}) {
    
    
    return (
        <div className=''>
            <div className='container px-8 mt-8'>
                <h1 className='text-3xl py-2 font-semibold'>Add Camera</h1>
                <AddCameraForm/>
            </div>
        </div>
    )
}