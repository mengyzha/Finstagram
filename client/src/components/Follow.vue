<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Follow Requests</h1>
        <br>

        <div>
          <b-nav tabs>
            <b-nav-item>
              <b-link to="/home">Home</b-link>
            </b-nav-item>
            <b-nav-item active>
              <b-link to="/follow">Follow Requests</b-link>
            </b-nav-item>
            <b-nav-item>
              <b-link to="/tag">Tag Requests</b-link>
            </b-nav-item>
            <b-nav-item>
              <b-link to="/group">My Groups</b-link>
            </b-nav-item>
            <b-nav-item>
              <b-link to="/following">Following</b-link>
            </b-nav-item>
          </b-nav>
        </div>
        <br>
        <br>
        <alert :message = "message" v-if="showMessage"></alert>
        
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Follower</th>
              <th scope="col">Accepted?</th>
              <th scope="col"></th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(follower, index) in followers" :key="index">
              <td>{{ follower.followerUsername }}</td>
              <td>{{ follower.acceptedfollow ? 'Yes' : 'No' }}</td>
              <td></td>
              <td>
                <b-button variant="success" size="sm" v-if="!follower.acceptedfollow" @click="onAcceptFollow(follower.followerUsername)">Accept</b-button>
                <b-button variant="danger" size="sm" v-if="!follower.acceptedfollow" @click="onDeclineFollow(follower.followerUsername)">Decline</b-button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import router from '../router';
import axios from 'axios';
import Alert from './Alert';

export default {
  name: 'Follow',
  data() {
    return {
      followers: [],
      message: '',
      showMessage: false,
    };
  },
  components: {
    alert: Alert,
  },
  created() {
    this.getFollows();
  },
  methods: {
    getFollows() {
      const path = 'http://localhost:5000/follow';
      let params = {
        username: localStorage.username,
      };
      axios.get(path, {params})
        .then((res) => {
          if (res.data.errno == 403) {
            router.push({ name: 'Login' });
          } else {
            this.followers = res.data.follows;
          }
        }).catch((error) => {
          // eslint-disable-next-line
          console.log(res.data.status);
        });
    },
    updateFollow(payload) {
      const path = 'http://localhost:5000/follow';
      axios.put(path, payload)
        .then((res) => {
          this.message = res.data.message;
          this.showMessage = true;
          this.getFollows();
        }).catch((error) => {
          // eslint-disable-next-line
          console.log(res.data.status);
        })
    },
    deleteFollow(followerUsername, followeeUsername) {
      const path = `http://localhost:5000/unfollow/${followerUsername}/${followeeUsername}`
      // must use `` to close path, unlike '' in other places
      console.log("followerUsername: " + followerUsername);
      console.log("followeeUsername: " + followeeUsername);
      axios.delete(path)
      .then((res) => {
          this.message = res.data.message;
          this.showMessage = true;
          this.getFollows();
        }).catch((error) => {
          // eslint-disable-next-line
          console.log(res.data.status);
        });
    },
    onAcceptFollow(followerUsername) {
      const payload = {
        followerUsername: followerUsername,
        followeeUsername: localStorage.username,
        acceptedfollow: true,
      };
      this.updateFollow(payload);
    },
    onDeclineFollow(followerUsername) {
      this.deleteFollow(followerUsername, localStorage.username);
    },
  },
};
</script>
