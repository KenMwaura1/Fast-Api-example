<template>
    <div>
        <h3> Fast Api Test </h3>

        {{ notes }}
    </div>
</template>

<script>
    export default {
        name: "Test",
        props: {
            notes: [],
  },
    }
</script>

<style scoped>
h3 {
  margin: 40px 0 0;
}
a {
  color: #42b983;
}
</style>

