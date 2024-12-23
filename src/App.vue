<template>
  <div id="app">
    <TeacherDashboard />
  </div>
</template>

<script>
import TeacherDashboard from './components/TeacherDashboard.vue'

export default {
  name: 'App',
  components: {
    TeacherDashboard
  }
}
</script>

<style>

body {
  margin: 0;
  padding: 0;
  background-color: #121212;
}
</style>
