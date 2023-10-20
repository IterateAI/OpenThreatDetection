'use client'
import Link from 'next/link'
import React, { useEffect, useState } from 'react'
import { usePathname } from 'next/navigation'
import { FooterLogo } from './footerlogo'
import { routerBase } from '../config/config'

export const Sidebar = () => {
    const pathname = usePathname()
    const [active,setActive]=useState()
    useEffect(() => {

        let path=pathname.split("/")[2]
        if(path)
        setActive(path)
     
    }, [pathname])
    
    
    return (
        <>
            <div className={`fixed left-0 hidden md:block w-0 md:w-56 h-screen bg-gray-dark`}>
                <div className='relative'>
                    <ul className=' pt-2 '>
                    <li>
                        <Link className={`pl-8 block ${active=="allcamera"?"bg-black-600 ":""}  py-3.5 cursor-pointer text-white  hover:bg-black-600 focus:bg-black-600 active:bg-black`} 
                            href={routerBase+"dashboard/cameras"}>
                            All Cameras
                        </Link>

                    </li>
                    <li >
                        <Link className={`pl-8 block  ${active=="notifications"?"bg-black-600 ":""} py-3.5 cursor-pointer text-white  hover:bg-black-600 focus:bg-black-600 active:bg-black`} 
                            href={routerBase+"dashboard/notifications"}>
                            Notifications
                        </Link>
                    </li>
                    <li >
                        <Link className={`pl-8 block  ${active=="allAlert"?"bg-black-600 ":""} py-3.5 cursor-pointer text-white  hover:bg-black-600 focus:bg-black-600 active:bg-black`} 
                            href={routerBase+"dashboard/allAlert"}>
                            Alert List
                        </Link>
                    </li>

                </ul>
                <div className='fixed bottom-0 ml-8 '>
                <FooterLogo type="dark" />
                </div>
                   
            
                </div>
                
            </div>
            <div className={`w-screen  block md:hidden  `}>
                <ul className=' grid grid-cols-2 '>
                    <li>
                        <Link className={`  ${active=="allcamera"?"border-b-2 border-black bg-white ":"bg-black-300"}  text-center block  py-3.5 cursor-pointer text-black  hover:bg-black-100 focus:bg-black-100 active:bg-white`}
                            href={routerBase+"dashboard/allcamera"}>
                            All Cameras
                        </Link>

                    </li>
                    <li >
                        <Link className={`  ${active=="notifications"?"border-b-2 border-black bg-white ":"bg-black-300"} border-black text-center block  py-3.5 cursor-pointer text-black  hover:bg-black-100 focus:bg-black-100 active:bg-white`}
                            href={routerBase+"dashboard/notifications"}>
                            Notifications
                        </Link>
                    </li>

                </ul>
                
            </div>

           
            
        </>
    )
}
