<script setup>
import Swipe from '@/components/swipe.vue'
import navbar from '@/components/navbar.vue';
import Logo from '@/components/logo.vue';
import Status from '@/components/status.vue';
</script>


<template>
  <div>
    <Logo />
    <Status />
    <navbar />
  </div>
</template>

<style scope>
template {
  background-color: rgb(230, 239, 233);
}
</style>
