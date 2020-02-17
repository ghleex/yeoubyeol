//follow 친구 맺기 /끊기 
import axios from 'axios'
import dotenv from 'dotenv';

dotenv.config();

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

const requestTrendArticle = (data, callback, errorCallback) => {
    console.log(data);
    axios.get(`${process.env.VUE_APP_IP}/articles/monthlytrend/`)
        .then((response) => {
            console.log(response)
            callback(response)

        })
        .catch((response) => {
            console.log(response)
            console.log('catch ' + response)
            errorCallback('error')
        })
}

const requestTrendHashtags = (data, callback, errorCallback) => {
    
    axios.get(`${process.env.VUE_APP_IP}/articles/hashtagtrend/`)
        .then((response) => {
            console.log(response,"--",data)
            callback(response)

        })
        .catch((response) => {
            console.log(response)
            console.log('catch ' + response)
            errorCallback('error')
        })
}

const requestFeedOfFame = (callback, errorCallback) => {
    axios.get(`${process.env.VUE_APP_IP}/articles/honor/`)
        .then(response => {
            callback(response)
        })
        .catch(error => {
            errorCallback(error)
        })
}



const TrendFameApi = {
    requestTrendArticle: (data, callback, errorCallback) => requestTrendArticle(data, callback, errorCallback),
    requestTrendHashtags: (data, callback, errorCallback) => requestTrendHashtags(data, callback, errorCallback),
    requestFeedOfFame: (data, callback, errorCallback) => requestFeedOfFame(data, callback, errorCallback),
}
export default TrendFameApi