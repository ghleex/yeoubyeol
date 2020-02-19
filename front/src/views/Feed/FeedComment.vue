<template>
  <v-responsive fluid>
    <v-row class="pt-0" align="start" justify="center">
      <v-progress-linear
        :active="!isArticleLoaded"
        :indeterminate="!isArticleLoaded"
        absolute
        color="green"
      ></v-progress-linear>

      <!-- 글 원문  -->
      <v-col cols="12" v-if="isArticleLoaded">
        <!-- <div class="pa-2" @click="backward">
          <v-icon class="white--text">mdi-chevron-left</v-icon>
        </div>-->
        <Post v-bind="article" v-on:delPost="delPost" v-on:editPost="editPost" />
      </v-col>
      <!-- 댓글 보여주기 -->
      <v-col cols="12" v-for="comm in comments" :key="comm.comment_id">
        <CommentComment
          v-bind="comm"
          v-on:removeComment="removeComment"
          v-on:editComment="editComment"
        />
      </v-col>
      <!-- 댓글 작성 -->
      <v-col cols="12">
        <v-card class="mx-2" fixed color="#110B22" dark outlined style="border: 1px solid #71d087;">
          <v-form ref="form" v-model="valid" lazy-validation @submit.prevent="validate">
            <v-list-item>
              <v-list-item-avatar color="grey darken-3">
                <v-img :src="loginUserInfo.pic_name"></v-img>
              </v-list-item-avatar>

              <v-list-item-content>
                <v-list-item-title>{{ loginUserInfo.nickname }}</v-list-item-title>
              </v-list-item-content>
              <v-btn
                text
                style="background-color:#71d087;color:#110b22;"
                @click="validate"
                :disabled="!valid"
              >작성</v-btn>
            </v-list-item>
            <v-card-actions class="subtitle-2 grey--text text--lighten-5" align="start">
              <v-text-field
                v-model="loginUserInfo.content"
                counter="200"
                required
                :rules="commentRules"
                label="댓글"
                filled
                rounded
                dense
              ></v-text-field>
            </v-card-actions>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-responsive>
</template>

<script>
import Post from "@/components/common/Post";
import CommentComment from "@/components/common/CommentComment";
import FeedApi from "@/apis/FeedApi";
import CommentApi from "@/apis/CommentApi";
import dotenv from "dotenv";

dotenv.config();
export default {
  components: { Post, CommentComment },
  created() {
    this.getUserInformation();
    this.getArticleById(this.$route.params.id);
  },
  methods: {
    editPost(postId) {
      this.$router.push({ name: "피드 수정", params: { postId: postId } });
    },
    delPost(postId) {
      FeedApi.deletePost(
        postId,
        res => {
          //뒤로 가기
          alert("게시글 삭제가 완료되었습니다.");
          this.$router.push({ name: "메인피드" });
        },
        error => {
          alert("피드 삭제에 오류가 발생했어요 .");
        }
      );
    },

    validate() {
      if (this.$refs.form.validate()) {
        this.PostComments();
      }
    },
    async removeComment(v) {
      await this.removeCommentdone(v);
      this.getArticleById(this.$route.params.id);
    },
    removeCommentdone(v) {
      return new Promise((succ, fail) => {
        CommentApi.DeleteComments(
          v,
          res => {
            succ(res);
          },
          error => {
            alert("댓글 삭제에 오류가 발생했습니다.");
          }
        );
      });
    },
    async secondeditComment(data) {
      let articleID = await this.editCommentdone(data);
      console.log("1 : ", articleID);
      this.getArticleById(articleID);
    },
    editComment(data) {
      this.secondeditComment(data);
    },
    editCommentdone(data) {
      return new Promise((succ, fail) => {
        CommentApi.EditComments(
          data,
          res => {
            succ(res.data.article);
          },
          error => {
            alert("댓글 수정에 오류가 발생했습니다.");
          }
        );
      });
    },
    getUserInformation() {
      let userInfo = this.$cookies.get("LoginUserInfo");
      this.loginUserInfo.nickname = userInfo.nickname;
      this.loginUserInfo.pic_name = `${process.env.VUE_APP_IP}${userInfo.pic_name}`;
    },
    AddComment() {
      if (this.loginUserInfo.content.trim() === "") {
        alert("내용을 입력해주세요.");
      } else {
        this.PostComments();
      }
    },
    PostComments() {
      let form = new FormData();
      form.append("article_id", this.article.id);
      form.append("my_nickname", this.loginUserInfo.nickname);
      form.append("comment", this.loginUserInfo.content);
      CommentApi.PostComments(
        form,
        res => {
          alert("댓글 달기를 성공했어요 ");
          this.loginUserInfo.content = "";
          this.getArticleById(this.article.id);
        },
        error => {
          alert(
            "댓글 달기에 오류가 발생했습니다. 잠시후에 다시 시도해주세요 .."
          );
        }
      );
    },
    getArticleById(id) {
      this.isArticleLoaded = false;
      FeedApi.getArticleById(
        id,
        res => {
          //성공시
          let articleFromServer = {
            nickname: res.data.nickname,
            img: res.data.article.image,
            pic_name: `${process.env.VUE_APP_IP}${res.data.pic_name}`,

            id: res.data.article.id,
            article: res.data.article.article,
            author: res.data.article.author,
            hashtags: res.data.hashtags,
            likes: res.data.article.like_users.length,
            comments: res.data.comments.length,
            created_at: res.data.article.created_at,
            like_users: res.data.article.like_users
          };
          this.article = articleFromServer;
          this.isArticleLoaded = true;
          //comment

          this.comments = [];

          for (let c = 0; c < res.data.comments.length; c++) {
            let comment = {
              nickname: res.data.comments[c][0],
              pic_name: `${process.env.VUE_APP_IP}${res.data.comments[c][1]}`,

              comment_id: res.data.comments[c][2],
              content: res.data.comments[c][3],
              created_at: res.data.comments[c][4]
            };
            this.comments.push(comment);
          }
        },
        error => {
          //실패 시
          this.isArticleLoaded = false;
          alert("댓글과 게시물을 불러오는데 오류가 발생했어요 ..");
          this.$router.push({ path: "/feed" });
        }
      );
    }
  },
  data: () => ({
    isArticleLoaded: false,
    valid: false,
    commentRules: [
      v => v.length < 200 || "조금 더 내용을 줄여보는 건 어떨까요"
    ],
    loginUserInfo: {
      nickname: "ss",
      pic_name: "2",
      content: ""
    },

    article: {
      nickname: "",
      picname: "",
      id: 0,
      article: "",
      hashtags: [],
      likes: 0,
      comment: 0,
      created_at: "",
      like_users: []
    },
    comments: [
      {
        nickname: "",
        pic_name: "",
        content: "",
        created_at: ""
      }
    ]
  })
};
</script>
