<script setup>
import NavAdmin from '@/components/NavAdmin.vue';
import navbar from '@/components/navbar.vue';
import Logo from '@/components/logo.vue';
import Table from '@/components/Table.vue';
import { ref } from 'vue'
// params of the Table component
const nameBase = ref('advertisements')
const childRef = ref()

// get an emit function from NavAdmin and reactive change the table component
const callGetPosts = () => {
  childRef.value.sayGetPosts()
}
</script>

<template>
  <div>
    <Logo />
  <NavAdmin  
    @name-base-advertisements = 'nameBase = "advertisements",callGetPosts()'
    @name-base-companies = 'nameBase = "companies",callGetPosts()'
    @name-base-people = 'nameBase = "people",callGetPosts()'
    /> 
    <!-- Table component without specific variable to show the whole datas in the database -->
    <Table :nameBase="[nameBase]" ref="childRef" />
    <navbar />
  </div>
</template>

<style scope>
template {
  display: flex;
  flex-wrap: wrap;
  background-color: rgb(230, 239, 233);
}
</style>