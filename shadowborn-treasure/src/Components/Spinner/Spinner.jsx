import React from 'react';
import Loader from "react-loader-spinner";
import "react-loader-spinner/dist/loader/css/react-spinner-loader.css"
import "../../styles/loader.scss"

const LoadingSpinner = () => (
    <div className='loader-div'>
        <Loader type="MutatingDots" height={100} width={100} color='red' />
        <h6 className='loading-message'>Traveling...</h6>
    </div>
)

export default LoadingSpinner;