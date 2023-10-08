'use client'
export function getTimeDelay(DateTime){

const time = DateTime.split(' ')[1]; 
const date = DateTime.split(' ')[0]; 
console.log(`${date}`)
const y = date.split('-')[2]; 
const m = date.split('-')[1]; 
const d = date.split('-')[0]; 
const newData=y+'-'+m+'-'+d




const currentDate = new Date();
const currentTime = currentDate.toJSON();
console.log(`${newData}T${time}.000Z`)
console.log("current date",currentTime)

// Convert time strings to Date objects
const date1 = new Date(`${y}-${m}-${d}T${time}.000Z`);
const date2 = new Date(`${currentTime}`);

// Calculate the time difference in milliseconds
console.log("date1",date1)
console.log("date2",date2)

const timeDifferenceInMilliseconds = date2 - date1;

// Calculate the time difference in seconds
const timeDifferenceInSeconds = Math.abs(timeDifferenceInMilliseconds) / 1000;
console.log("Time difference",timeDifferenceInSeconds);
const hours = Math.floor(timeDifferenceInSeconds / 3600);
const minutes = Math.floor((timeDifferenceInSeconds % 3600) / 60);
const remainingSeconds = Math.round(timeDifferenceInSeconds % 60);
return `${hours}:${minutes}:${remainingSeconds}`
}