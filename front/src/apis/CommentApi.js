const ip ="http://192.168.31.87:8000"; 

import axios from 'axios'

// 댓글 작성하기
const PostComments = (data, callback, errorCallback) => {
    axios.post(`${ip}/articles/comment/`, data)
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

//새 글 작성하기
const newPost = (form, callback, errorCallback) => {
    

     axios.post(`http://192.168.31.87:8000/articles/`, form,{
        headers: {
            'Content-Type': 'multipart/form-data',
        }
     })
        .then((response) => {
            console.log('글작성 :',response)
            callback(response)
        
        })
        .catch((response) => {
            console.log(response)
            console.log('글작성 오류'  + response)
            errorCallback('error')
        }) 

}


const CommentApi = {
    PostComments: (data, callback, errorCallback) => PostComments(data, callback, errorCallback),
    newPost: (data, callback, errorCallback) => newPost(data, callback, errorCallback),
}
export default CommentApi