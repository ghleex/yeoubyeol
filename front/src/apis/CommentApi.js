import axios from 'axios'
import dotenv from 'dotenv';

dotenv.config();

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

// 댓글 작성하기
const PostComments = (data, callback, errorCallback) => {
    axios.post(`${process.env.VUE_APP_IP}/articles/comment/`, data)
        .then((response) => {
            callback(response)
        
        })
        .catch((response) => {
            errorCallback('error')
        })
}

// 댓글 수정하기
const EditComments = (data, callback, errorCallback) => {
    let id = data.comment_id;
    let form=new FormData();
    form.append("comment",data.comment);

    axios.put(`${process.env.VUE_APP_IP}/articles/comment/${id}/`, form)
        .then((response) => {
            callback(response)
        
        })
        .catch((response) => {
            errorCallback('error')
        })
}

// 댓글 삭제하기
const DeleteComments = (data, callback, errorCallback) => {
    axios.delete(`${process.env.VUE_APP_IP}/articles/comment/${data}`)
        .then((response) => {
            callback(response)
        
        })
        .catch((response) => {
            errorCallback('error')
        })
}




const CommentApi = {
    PostComments: (data, callback, errorCallback) => PostComments(data, callback, errorCallback),
    EditComments: (data, callback, errorCallback) => EditComments(data, callback, errorCallback),
    DeleteComments: (data, callback, errorCallback) => DeleteComments(data, callback, errorCallback),
}
export default CommentApi