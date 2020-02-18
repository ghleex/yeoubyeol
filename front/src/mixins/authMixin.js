import VueAxios from 'vue-axios'
import axios from 'axios';
import Vue from 'vue'

export const authMixin = {
    methods: {
        checkToken: function(provider, redirect){
            axios.post("http://192.168.31.87:8000/api/check/", {"token": localStorage.getItem("vue-authenticate.vueauth_token")})
            .then((response) => {
                    let path = (response.data.status)? true : "/";
                    redirect({ path: path});
                }).catch((error) => {
            });
        },
        authenticate: function(provider) {
            this.$auth.authenticate(provider, {provider: "google-oauth2"})
            .then(function (response) {
                window.location = "/dashboard";
            }).catch(error => {
                console.log(error);
            });
        }
    }
}