import Link from 'next/link';
import React, { useState } from 'react';

function DataTable({ data, itemsPerPage }) {
  const [currentPage, setCurrentPage] = useState(1);

  const totalPages = Math.ceil(data.length / itemsPerPage);

  const handlePageChange = (page) => {
    setCurrentPage(page);
  };

  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const currentData = data.slice(startIndex, endIndex);
  console.log(currentData)
  return (
    <div className=" container mx-auto bg-white rounded-lg overflow-hidden">
      <h1 className='text-3xl py-2 font-semibold mb-8'>All Alerts</h1>
      <table className="min-w-full divide-y border-2 border-gray divide-gray">
        <thead>
          <tr>
            <th className="px-6 py-3 bg-gray text-left text-md leading-4 font-bold  uppercase tracking-wider">
              Location
            </th>
            <th className="px-6 py-3 bg-gray text-left text-md leading-4 font-bold uppercase tracking-wider">
              Weapon Status
            </th>
            <th className="px-6 py-3 bg-gray text-left text-md leading-4 font-bold uppercase tracking-wider">
              Date and Time
            </th>
            <th className="px-6 py-3 bg-gray text-left text-md leading-4 font-bold uppercase tracking-wider">
              Image
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {currentData.map((item, index) => (
            <tr key={index} className={index % 2 === 0 ? 'bg-gray-light' : 'bg-white'}>
              <Link href={"/dashboard/notifications/" + item.id}><td className="px-6 py-4 whitespace-no-wrap">{item.video_name}</td></Link>
              <td className="px-6 py-4 whitespace-no-wrap">{item.status}</td>
              <td className="px-6 py-4 whitespace-no-wrap">{item.date_time}</td>
              <Link href={"/dashboard/notifications/" + item.id}><td className="px-6 py-4 whitespace-no-wrap">{item.image_path}</td></Link>

            </tr>
          ))}
        </tbody>
      </table>
      <div className="bg-white max-w-md px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6">
        <button
          onClick={() => handlePageChange(currentPage - 1)}
          disabled={currentPage === 1}
          className={`px-4 py-2 text-sm leading-5 font-medium rounded-md ${currentPage === 1
              ? 'text-gray-400 bg-gray-100 cursor-not-allowed'
              : 'text-indigo-600 bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:bg-indigo-200 active:bg-indigo-300'
            }`}
        >
          <div className='flex items-center gap-2'>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 12h-15m0 0l6.75 6.75M4.5 12l6.75-6.75" />
            </svg>
            Previous
          </div>
        </button>
        <span className="text-sm leading-5 text-gray-700">
          Page {currentPage} of {totalPages}
        </span>
        <button
          onClick={() => handlePageChange(currentPage + 1)}
          disabled={currentPage === totalPages}
          className={`px-4 py-2 text-sm leading-5 font-medium rounded-md ${currentPage === totalPages
              ? 'text-gray-400 bg-gray-100 cursor-not-allowed'
              : 'text-indigo-600 bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:bg-indigo-200 active:bg-indigo-300'
            }`}
        >
          <div className='flex items-center gap-2'>
            Next<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12h15m0 0l-6.75-6.75M19.5 12l-6.75 6.75" />
            </svg>
          </div>
        </button>
      </div>
    </div>
  );
}

export default DataTable;
