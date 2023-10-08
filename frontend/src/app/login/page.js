import { FooterLogo } from "../components/footerlogo";
import LoginForm from "../components/loginform";

export default function Login() {
  
  return (
    <div>
      
      <div className="flex justify-center pt-24 ">
        <div className='container mx-auto'>
          <div className="py-8">
            <img className="h-36 w-auto mx-auto" src="../images/threat_logo.png" alt="" />
          </div>
          <LoginForm/>
        </div>
      </div>
      <FooterLogo type={"light"}/>
    </div>
  )
}