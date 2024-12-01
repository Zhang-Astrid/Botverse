<template>
  <footer id="footer">
    <div class="container">
      <div class="copyright">
        &copy; Copyright <strong><span>Botverse Team</span></strong>. All Rights Reserved
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer'
}
</script>

<style scoped>
/* Scoped styles for Footer */
#footer {
  background-color: #ffffff;
  color: #4c5caf;
  padding: 20px 0;
  bottom: 0;
}

#footer .container {
  display: flex;
  justify-content: center;
  align-items: center;
}

#footer .copyright {
  text-align: center;
}
</style>
