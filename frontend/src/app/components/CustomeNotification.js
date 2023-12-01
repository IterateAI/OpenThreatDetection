import Link from 'next/link';
import { useState } from 'react';

function CustomeNotification({ message,id, type, onClose,onClick }) {
  return (
    <div
      className={`fixed z-100 top-4 right-4 p-4 bg-red text-white rounded-md shadow-md flex justify-between items-center`}
    >
      <div className='cursor-pointer px-4 py-4' onClick={onClick}>
      <span>{message}</span>
      </div>
      <button
        className="text-lg font-bold hover:text-gray-300 focus:outline-none"
        onClick={onClose}
      >
        &times;
      </button>
    </div>
  );
}

export default CustomeNotification;
