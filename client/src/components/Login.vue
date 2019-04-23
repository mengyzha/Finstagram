<template>
  <div class="container">
    <b-jumbotron>
      <template slot="header">Finstagram</template>

      <template slot="lead">
        This is a simple hero unit, a simple jumbotron-style component for calling extra attention to
        featured content or information.
      </template>

      <hr class="my-4">

      <p>
        It uses utility classes for typography and spacing to space content out within the larger
        container.
      </p>

      <b-button variant="primary" v-b-modal.login-modal href="#">Login</b-button>
      <b-button variant="success" v-b-modal.register-modal href="#">Register</b-button>
      <br><br>
      <alert :message="message" v-if="showMessage"></alert>
    </b-jumbotron>

    <b-modal ref="loginModal" id="login-modal" title="Log into your account" hide-footer>
      <b-form @submit="onSubmitLogin" @reset="onCancelLogin" class="w-100">
        <b-form-group id="form-login-user-group" label="Username:" label-for="form-login-user-input">
          <b-form-input
            id="form-login-user-input"
            type="text"
            v-model="loginForm.username"
            required
            placeholder="Enter the username"
          ></b-form-input>
        </b-form-group>
        <b-form-group id="form-login-password-group" label="Password:" label-for="form-login-password-input">
          <b-form-input
            id="form-login-password-input"
            type="password"
            v-model="loginForm.password"
            required
            placeholder="Enter the password"
          ></b-form-input>
        </b-form-group>
    
        <b-button type="submit" variant="primary">Login</b-button>
        <b-button type="reset" variant="danger">Cancel</b-button>
      </b-form>
    </b-modal>

    <b-modal ref="registerModal" id="register-modal" title="Register an account" hide-footer>
      <b-form @submit="onSubmitRegister" @reset="onCancelRegister" class="w-100">
        <b-form-group id="form-register-user-group" label="Username:" label-for="form-register-user-input">
          <b-form-input
            id="form-register-user-input"
            type="text"
            v-model="registerForm.username"
            required
            placeholder="Enter the username"
          ></b-form-input>
        </b-form-group>

        <b-form-group id="form-register-password-group" label="Password:" label-for="form-register-password-input">
          <b-form-input
            id="form-register-password-input"
            type="password"
            v-model="registerForm.password"
            required
            placeholder="Enter the password"
          ></b-form-input>
        </b-form-group>
        
        <b-form-group id="form-register-fname-group" label="Your first name:" label-for="form-register-fname-input">
          <b-form-input
            id="form-register-fname-input"
            type="text"
            v-model="registerForm.fName"
            required
            placeholder="first name"
          ></b-form-input>
        </b-form-group>

        <b-form-group id="form-register-lname-group" label="Your last name:" label-for="form-register-lname-input">
          <b-form-input
            id="form-register-lname-input"
            type="text"
            v-model="registerForm.lName"
            required
            placeholder="last name"
          ></b-form-input>
        </b-form-group>

        <b-form-group id="form-register-avatar-group" label="Your avatar:" label-for="form-register-avatar-input">
          <b-form-input
            id="form-register-avatar-input"
            type="text"
            v-model="registerForm.avatar"
            placeholder="avatar"
          ></b-form-input>
        </b-form-group>

        <b-form-group id="form-register-bio-group" label="Your bio:" label-for="form-register-bio-input">
          <b-form-input
            id="form-register-bio-input"
            type="text"
            v-model="registerForm.bio"
            placeholder="bio"
          ></b-form-input>
        </b-form-group>

        <b-form-group id="form-register-isprivate-group">
          <b-form-checkbox-group v-model="registerForm.isPrivate" id="form-register-checks">
            <b-form-checkbox value="true">Is Private?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>

        <b-button type="submit" variant="primary">Register</b-button>
        <b-button type="reset" variant="danger">Cancel</b-button>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import router from '../router';
import Alert from './Alert';


export default {
  name: 'Login',
  data() {
    return {
      message: '',
      showMessage: false,
      loginForm: {
        username: '',
        password: '',
      },
      registerForm: {
        username: '',
        password: '',
        fName: '',
        lName: '',
        avatar: '',
        bio: '',
        isPrivate: [],
      },
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    registerUser(payload) {
      const path = 'http://localhost:5000/register';
      axios.post(path, payload)
        .then((res) => {
          router.push({name: 'Login'});
        }).catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    loginUser(payload) {
      const path = 'http://localhost:5000/login';
      axios.post(path, payload)
        .then((res) => {
          if (res.data.errno == 0) {
            router.push({name: 'Home'});
          } else {
            this.message = res.data.errmsg;
            this.showMessage = true;
          }
        }).catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    onSubmitLogin(evt) {
      evt.preventDefault();
      this.$refs.loginModal.hide();
      const payload = {
        username: this.loginForm.username,
        password: this.loginForm.password,
      };
      // store the username in the local storage
      localStorage.username = this.loginForm.username;
      this.emptyForm(); // empty before because loginUser could jump to other page 
      this.loginUser(payload);
    },
    onCancelLogin(evt) {
      evt.preventDefault();
      this.$refs.loginModal.hide();
      this.emptyForm();
    },
    emptyForm() {
      this.loginForm.username = '';
      this.loginForm.password = '';

      this.registerForm.fName = '';
      this.registerForm.lName = '';
      this.registerForm.username = '';
      this.registerForm.password = '';
      this.registerForm.avatar = '';
      this.registerForm.bio = '';
      this.registerForm.isPrivate = [];
    },
    onSubmitRegister(evt) {
      evt.preventDefault();
      this.$refs.registerModal.hide();

      let isPrivate = false;
      if (this.registerForm.isPrivate) isPrivate = true;
      const payload = {
        username: this.registerForm.username,
        password: this.registerForm.password,
        fName: this.registerForm.fName,
        lName: this.registerForm.lName,
        avatar: this.registerForm.avatar,
        bio: this.registerForm.bio,
        isPrivate,
      }
      this.registerUser(payload);
      this.emptyForm();
    },
    onCancelRegister(evt) {
      evt.preventDefault();
      this.$refs.registerModal.hide();
      this.emptyForm();
    },
  },
};
</script>