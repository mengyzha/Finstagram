<template>
  <div class="container">
    <h1>{{ username }}: Welcome to Home</h1>
    <br>

    <div>
      <b-nav tabs>
        <b-nav-item active>
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
      </b-nav>
    </div>
    <br><br>
    <alert :message="message" v-if="showMessage"></alert>

    <button type="button" v-b-modal.post-modal class="btn btn-success btn-sm">Post</button>
    <button type="button" v-b-modal.follow-modal class="btn btn-success btn-sm">Follow</button>
    <button type="button" @click="logout" class="btn btn-warning btn-sm">Logout</button>
    <br>
    <br>

    <div class="row">
      <!-- <div class="col-md-4 col-lg4" v-for="(photo, index) in photos" :key="index"> -->
      <b-card-group columns>
        <b-card
          v-for="(photo, index) in photos"
          :key="index"
          :title="photo.photoOwner"
          :img-src="photo.filePath"
          img-alt="Image"
          img-top
          tag="article"
          style="max-width: 20rem;"
          class="mb-2"
        >
          <b-card-text>{{photo.caption}}</b-card-text>
          <br>
          <b-card-text
            class="small text-muted"
          >{{photo.photoID}} posted at {{photo.timestamp}}</b-card-text>
          <br><br>
          <button class="btn btn-outline-primary" @click="onClickFollow(photo.photoOwner)">Follow</button>
          <button class="btn btn-outline-primary" @click="onClickTag(photo.photoID)" v-b-modal.tag-modal>Tag</button>
          <!-- <b-link href="#" class="card-link">Follow</b-link>
          <b-link href="#" class="card-link">Tag</b-link>-->
        </b-card>
      </b-card-group>
      <!-- </div> -->
    </div>

    <b-modal ref="postPhotoModal" id="post-modal" title="Post a new photo" hide-footer>
      <b-form @submit="onSubmitPost" @reset="onCancelPost" class="w-100">
        <b-form-group id="form-path-group" label="File Path:" label-for="form-path-input">
          <b-form-input
            id="form-path-input"
            type="text"
            v-model="postPhotoForm.filePath"
            required
            placeholder="Enter a file path"
          ></b-form-input>
        </b-form-group>
        <b-form-group id="form-caption-group" label="Caption:" label-for="form-caption-input">
          <b-form-input
            id="form-caption-input"
            type="text"
            v-model="postPhotoForm.caption"
            placeholder="Enter caption"
          ></b-form-input>
        </b-form-group>
        <b-form-group id="form-followers-group">
          <b-form-checkbox-group v-model="postPhotoForm.allFollowers" id="form-checks">
            <b-form-checkbox value="true">All Followers?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-form-group>
          <b-form-select v-model="selected" :options="options"></b-form-select>
        </b-form-group>

        <b-button type="submit" variant="primary">Post</b-button>
        <b-button type="reset" variant="danger">Cancel</b-button>
      </b-form>
    </b-modal>

    <b-modal ref="followUserModal" id="follow-modal" title="Follow a new user" hide-footer>
      <b-form @submit="onSubmitFollow" @reset="onCancelFollow" class="w-100">
        <b-form-group id="follow-form-user-group" label="User:" label-for="follow-form-user-input">
          <b-form-input
            id="follow-form-user-input"
            type="text"
            v-model="followUserForm.username"
            required
            placeholder="Enter the username"
          ></b-form-input>
        </b-form-group>
        <b-button type="submit" variant="primary">Follow</b-button>
        <b-button type="reset" variant="danger">Cancel</b-button>
      </b-form>
    </b-modal>

    <b-modal ref="tagUserModal" id="tag-modal" title="Tag a new user" hide-footer>
      <b-form @submit="onSubmitTag" @reset="onCancelTag" class="w-100">
        <b-form-group id="tag-form-user-group" label="User:" label-for="tag-form-user-input">
          <b-form-input
            id="tag-form-user-input"
            type="text"
            v-model="tagUserForm.username"
            required
            placeholder="Enter the username"
          ></b-form-input>
        </b-form-group>
        <b-button type="submit" @click="tag" variant="primary">Tag</b-button>
        <b-button type="reset" variant="danger">Cancel</b-button>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert';
import router from '../router';

export default {
  name: 'Home',
  data() {
    return {
      username: '',
      message: '',
      showMessage: false,
      photos: [],
      postPhotoForm: {
        filePath: '',
        caption: '',
        allFollowers: [],
      },
      followUserForm: {
        username: '',
      },
      tagUserForm: {
        username: '',
      },
      tagPhotoID: '',
      selected: null,
      options: [
        { value: null, text: 'Please select some item' },
      ],
    };
  },
  components: {
    alert: Alert,
  },
  created() {
    if (localStorage.username) {
      this.username = localStorage.username;
    } else {
      this.username = 'Home Page';
    }

    this.getPhotos();
    // this.getGroups();
  },
  methods: {
    getPhotos() {
      const path = 'http://localhost:5000';
      let params = {
        username: localStorage.username,
      };
      axios.get(path, {params})
        .then((res) => {
          // eslint-disable-next-line
          if (res.data.errno == 403) {
            this.message = res.data.errmsg;
            this.showMessage = true;
            router.push({ name: 'Login' });
            return;
          }
          // eslint-disable-next-line
          console.log(res.data.status);
          this.photos = res.data.photos;
        }).catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getGroups() {
      const path = 'http://localhost:5000/group';
      let params = {
        username: localStorage.username,
      };
      axios.get(path, {params})
        .then((res) => {
          console.log(res.data.message);
          console.log(res.data.groups);
          this.constructOptions(res.data.groups);
        }).catch((error) => {
          // eslint-disable-next-line
          console.log(res.data.status);
        });
    },
    constructOptions(groups) {
      for (i = 0; i < groups.length; ++i) {
        this.options.push({value: groups[i].groupName, text: groups[i].groupName});
        console.log(groups[i].groupName + " " + groups[i].groupName);
      }
    },
    addPhoto(payload) {
      const path = 'http://localhost:5000';
      axios.post(path, payload)
        .then((res) => {
          this.getPhotos();
          this.message = res.data.message;
          this.showMessage = true;
        }).catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getPhotos();
        });
    },
    logout() {
      const path = 'http://localhost:5000/logout';
      axios.put(path)
        .then((res) => {
          if (res.data.errno === 0) {
            localStorage.removeItem('username');
            router.push({ name: 'Login' });
          }
        }).catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    requestFollow(payload) {
      const path = 'http://localhost:5000/follow';
      axios.post(path, payload)
        .then((res) => {
          this.message = res.data.message;
          this.showMessage = true;
        }).catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    tag() {
      const payload = {
        username: this.tagUserForm.username,
        photoID: this.tagPhotoID,
      };
      const path = 'http://localhost:5000/tag';
      axios.post(path, payload)
        .then((res) => {
          this.message = res.data.message;
          this.showMessage = true;
        }).catch((error) => {
          // eslint-disable-next-line

          console.log(error);
        });
    },
    onClickFollow(username) {
      const params = {
        followerUsername: localStorage.username,
        followeeUsername: username,
      };
      this.requestFollow(params);
    },
    onClickTag(photoID) {
      console.log("Tag button clicked!");
      console.log("Photo ID: " + photoID);
      this.tagPhotoID = photoID;
    },
    onSubmitPost(evt) {
      evt.preventDefault();
      this.$refs.postPhotoModal.hide();
      let allFollowers = false;
      if (this.postPhotoForm.allFollowers[0]) allFollowers = true;
      const payload = {
        username: localStorage.username,
        filePath: this.postPhotoForm.filePath,
        caption: this.postPhotoForm.caption,
        allFollowers,
      };
      this.addPhoto(payload);
      this.initForm();
    },
    onCancelPost(evt) {
      evt.preventDefault();
      this.$refs.postPhotoModal.hide();
      this.initForm();
    },
    initForm() {
      this.postPhotoForm.filePath = '';
      this.postPhotoForm.caption = '';
      this.postPhotoForm.allFollowers = [];
      this.followUserForm.username = '';
      this.tagUserForm.username = '';
    },
    onSubmitFollow(evt) {
      evt.preventDefault();
      this.$refs.followUserModal.hide();
      const payload = {
        followerUsername: localStorage.username,
        followeeUsername: this.followUserForm.username,
      };
      this.requestFollow(payload);
      this.initForm();
    },
    onCancelFollow(evt) {
      evt.preventDefault();
      this.$refs.followUserModal.hide();
      this.initForm();
    },
    onSubmitTag(evt) {
      evt.preventDefault();
      this.$refs.tagUserModal.hide();
      this.initForm();

      // check
      // 1. self tag -> ok -> add (self, photID, true)
      // 2. tag y (visible to y) -> ok -> add (y, photoID, false)
      // 3. tag z (not visible to z) -> cannot tag -> alert
    },
    onCancelTag(evt) {
      evt.preventDefault();
      this.$refs.tagUserModal.hide();
      this.initForm();
    },
  },
};
</script>

