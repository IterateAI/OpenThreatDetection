import React from 'react'

export const FooterLogo = ({type}) => {

    if (type == "light")
        return (
            <div className='relative min-w-full bottom-0 '>
                <div className=' py-8 flex justify-center'>
                    <div>
                        <span className='font-semibold text-xs  block'>Open Source Provided By</span>
                        <img className='h-14 mt-2' src='/app/images/iterate_logo.png' />
                    </div>

                </div>
            </div>
        )
    else
        return (
            <div className='relative min-w-full bottom-0 '>
                <div className=' py-8 flex justify-center'>
                    <div>
                        <span className='text-xs text-white   block'>Open Source Provided By</span>
                        <img className='h-14 mt-2' src='/app/images/logo_dark.png' />
                    </div>

                </div>
            </div>
        )
}
