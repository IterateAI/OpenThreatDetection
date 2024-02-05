'use client'
import React from 'react'

export function InputField({label,type,name,id,autoComplete,value,onchange}) {
   
    return (

        <div className='w-full'>
            <label htmlFor="first-name" className="block text-sm font-semibold leading-6 text-black-600">
                {label}
            </label>
            <div className="mt-2.5">
                <input
                    type={type}
                    name={name}
                    id={id}
                    value={value}
                    onChange={onchange}
                    autoComplete={autoComplete}
                    className="block w-full rounded-md border-0 px-3.5 py-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                />
            </div>
        </div>

    )
}



