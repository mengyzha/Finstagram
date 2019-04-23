<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>My CloseFriendGroups</h1>
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
            <b-nav-item active>
              <b-link to="/group">My Groups</b-link>
            </b-nav-item>
          </b-nav>
        </div>
        <br>
        <alert :message="message" v-if="showMessage"></alert>

        <button type="button" v-b-modal.add-group-modal class="btn btn-success btn-sm">
          Add Group</button>
        <br>
        <br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Group</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(group, index) in groups" :key="index">
              <td>{{ group.groupName }}</td>
              <td>
                <button type="button" v-b-modal.add-modal @click="setGroupName(group.groupName)" class="btn btn-success btn-sm">
                  Add User</button>
                <button
                  type="button"
                  v-b-modal.remove-modal
                  @click="setGroupName(group.groupName)"
                  class="btn btn-warning btn-sm"
                >Remove User</button>
                <button type="button" @click="setGroupName(group.groupName)" class="btn btn-danger btn-sm">Remove Group</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <b-modal ref="addUserModal" id="add-modal" title="Add a new user into group" hide-footer>
      <b-form @submit="onSubmitAdd" @reset="onCancelAdd" class="w-100">
        <b-form-group id="form-add-user-group" label="User:" label-for="form-add-user-input">
          <b-form-input
            id="form-add-user-input"
            type="text"
            v-model="addUserForm.username"
            required
            placeholder="Enter the username"
          ></b-form-input>
        </b-form-group>
        <b-button type="submit" variant="primary">Add</b-button>
        <b-button type="reset" variant="danger">Cancel</b-button>
      </b-form>
    </b-modal>

    <b-modal
      ref="removeUserModal"
      id="remove-modal"
      title="Remove a new user from group"
      hide-footer
    >
      <b-form @submit="onSubmitRemove" @reset="onCancelRemove" class="w-100">
        <b-form-group id="form-remove-user-group" label="User:" label-for="form-remove-user-input">
          <b-form-input
            id="form-remove-user-input"
            type="text"
            v-model="removeUserForm.username"
            required
            placeholder="Enter the username"
          ></b-form-input>
        </b-form-group>
        <b-button type="submit" variant="primary">Remove</b-button>
        <b-button type="reset" variant="danger">Cancel</b-button>
      </b-form>
    </b-modal>

    <b-modal
      ref="addGroupModal"
      id="add-group-modal"
      title="Add a new group"
      hide-footer
    >
      <b-form @submit="onSubmitGroup" @reset="onCancelGroup" class="w-100">
        <b-form-group id="form-add-group-group" label="Group:" label-for="form-add-group-input">
          <b-form-input
            id="form-add-group-input"
            type="text"
            v-model="addGroupForm.name"
            required
            placeholder="Enter a group name"
          ></b-form-input>
        </b-form-group>
        <b-button type="submit" variant="primary">Add</b-button>
        <b-button type="reset" variant="danger">Cancel</b-button>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert';

export default {
  name: 'Group',
  data() {
    return {
      groups: [],
      addUserForm: {
        username: '',
      },
      removeUserForm: {
        username: '',
      },
      addGroupForm: {
        name: '',
      },
      message: '',
      showMessage: false,
      groupName: '',
    };
  },
  components: {
    alert: Alert,
  },
  created() {
    this.getGroups();
  },
  methods: {
    getGroups() {
      const path = 'http://localhost:5000/group';
      let params = {
        username: localStorage.username,
      };
      axios.get(path, {params})
        .then((res) => {
          this.groups = res.data.groups;
        }).catch((error) => {
          // eslint-disable-next-line
          console.log(res.data.status);
        });
    },
    addGroup(payload) {
      const path = 'http://localhost:5000/group';
      axios.post(path, payload)
        .then((res) => {
          this.message = res.data.message;
          this.showMessage = true;
          this.getGroups();
        }).catch((error) => {
          // eslint-disable-next-line
          console.log(res.data.status);
        });
    },
    addUser(params) {
      const path = 'http://localhost:5000/group/add';
      axios.post(path, params)
        .then((res) => {
          this.message = res.data.message;
          this.showMessage = true;
        }).catch((error) => {
          // eslint-disable-next-line
          console.log(res.data.status);
        });
    },
    removeUser(groupName, groupOwner, username) {
      const path = `http://localhost:5000/group/${groupName}/${groupOwner}/${username}`;
      axios.delete(path)
        .then((res) => {
          this.message = res.data.message;
          this.showMessage = true;
        }).catch((error) => {
          // eslint-disable-next-line
          console.log(res.data.status);
        });
    },
    setGroupName(groupName) {
      console.log(groupName);
      this.groupName = groupName;
    },
    onSubmitAdd(evt) {
      evt.preventDefault();
      this.$refs.addUserModal.hide();
      const params = {
        username: this.addUserForm.username,
        groupName: this.groupName,
        groupOwner: localStorage.username,
      };
      this.addUser(params);
      this.initForm();
    },
    onCancelAdd(evt) {
      evt.preventDefault();
      this.$refs.addUserModal.hide();
      this.initForm();
    },
    onSubmitRemove(evt) {
      evt.preventDefault();
      this.$refs.removeUserModal.hide();
      this.removeUser(this.groupName, localStorage.username, this.removeUserForm.username);
      this.initForm();
    },
    onCancelRemove(evt) {
      evt.preventDefault();
      this.$refs.removeUserModal.hide();
      this.initForm();
    },
    onSubmitGroup(evt) { // add a group
      evt.preventDefault();
      this.$refs.addGroupModal.hide();
      const payload = {
        groupName: this.addGroupForm.name,
        username: localStorage.username,
      };
      console.log("GroupName: " + this.addGroupForm.name + " User: " + localStorage.username);
      this.addGroup(payload);
      this.initForm();
    },
    onCancelGroup(evt) {
      evt.preventDefault();
      this.$refs.addGroupModal.hide();
      this.initForm();
    },
    initForm() {
      this.addUserForm.username = '';
      this.removeUserForm.username = '';
      this.addGroupForm.name = '';
    },
  },
};
</script>
