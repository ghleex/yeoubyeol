<template>
  <v-card dark color="#110b22">
    <v-card-actions class="px-0">
      <v-list-item class="grow px-2 py-0">
        <v-list-item-avatar color="grey darken-3">
          <v-img
            class="elevation-6"
            src="https://avataaars.io/?avatarStyle=Transparent&topType=ShortHairShortCurly&accessoriesType=Prescription02&hairColor=Black&facialHairType=Blank&clotheType=Hoodie&clotheColor=White&eyeType=Default&eyebrowType=DefaultNatural&mouthType=Default&skinColor=Light"
          ></v-img>
        </v-list-item-avatar>

        <v-list-item-content>
          <v-list-item-title style="color:#71d087">{{email}}</v-list-item-title>
          {{nickName}}
        </v-list-item-content>

        <v-col align="center" justify="end" cols="4">
          <span class="subheading grey--text px-2">
            <v-btn
            v-if = "isFollowing"
             text style="color:#71d087">팔로잉 취소</v-btn>
             <v-btn
             v-else
             text style="color:#71d087">팔로잉

             </v-btn>
          </span>
        </v-col>
      </v-list-item>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  props: {
    email: {
      type: String,
      default: " "
    },
    nickName: {
      type: String,
      default: "default"
    },
    picName: {
      type: String,
      default: "default"
    },
    isFollowing:{
      type:Boolean,
      default:false
    }
  },
  data: function() {
    return {};
  },
};
</script>
