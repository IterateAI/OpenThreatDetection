// 'use client'
import { FooterLogo } from "../components/footerlogo"
import Header from "../components/header"
import { Sidebar } from "../components/sidebar"


export const metadata = {
  title: 'Threat Detect | Dashboard',
  description: 'Weapon Detection Web Application',
}

export default function DashboardLayout({ children }) {
  return (
    <section>
      <Header />
      <div className="md:flex pt-16">
        <div className="flex-none w-0 md:w-56">
          <Sidebar />
        </div>
        <div className="flex-1 ">
          {children}
        </div>
      </div>
    </section>
    
  )
}
