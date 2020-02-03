<template> <v-card dark color="#110b22">
      <v-card-actions class='px-0'>
      <v-list-item class="grow px-2 py-0">
        <v-list-item-avatar color="grey darken-3">
          <v-img
            class="elevation-6"
            src="https://avataaars.io/?avatarStyle=Transparent&topType=ShortHairShortCurly&accessoriesType=Prescription02&hairColor=Black&facialHairType=Blank&clotheType=Hoodie&clotheColor=White&eyeType=Default&eyebrowType=DefaultNatural&mouthType=Default&skinColor=Light"
          ></v-img>
        </v-list-item-avatar>

        <v-list-item-content>
          <v-list-item-title style="color:#71d087">{{uid}}</v-list-item-title>
        {{setContent}}

        </v-list-item-content>

        <v-row
          align="center"
          justify="end"
        >
         
          <span class="subheading grey--text px-2" >{{time}}</span>
        </v-row>
      </v-list-item>
    </v-card-actions>
              </v-card>
</template>

<script>
    export default {
        // props : ['text', 'image','isLiked','picname'],
        props:{
            uid:{
                type:String,
                default:' ',
            },
            picName:{
                type:String,
                default:'default',
            },
            code:{
                type:String,
                required:true
            },
            time:{
                type:String,
                required:true
            },

        },
          data: function () {
            return {

            }
        },
    computed:{
        setContent: function(){
            if(this.code==='1'){
                return "내 피드에 댓글"
            }else if(this.code==='2'){
                return "내 피드에 좋아요"
            }
            else if(this.code==='3'){
                return "나에게 팔로잉 신청"
            }else if(this.code==='4'){
                return "나의 팔로잉 거절"
            }else if(this.code==='5'){
                return "나의 팔로잉 수락"
            }
            return this.code
        }
    }
    }
</script>
