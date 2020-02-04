<template>
<div>


<!--  https://vuetifyjs.com/ko/components/cards -->
  <!-- <v-layout row dark color="#110b22" class="py-2"> -->
      <v-card dark color="#110b22" width="100%" style="border:1px solid #110b22;">
        <v-card-title>
             <v-avatar size="55">
          <img v-if="picName!=='default'"
        :src="'../../assets/images/example/'+this.userInfo.picname"
      >
          <img v-else
        src="../../assets/images/profile_default.png"
      >
        </v-avatar>
        <div>

        <h5 class="green--text">hongjuzzang</h5>
        <h6 class="white--text">@홍주네 고양이</h6>
        </div>
        <v-spacer></v-spacer>
        <div><p class="caption">23시간 전</p></div>
        <v-card-text>

        {{content}}
        </v-card-text>

        </v-card-title>
        <v-img v-if="image"
          src="https://cdn.vuetifyjs.com/images/cards/sunshine.jpg"
          height="200px"
        >
        </v-img>

        <v-card-actions>

         
<v-btn text>
           <v-icon left class="red--text" @click=" isLiked = !isLiked">{{isLiked? 'mdi-heart' : 'mdi-heart-outline'}}</v-icon>
    {{likes}}
</v-btn>
<v-btn text>
           <v-icon left class="yellow--text" @click=" isClipped = !isClipped">{{isClipped? 'mdi-star' : 'mdi-star-outline'}}</v-icon>
    {{likes}}
</v-btn>
<v-btn text>
           <v-icon left>mdi-comment</v-icon>
    {{likes}}
</v-btn>
<v-spacer></v-spacer>
          <v-btn icon @click="show = !show">
            <v-icon>{{ show ? 'mdi-chevron-down' : 'mdi-chevron-up' }}</v-icon>
          </v-btn>
        </v-card-actions>

        <v-slide-y-transition>
          <v-card-text v-show="show">
            I'm a thing. But, like most politicians, he promised more than he could deliver. You won't have time for sleeping, soldier, not with all the bed making you'll be doing. Then we'll go with that data file! Hey, you add a one and two zeros to that or we walk! You're going to do his laundry? I've got to find a way to escape.
          </v-card-text>
        </v-slide-y-transition>
      </v-card>
  <!-- </v-layout> -->
  </div>
</template>

<script>
    export default {
        name: "Post",
        // props : ['text', 'image','isLiked','picname'],
        props:{
            content:{
                type:String,
                default:' ',
            },
            image:{
                type:String,
            },
            isLiked:{
                type:Boolean,
                required:true
            },
            picName:{
                type:String,
                default:"default",
                required:false
            },
            isClipped:{
                type:Boolean,
                required:true
            }

        },
          data: function () {
            return {
                show:false,
                likes:213,
            }
        },
    }
</script>
\