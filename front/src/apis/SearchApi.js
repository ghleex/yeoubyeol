import axios from 'axios'

const SearchUser = (data, callback, errorCallback) => {
    let searchKeyword = new FormData()
    searchKeyword.append('keyword', data.keyword)

    console.log("여기서보낼거야~!"+searchKeyword);

    axios.post('http://192.168.31.87:8000/articles/search/', searchKeyword)
        .then(res => {
            console.log(res)
            console.log('검색쿠성공')
            callback(res)
        })
        .catch(err => {
            console.log(err)
            errorCallback('search-error')
        })
}


const SearchApi = {
    SearchUser: (data, callback, errorCallback) => SearchUser(data, callback, errorCallback),
}
export default SearchApi