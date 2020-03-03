<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/>
    <Test :notes="notes"> {{notes}} </Test>
    <Api/>
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import Test from "./components/Test";
import Api from "./Api";
export default {
  name: 'App',
  components: {
    HelloWorld,
    Test,
    Api
  },
    data: function () {
      //let headers = {'Content-Type':'application/json'}
        let mode = 'no-cors'
      return {
          notes:fetch('http://localhost:8002/notes/7',{mode:mode})
    }
    }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
