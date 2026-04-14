<script setup>
import { useAuthStore } from './stores/auth';
import Auth from './components/Auth.vue';
import NoteList from './components/NoteList.vue';

const authStore = useAuthStore();
</script>

<template>
  <div id="app">
    <h1 class="main-title">FastAPI Notes App</h1>
    <main>
      <Auth v-if="!authStore.isAuthenticated" />
      <NoteList v-else />
    </main>
  </div>
</template>

<style>
#app {
  font-family: Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 60px;
}
.main-title {
  text-align: center;
  color: #42b983;
}
body {
  margin: 0;
  padding: 0;
  background-color: #f4f7f6;
}
</style>
