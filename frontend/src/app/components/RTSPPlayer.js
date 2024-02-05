'use client'
import React from "react";
import ReactPlayer from "react-player";

const RTSPPlayer=({url})=>{
    const rtspStreamUrl=url
    return(
        <div>
            <ReactPlayer loop={true} url={rtspStreamUrl} playing={true} controls={true} width="100%" height="auto"/>
        </div>
    )
}
export default RTSPPlayer;