<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Following</h1>
        <br>

        <div>
          <b-nav tabs>
            <b-nav-item>
              <b-link to="/home">Home</b-link>
            </b-nav-item>
            <b-nav-item>
              <b-link to="/follow">Follow Requests</b-link>
            </b-nav-item>
            <b-nav-item>
              <b-link to="/tag">Tag Requests</b-link>
            </b-nav-item>
            <b-nav-item>
              <b-link to="/group">My Groups</b-link>
            </b-nav-item>
            <b-nav-item active>
              <b-link to="/following">Following</b-link>
            </b-nav-item>
          </b-nav>
        </div>
        <br>
        <br>
        <alert :message = "message" v-if = "showMessage"></alert>

        <!-- <button type="button" class="btn btn-success btn-sm">Add Book</button>
        <br>
        <br> -->
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">User</th>
              <th scope="col"></th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(user, index) in followingList" :key="index">
              <td>{{ user.followeeUsername }}</td>
              <td></td>
              <td>
                <b-button type="button" @click="onUnfollow(user.followeeUsername)" variant="warning" size="sm">Unfollow</b-button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert';

export default {
  name: 'Friend',
  data() {
    return {
      followingList: [],
      message: '',
      showMessage: false,
    };
  },
  components: {
    alert: Alert,
  },
  created() {
    this.getFollowingList();
  },
  methods: {
    getFollowingList() {
      const path = 'http://localhost:5000/following';
      let params = {
        username: localStorage.username,
      };
      axios.get(path, {params})
        .then((res) => {
          this.followingList = res.data.followings;
        }).catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    onUnfollow(followeeUsername) {
        let followerUsername = localStorage.username;
        const path = `http://localhost:5000/unfollow/${followerUsername}/${followeeUsername}`;
        console.log("followerUsername: " + followerUsername);
        console.log("followeeUsername: " + followeeUsername);
        axios.delete(path)
        .then((res) => {
            this.message = res.data.message;
            this.showMessage = true;
            this.getFollowingList();
        }).catch((error) => {
            // eslint-disable-next-line
            console.log(error);
        });
    },
  },
};
</script>
