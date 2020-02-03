import axios from 'axios'

export default {
    onSignIn(googleUser) {
        var profile = googleUser.getBasicProfile();
        console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
        console.log('Name: ' + profile.getName());
        console.log('Image URL: ' + profile.getImageUrl());
        console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.
        
        var form = new FormData();
        form.append('username', profile.getEmail())
        axios.post('http://192.168.31.89:8000/accounts/email/', form)
        .then(response => {
            console.log(response)
        })
    },
    
    signOut() {
        var auth2 = gapi.auth2.getAuthInstance();
        auth2.signOut().then(function () {
            console.log('User signed out.');
        });
    }
}