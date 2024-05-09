'use client'
import { useEffect, useState } from 'react';
import { InputField } from './InputFiled';
import { API_URL, routerBase } from '../config/config';
import axios from 'axios';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

function EditCameraForm({camId}) {
  const router=useRouter()
  const [formData, setFormData] = useState({
    video_type: '',
    link: '',
    name: '',
    location:'',
    address:'',
    frame_skip_size:100,
    lat:'',
    long:''
  });
  const [updateformData, setupdateFormData] = useState({
  });
  const link_types = ['mp4', 'rtsp', 'HLS'];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
    setupdateFormData({
      ...updateformData,
      [name]:value
    })
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log(updateformData)
    try {
      const response = await axios.put(API_URL+'/camera/cameras/update/'+camId, 
      JSON.stringify({"updated_fields":updateformData}),
      {
        headers: {
          'Content-Type': 'application/json',
        }
      }
      );

      if (response.status === 200) {
        
        console.log('Form submitted successfully');
        router.push('/dashboard/cameras/'+camId)
      } else {
        console.error('Form submission failed');
      }
    } catch (error) {
      console.error('Form submission error:', error);
    }
  };
  useEffect(()=>{
    axios.get(API_URL + '/camera/cameras/' + camId) // Replace with your API endpoint
    .then((response) => {
        console.log(response.data)
        const resData=response.data
        // const updateData=state
        // updateData.selectedCamera=resData
        setFormData(resData)
        // setState(updateData)
    })
    .catch((error) => {
        console.error('Error fetching data:', error);
    });
  },[])
  console.log(formData)

  return (
    <div className='max-w-xl'>
      <form onSubmit={handleSubmit}>
        <div className='py-4'>
          <label htmlFor="video_type" className="block text-sm font-semibold leading-6 text-black-600">Stream Type:</label>
          <select
            className="block w-full rounded-md border-0 px-3.5 py-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"

            id="video_type"
            name="video_type"
            value={formData.video_type}
            onChange={handleChange}
          >
            {/* <option value="">Select Stream Type</option> */}
            {link_types.map((type) => (
              <option key={type} value={type}>
                {type}
              </option>
            ))}
          </select>
        </div>
        <div className='py-4'>
          <InputField
            label={"Video URL"}
            type={"text"}
            id={"video_link"}
            name={"video_link"}
            value={formData.video_link}
            onchange={handleChange}
          />
          <InputField
            label={"Name"}
            type={"text"}
            id={"name"}
            name={"name"}
            value={formData.name}
            onchange={handleChange}
          />
           <InputField
            label={"Location"}
            type={"text"}
            id={"location"}
            name={"location"}
            value={formData.location}
            onchange={handleChange}
          />
          <InputField
            label={"Address"}
            type={"text"}
            id={"address"}
            name={"address"}
            value={formData.address}
            onchange={handleChange}
          />
          <div className='flex flex-warp py-4 gap-4 '>
          <InputField
            label={"Latitude"}
            type={"text"}
            id={"lat"}
            name={"lat"}
            value={formData.lat}
            onchange={handleChange}
          />
          <InputField
            label={"Longitude"}
            type={"text"}
            id={"long"}
            name={"long"}
            value={formData.long}
            onchange={handleChange}
          />
          </div>
          
        </div>
        <div className='py-4 flex  gap-4'>
          <button
            type="submit"
            className="flex w-full justify-center rounded-md bg-black px-3 py-3.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-black-600  "
          >
            UPDATE CAMERA
          </button>
          <Link
            href={"/app/dashboard/cameras"}
            className="flex w-full justify-center rounded-md bg-white px-3 py-3.5 text-sm font-semibold  border-2 leading-6 text-black shadow-sm hover:bg-black-600  "
          >
            CANCEL
          </Link>
        </div>

      </form>
    </div>
  );
}

export default EditCameraForm;
