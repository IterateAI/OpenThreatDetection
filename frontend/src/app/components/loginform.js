'use client'
import React from 'react'
import { useState } from 'react'
import {useRouter} from 'next/navigation'
import {
  EyeIcon,
  EyeSlashIcon
} from '@heroicons/react/24/outline'
import { routerBase } from '../config/config'

function LoginForm() {
  const router = useRouter()
  const [passVisible, setPassVisible] = useState(false)
    const onSubmit=(e)=>{
        e.preventDefault()
        localStorage.setItem("token","myname")
        router.push(routerBase+"dashboard")
      }
  return (
    <div>
        <form  onSubmit={onSubmit} className="mx-auto max-w-md">
            <div className="grid grid-cols-1 gap-x-8 gap-y-6 px-8 md:px-2">
              <div>
                <label htmlFor="first-name" className="block text-sm font-semibold leading-6 text-black-600">
                  Email Address
                </label>
                <div className="mt-2.5">
                  <input
                    type="text"
                    name="email"
                    id="email"
                    autoComplete="given-name"
                    className="block w-full rounded-md border-0 px-3.5 py-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                  />
                </div>
              </div>
              <div>
                <label htmlFor="first-name" className="block text-sm font-semibold leading-6 text-black-600">
                  Password
                </label>
                <div className="relative mt-2.5">
                  <div className="cursor-pointer absolute inset-y-0 right-0 flex items-center pr-3" onClick={() => setPassVisible(!passVisible)}>
                    {passVisible ? <EyeIcon color='gray' className="h-6 w-6" /> :
                      <EyeSlashIcon color='gray' className="h-6 w-6" />}
                  </div>
                  <input
                    type="password"
                    name="password"
                    id="password"
                    autoComplete="given-name"
                    className="block w-full rounded-md border-0 px-3.5 py-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                  />
                </div>
              </div>
              <div>
              <button
                type="submit"
                className="flex w-full justify-center rounded-md bg-black px-3 py-3.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-black-600  "
              >
                LOG IN
              </button>
            </div>
            </div>
            <div className='cursor-pointer hover:text-black-600 text-center mt-8' onClick={()=>router.replace("/forgot")}>Forgot password?</div>
          </form>
    </div>
  )
}

export default LoginForm