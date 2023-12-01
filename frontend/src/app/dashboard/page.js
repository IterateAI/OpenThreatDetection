"use client"
import React from 'react'
import Image from 'next/image'
import { Fragment, useState, useEffect } from 'react'
import { Dialog, Disclosure, Popover, Transition } from '@headlessui/react'
import {
  Bars3Icon,
  XMarkIcon,
} from '@heroicons/react/24/outline'
import { redirect, useRouter } from 'next/navigation'
import { FooterLogo } from '../components/footerlogo'

import Link from 'next/link'
import { routerBase } from '../config/config'

export default function Dashboard() {
  const { router } = useRouter()
  return (
    <div className='container px-12 py-12'>
      <div className='flex flex-col justify-center items-center'>
        <img src={"/images/threat_logo.png"} />
        <Link href={"/dashboard/cameras"}
          type="submit"
          className="flex w-48 mt-8  justify-center rounded-md bg-black px-3 py-3.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-black-600  "
        >
          Start Here
        </Link>
        <FooterLogo type={"light"} />
      </div>
    </div>
  )
}
