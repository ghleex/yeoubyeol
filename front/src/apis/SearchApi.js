import axios from 'axios'
import dotenv from 'dotenv';

dotenv.config();

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

const SearchUser = (data, callback, errorCallback) => {
    let searchKeyword = new FormData()
    searchKeyword.append('keyword', data.keyword)

    axios.post(`${process.env.VUE_APP_IP}/articles/search/`, searchKeyword)
        .then(res => {
            callback(res)
        })
        .catch(err => {
            errorCallback('search-error')
        })
}
const SearchKeyword = (data, callback, errorCallback) => {
    let searchKeyword = new FormData()
    searchKeyword.append('keyword', data.keyword)

    axios.post(`${process.env.VUE_APP_IP}/articles/keyword/`, searchKeyword)
        .then(res => {
            callback(res)
        })
        .catch(err => {
            errorCallback('search-error(keyword)')
        })
}


const SearchApi = {
    SearchUser: (data, callback, errorCallback) => SearchUser(data, callback, errorCallback),
    SearchKeyword: (data, callback, errorCallback) => SearchKeyword(data, callback, errorCallback),
}
export default SearchApi