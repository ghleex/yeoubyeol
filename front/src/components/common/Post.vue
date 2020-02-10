<template>
<div>
  <v-card
      class="mx-2"
      color="#110B22"
      dark
      outlined
      style="border: 1px solid #71d087;"
    >
      <v-list-item>
        <v-list-item-avatar color="grey darken-3">
          <v-img
            src=""
          ></v-img>
        </v-list-item-avatar>

        <v-list-item-content>
          <v-list-item-title>Evan You</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-card-text class="subtitle-2 grey--text text--lighten-5 pb-0">
        {{article}}
        <br>
        <v-row class="overline font-weight-thin pr-4" align="center" justify="end">
          2시간 전
        </v-row>
      </v-card-text>
  
      <v-card-actions class="pt-0">
        <v-list-item>
          <v-row
            class="mr-1"
            align="center"
            justify="end"
          >
            <v-icon class="mr-1" size="x-large">mdi-heart-outline</v-icon>
            <span class="subheading mr-2">256</span>
            <v-icon class="mr-1" size="x-large">mdi-star-outline</v-icon>
            <span class="subheading">45</span>
          </v-row>
        </v-list-item>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
    export default {
        name: "Post",
        props:{
            nickName:{
              type:String,
            },
            article:{
              type:String,
            },
            image:{
                type:String,
            },
            picName:{
                type:String,
                default:"no-image",
            },

        },
          data: function () {
            return {
            }
        },
    }
</script>
\