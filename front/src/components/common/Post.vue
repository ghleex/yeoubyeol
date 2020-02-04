<template>
<div>
  <v-card
      class="mx-auto"
      color="#110B22"
      dark
      outlined
      max-width="400"
      style="border: 1px solid #71d087;"
    >
      <v-card-text class="subtitle-2 grey--text text--lighten-5 pb-0">
        '뭐해?'라는 두 글자에 <br>
        '네가 보고 싶어' 나의 속마음을 담아 우 <br>
        이모티콘 하나하나 속에 <br>
        달라지는 내 미묘한 심리를 알까 우 <br>
        <br>
        아니 바쁘지 않아 nothing no no <br>
        잠들어 있지 않아 insomnia nia nia <br>
        지금 다른 사람과 함께이지 않아 <br>
        응, 나도 너를 생각 중 <br>
        <br>
        우리의 네모 칸은 bloom <br>
        엄지손가락으로 장미꽃을 피워 <br>
        향기에 취할 것 같아 우 <br>
        오직 둘만의 비밀의 정원 <br>
        <br>
        I feel bloom I feel bloom I feel bloom <br>
        너에게 한 송이를 더 보내 <br>
        <br>
        <v-row class="overline font-weight-thin pr-4" align="center" justify="end">
          2시간 전
        </v-row>
      </v-card-text>
  
      <v-card-actions class="pt-0">
        <v-list-item>
          <v-list-item-avatar color="grey darken-3">
            <v-img
              src="https://avataaars.io/?avatarStyle=Transparent&topType=ShortHairShortCurly&accessoriesType=Prescription02&hairColor=Black&facialHairType=Blank&clotheType=Hoodie&clotheColor=White&eyeType=Default&eyebrowType=DefaultNatural&mouthType=Default&skinColor=Light"
            ></v-img>
          </v-list-item-avatar>
  
          <v-list-item-content>
            <v-list-item-title>Evan You</v-list-item-title>
          </v-list-item-content>
          <v-row
            class="mr-1"
            align="center"
            justify="end"
          >
            <v-icon class="mr-1" size="medium">mdi-heart</v-icon>
            <span class="subheading mr-2">256</span>
            <v-icon class="mr-1" size="medium">mdi-star-outline</v-icon>
            <span class="subheading">45</span>
          </v-row>
        </v-list-item>
      </v-card-actions>
    </v-card>

<!--  https://vuetifyjs.com/ko/components/cards -->
  <!-- <v-layout row dark color="#110b22" class="py-2"> -->
      <v-card dark color="#110b22" width="100%">
        <v-card-title>
          <v-avatar size="55">
            <img v-if="picName!=='default'"
              :src="'../../assets/images/example/'+this.userInfo.picname">
            <img v-else
              src="../../assets/images/profile_default.png">
          </v-avatar>
          
          <div>
            <h5 class="green--text">hongjuzzang</h5>
            <h6 class="white--text">@홍주네 고양이</h6>
          </div>
          
          <v-spacer></v-spacer>
          
          <div>
            <p class="caption">23시간 전</p>
          </div>
          
          <v-card-text>
            Hello
          </v-card-text>

        </v-card-title>
        <v-img v-if="image"
          src="https://cdn.vuetifyjs.com/images/cards/sunshine.jpg"
          height="200px"
        >
        </v-img>

        <!-- <v-card-actions>
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
        </v-card-actions> -->

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
            // content:{
            //     type:String,
            //     default:' ',
            // },
            image:{
                type:String,
            },
            // isLiked:{
            //     type:Boolean,
            //     required:true
            // },
            picName:{
                type:String,
                default:"default",
                required:false
            },
            // isClipped:{
            //     type:Boolean,
            //     required:true
            // }

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