<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';

const auth = useAuthStore();
const isLogin = ref(true);
const username = ref('');
const email = ref('');
const password = ref('');

const handleSubmit = async () => {
  if (isLogin.value) {
    await auth.login(username.value, password.value);
  } else {
    const success = await auth.register(username.value, email.value, password.value);
    if (success) {
      isLogin.value = true;
      alert('Registration successful! Please login.');
    }
  }
};
</script>

<template>
  <div class="auth-container">
    <h2>{{ isLogin ? 'Login' : 'Register' }}</h2>
    <form @submit.prevent="handleSubmit" class="auth-form">
      <div class="form-group">
        <label>Username</label>
        <input v-model="username" type="text" required />
      </div>
      <div v-if="!isLogin" class="form-group">
        <label>Email</label>
        <input v-model="email" type="email" required />
      </div>
      <div class="form-group">
        <label>Password</label>
        <input v-model="password" type="password" required minlength="8" />
      </div>
      <button type="submit" :disabled="auth.loading">
        {{ auth.loading ? 'Processing...' : (isLogin ? 'Login' : 'Register') }}
      </button>
      <p v-if="auth.error" class="error">{{ auth.error }}</p>
      <p class="toggle-link" @click="isLogin = !isLogin">
        {{ isLogin ? "Don't have an account? Register" : "Already have an account? Login" }}
      </p>
    </form>
  </div>
</template>

<style scoped>
.auth-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background: #f9f9f9;
}
.auth-form {
  display: flex;
  flex-direction: column;
}
.form-group {
  margin-bottom: 15px;
}
.form-group label {
  display: block;
  margin-bottom: 5px;
}
.form-group input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}
button {
  padding: 10px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:disabled {
  background-color: #ccc;
}
.error {
  color: red;
  margin-top: 10px;
}
.toggle-link {
  margin-top: 15px;
  color: #2c3e50;
  cursor: pointer;
  text-decoration: underline;
  text-align: center;
}
</style>
