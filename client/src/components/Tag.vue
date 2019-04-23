<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Tag Requests</h1>
        <br>

        <div>
          <b-nav tabs>
            <b-nav-item>
              <b-link to="/home">Home</b-link>
            </b-nav-item>
            <b-nav-item>
              <b-link to="/follow">Follow Requests</b-link>
            </b-nav-item>
            <b-nav-item active>
              <b-link to="/tag">Tag Requests</b-link>
            </b-nav-item>
            <b-nav-item>
              <b-link to="/group">My Groups</b-link>
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
              <th scope="col">Photo Owner</th>
              <th scope="col">Photo ID</th>
              <th scope="col">Accepted?</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(tagRequest, index) in tagRequests" :key="index">
              <td>{{ tagRequest.photoOwner }}</td>
              <td>{{ tagRequest.photoID }}</td>
              <td>{{ tagRequest.acceptedTag ? "Yes" : "No"}}</td>
              <td>
                <button type="button" @click="onAcceptTag(tagRequest.photoID)" class="btn btn-success btn-sm">
                  Accept</button>
                <button type="button" @click="onDeclineTag(tagRequest.photoID)" class="btn btn-danger btn-sm">
                  Decline</button>
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
  name: 'Tag',
  data() {
    return {
      tagRequests: [],
      message: '',
      showMessage: false,
    };
  },
  components: {
    alert: Alert,
  },
  created() {
    this.getTagRequests();
  },
  methods: {
    getTagRequests() {
      const path = 'http://localhost:5000/tag';
      let params = {
        username: localStorage.username,
      };
      axios.get(path, {params})
        .then((res) => {
          this.tagRequests = res.data.Tags;
        }).catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    editTag(payload) {
      const path = 'http://localhost:5000/tag';
      axios.put(path, payload)
        .then((res) => {
          console.log(res.data.message);
          this.message = res.data.message;
          this.showMessage = true;
          this.getTagRequests();
        }).catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    onAcceptTag(photoID) {
      console.log("accept button clicked!");
      const payload = {
        username: localStorage.username,
        photoID: photoID,
        acceptedTag: true,
      };
      this.editTag(payload);
    },
    onDeclineTag(photoID) {
      const path = `http://localhost:5000/tag/${localStorage.username}/${photoID}`;
      axios.delete(path)
        .then((res) => {
          this.message = res.data.message;
          this.showMessage = true;
          this.getTagRequests();
        }).catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        })
    },
  },
};
</script>
