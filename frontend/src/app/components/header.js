'use client'
import React, { useEffect, useState } from 'react'
import { VideoCameraIcon } from '@heroicons/react/24/outline'
import Image from 'next/image'
import { io } from "socket.io-client";
import CustomeNotification from './CustomeNotification';
import { useGlobalContext } from '../context/store';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { routerBase } from '../config/config';

const socket = io("http://localhost:5001");

const Header = () => {
    const router=useRouter()
    const {alerts,setAlerts}=useGlobalContext();
    const [components, setComponents] = useState([]);
    const handleClick=()=>{
        router.push(routerBase+"dashboard/notifications")
    }

    const handleAddDynamicComponent = (data) => {
        console.log(data)
        // localStorage.setItem("thread",JSON.stringify(data))
        const newComponent = <CustomeNotification onClick={handleClick} onClose={handleRemoveDynamicComponent} message={data.video_name+":"+data.status} id={data._id} type={"alert"}/>;
        setComponents((prevComponents) => [...prevComponents, newComponent]);
    };

    const handleRemoveDynamicComponent = (componentKey) => {
        setComponents((prevComponents) =>
            prevComponents.filter((component) => component.key !== componentKey)
        );
    };

    useEffect(() => {
        const timer = setInterval(() => {
          if (components.length > 0) {
            
            handleRemoveDynamicComponent(components[0].key);
          }
        }, 50000); 
    
        return () => clearInterval(timer);
      }, [components]);


    useEffect(() => {
        
        socket.on('connect', function () {
            console.log('connected 5');
        }
        );
        socket.on('msg', (data) => {
            console.log(data)
            const updateData=JSON.parse(data)
            setAlerts(updateData)
            
            handleAddDynamicComponent(JSON.parse(data))
            // setNotification(JSON.parse(data));
        });

        return () => {

            // setThreatState(false)
            socket.disconnect();
        };
    }, []);

    return (
        <div className='fixed  top-0 w-screen'>
            <header className="bg-black">
                <nav className="mx-auto flex max-w-7xl items-center justify-between p-6 lg:px-8" aria-label="Global">
                    <div className="flex lg:flex-1">
                        <Link href={routerBase+"dashboard"} className="-m-1.5 p-1.5">
                            <span className="sr-only">Threat Detect</span>
                            <img className="h-4 w-auto" src={routerBase+"images/header_logo.png"} alt="Threat Detect" />
                        </Link>
                    </div>
                    <div className="lg:flex lg:flex-1 lg:justify-end">
                        <Link href={routerBase+"dashboard/cameras/add"} className="text-sm font-semibold leading-6 text-gray-900">
                            <img className='px-4  ' src={routerBase+'images/videoadd.png'} />
                        </Link>
                    </div>

                </nav>
            </header>

      <div>
        {components.map((component) => (
          <div key={component.key}>
            {component}
            
          </div>
        ))}
      </div>
        </div>
    )
}

export default Header