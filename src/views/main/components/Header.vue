<template>
  <header id="header" class="hero-section">
    <div class="container">
      <!-- Logo Section -->
<!--      <div class="logo float-left">-->
<!--        <h1 class="text-light">-->
<!--          <span>Botverse</span>-->
<!--        </h1>-->
<!--      </div>-->

      <!-- Navigation Menu Section -->
      <nav class="nav-menu float-right d-none d-lg-block">
        <ul>
          <li class="main"><a href="/main">Main</a></li>
          <li><a href="/chatbot/session/:sessionId">Chat</a></li>
          <li><a href="/choosebot">Bots</a></li>
          <li><a href="/forum">Forum</a></li>
          <li><a href="/search">Search</a></li>
        </ul>
      </nav>
    </div>

    <!-- Hero Section with Tagline and CTA -->
    <div class="hero-content text-center">
      <h2>Botverse</h2>
      <p>Integrated large model web site</p>
<!--      <a href="#team" class="cta-button">了解更多</a>-->
    </div>
  </header>
</template>

<script>
export default {
  name: 'Header'
}
</script>

<style scoped>
/* Scoped styles for Header component */
.hero-section {
  background: linear-gradient(to right, #af1fc6,#6a11cb, #2575fc);
  padding: 100px 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.logo {
  flex: 1;
  text-align: left;
}

.nav-menu {

  flex: 2;
  text-align: right;
  position: fixed;    /* Fixed at the top */
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;       /* Make sure it's on top of other content */
  padding: 20px 0;
  width: 95%;
}

.nav-menu ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-menu ul li {
  display: inline-block;
  margin: 0 10px;
  padding-right: 10px;
}

.nav-menu ul li a {
  color: white;
  text-decoration: none;
  font-size: 1.2rem;
  word-spacing: .2rem;
}

.hero-content h2,p {
  font-style:italic;
  font-size: 3rem;
  color: white;
  margin-bottom: 20px;
}


.cta-button {
  background-color: #2575fc;
  color: white;
  padding: 10px 20px;
  font-size: 1.2rem;
  text-decoration: none;
  border-radius: 5px;
  margin-top: 20px;
}
</style>
