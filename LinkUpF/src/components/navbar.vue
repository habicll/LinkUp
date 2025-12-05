<script>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <footer>
    <nav>
      <RouterLink to="/home" class="link">Home</RouterLink>
      <RouterLink to="/status" class="link">Status</RouterLink>
      <RouterLink to="/profil" class="link">Profil</RouterLink>
    </nav>
  </footer>
</template>


<style>
footer {
  display: flex;
  background: linear-gradient( rgb(230, 239, 233) , rgb(45, 130, 183));
  width: 100%;
  height: 20vh;
  position: absolute;
  bottom: 0;
  justify-content: center;
  align-items: center;
}

nav {
  display: flex;
  justify-content: space-around;
  align-items: center;
  width: 60%;
}

.link:link {
  text-decoration: none;
  color: white;
  font-size: 25px;

}

.link:visited{
  text-decoration: none;
  color: white;
  font-size: 25px;
} 
</style>