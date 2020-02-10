<template>
  <div>
    <v-card dark color="#110b22" style="border:solid 2px #888">
      <v-form ref="form" v-model="valid" lazy-validation>
        <v-row class="py-0 ma-2">
          <v-col cols="12" class="pa-1">
            <v-btn
              class="mb-2"
              color="#71d087"
              style
              text
              justify="end"
              @click="validate"
              :disabled="!valid"
            >피드 발행하기</v-btn>
          </v-col>
          <v-col cols="12" class="pa-1">
            <div id="preview">
              <img v-if="url" :src="url" style="padding-bottom:5px" />
              <br />
            </div>
            <v-file-input
              accept="image/*"
              prepend-icon="mdi-camera"
              outlined
              dense
              required
              :clearable=false
              label="Image"
              @change="onFileChanged"
            ></v-file-input>
          </v-col>

          <v-col cols="12" class="pa-1">
            <v-textarea
              dark
              :rules="contentRules"
              required
              outlined
              v-model="inputPostContent"
              :autofocus="true"
              :auto-grow="true"
              clearable
            >{{inputPostContent}}</v-textarea>

            <v-btn @click="requestHashTags" text>해시태그 추천받기</v-btn>
            <!-- 여기부터 시작야이             -->
            <v-combobox
              v-model="model"
              :filter="filter"
              :hide-no-data="!search"
              :items="items"
              :search-input.sync="search"
              hide-selected
              label="Search for an option"
              multiple
              small-chips
              solo
            >
              <template v-slot:no-data>
                <v-list-item>
                  <span class="subheading">추가하기</span>
                  <v-chip color="darkgrey" label small>{{ search }}</v-chip>
                </v-list-item>
              </template>
              <template v-slot:selection="{ attrs, item, parent, selected }">
                <v-chip
                  v-if="item === Object(item)"
                  v-bind="attrs"
                  color="darkgrey"
                  :input-value="selected"
                  label
                  small
                >
                  <span class="pr-2">{{ item.text }}</span>
                  <v-icon small @click="parent.selectItem(item)">mdi-close</v-icon>
                </v-chip>
              </template>
              <template v-slot:item="{ index, item }">
                <v-text-field
                  v-if="editing === item"
                  v-model="editing.text"
                  autofocus
                  flat
                  background-color="transparent"
                  hide-details
                  solo
                  @keyup.enter="edit(index, item)"
                ></v-text-field>
                <v-chip v-else color="darkgrey" dark label small>{{ item.text }}</v-chip>
                <v-spacer></v-spacer>
                <v-list-item-action @click.stop>
                  <v-btn icon @click.stop.prevent="edit(index, item)">
                    <v-icon>{{ editing !== item ? 'mdi-pencil' : 'mdi-check' }}</v-icon>
                  </v-btn>
                </v-list-item-action>
              </template>
            </v-combobox>
          </v-col>
        </v-row>
      </v-form>
    </v-card>
  </div>
</template>

<script>
import FeedApi from "@/apis/FeedApi";

export default {
  created() {
    this.loginedNickname = JSON.parse(
      sessionStorage.getItem("LoginUserInfo")
    ).nickname;
  },
  methods: {
    requestHashTags() {
      let form = new FormData();
      form.append("article", this.inputPostContent);
      FeedApi.requestHashTags(
        form,
        res => {
          this.items = [];
          this.items.push({
            header: "아래 중 하나를 입력하거나, 새로 입력해보세요!"
          });
          for (let i = 0; i < res.data.length; i++) {
            console.log("넣을 키워드는 :", res.data[i]);
            this.items.push({
              text: res.data[i]
            });
          }
        },
        error => {
          console.log("error");
        }
      );
    },
    edit(index, item) {
      if (!this.editing) {
        this.editing = item;
        this.index = index;
      } else {
        this.editing = null;
        this.index = -1;
      }
    },
    filter(item, queryText, itemText) {
      if (item.header) return false;

      const hasValue = val => (val != null ? val : "");

      const text = hasValue(itemText);
      const query = hasValue(queryText);

      return (
        text
          .toString()
          .toLowerCase()
          .indexOf(query.toString().toLowerCase()) > -1
      );
    },
    onFileChanged(event) {
        this.selectedFile = event;
        this.url = URL.createObjectURL(this.selectedFile);
    },
    validate() {
      if (this.$refs.form.validate()) {
        // this.snackbar = true;
        this.newPost();
      }
    },
    newPost() {
      console.log(this.hash_check);
      let form = new FormData();
      let tagLists = [];
      for (let i = 0; i < this.model.length; i++) {
        tagLists.push(this.model[i].text);
      }
      console.log(tagLists[0]);
      console.log(tagLists[1]);
      console.log(tagLists[2]);

      form.append("nickname", this.loginedNickname);
      form.append("article", this.inputPostContent);
      form.append("image", this.selectedFile);
      form.append("hashtags", tagLists);
      FeedApi.newPost(
        form,
        res => {
          console.log(res);
          alert("글이 성공적으로 게시되었습니다.");
          window.close();
        },
        error => {
          console.log("error");
          window.close();
        }
      );
    }
  },
  data: () => {
    return {
      activator: null,
      attach: null,
      editing: null,
      url: null,
      index: -1,
      items: [{ header: "아래 중 하나를 입력하거나, 새로 입력해보세요!" }],
      nonce: 1,
      menu: false,
      model: [
        {
          text: "감성"
        }
      ],
      x: 0,
      search: null,
      y: 0,

      loginedNickname: "",
      selectedFile: "",
      inputPostContent: "",
      hash_check: false,
      valid: false,
      contentRules: [v => !!v || "내용을 입력해주세요.."]
    };
  },
  watch: {
    model(val, prev) {
      if (val.length === prev.length) return;

      this.model = val.map(v => {
        if (typeof v === "string") {
          v = {
            text: v
          };

          this.items.push(v);

          this.nonce++;
        }

        return v;
      });
    }
  }
};
</script>
<style scoped>
#preview {
  display: flex;
  justify-content: center;
  align-items: center;
}

#preview img {
  max-width: 50%;
  max-height: 100px;
}
</style>