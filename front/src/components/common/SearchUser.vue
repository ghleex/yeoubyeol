<template>
 <v-card dark color="#110b22"
 >

      <v-card-actions class='px-0'>
      <v-list-item class="grow px-2 py-0">
        <v-list-item-avatar color="grey darken-3">
          <v-img
            class="elevation-6"
            src="../../assets/images/profile_default.png" />
          </v-list-item-avatar>

        <v-list-item-content>
          <v-list-item-title style="color:#71d087">{{nickname}}</v-list-item-title>
        username

        </v-list-item-content>
      </v-list-item>
    </v-card-actions>
              </v-card>
</template>

<script>
    export default {
        // props : ['text', 'image','isLiked','picname'],
        props:{
            nickname:{
                type:String,
            },
            username:{
                type:String,
            },

        },
          data: function () {
            return {

            }
        },
        methods:{
        }
    }
</script>
