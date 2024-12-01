<template>
  <div id="app">
    <Header />
    <MainSection />
    <Footer />
  </div>
</template>

<script>
import Header from './components/Header.vue'
import MainSection from './components/MainSection.vue'
import Footer from './components/Footer.vue'

export default {
  name: 'App',
  components: {
    Header,
    MainSection,
    Footer
  }
}
</script>

<style>
/* Global styles can go here */
</style>
