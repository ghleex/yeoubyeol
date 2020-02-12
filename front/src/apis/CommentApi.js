import axios from 'axios'
import dotenv from 'dotenv';
dotenv.config();
//  ------------------ 현재 기능
//댓글 작성
//댓글 수정


// 댓글 작성하기
const PostComments = (data, callback, errorCallback) => {
    axios.post(`http://${process.env.VUE_APP_IP}/articles/comment/`, data)
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

// 댓글 수정하기
const EditComments = (data, callback, errorCallback) => {
    axios.put(`http://${process.env.VUE_APP_IP}/articles/comment/`, data)
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

// 댓글 삭제하기
const DeleteComments = (data, callback, errorCallback) => {
    axios.delete(`http://${process.env.VUE_APP_IP}/articles/comment/${data}`)
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




const CommentApi = {
    PostComments: (data, callback, errorCallback) => PostComments(data, callback, errorCallback),
    EditComments: (data, callback, errorCallback) => EditComments(data, callback, errorCallback),
    DeleteComments: (data, callback, errorCallback) => DeleteComments(data, callback, errorCallback),
}
export default CommentApi