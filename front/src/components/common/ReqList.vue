<template>
  <v-card dark color="#110b22" outlined
  >
      <v-list-item class="grow px-2 py-0">
        <v-list-item-avatar color="grey darken-3">
          <v-img
            class="elevation-6"
            src="https://avataaars.io/?avatarStyle=Transparent&topType=ShortHairShortCurly&accessoriesType=Prescription02&hairColor=Black&facialHairType=Blank&clotheType=Hoodie&clotheColor=White&eyeType=Default&eyebrowType=DefaultNatural&mouthType=Default&skinColor=Light"
          ></v-img>
        </v-list-item-avatar>

        <v-list-item-content>
          <v-list-item-title ><b style="color:#71d087">{{uid}}&nbsp; </b> &nbsp;님의 팔로우 요청</v-list-item-title>
          <span style="color:#bbbbbb">
            {{time}}
            </span>
        </v-list-item-content>

        <!-- <v-row align="center" justify="end">
          <span class="subheading grey--text px-2">{{time}}</span>
        </v-row> -->
      </v-list-item>
    <v-card-actions class="px-0 py-0">
      <v-list-item>
        <v-spacer></v-spacer>
        <v-btn outlined min-width=120 style="color:#eeeeee">거절</v-btn>
        <v-spacer></v-spacer>
        <v-btn outlined min-width=120 color="#71d087">승인</v-btn>
        <v-spacer></v-spacer>
      </v-list-item>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: "NotiList",
  // props : ['text', 'image','isLiked','picname'],
  props: {
    uid: {
      type: String,
      default: " "
    },
    picName: {
      type: String,
      default: "default"
    },
    time: {
      type: String,
      required: true
    }
  },
  data: function() {
    return {};
  }
};
</script>
