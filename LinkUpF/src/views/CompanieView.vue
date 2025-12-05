<script setup>
import navbar from '@/components/navbar.vue';
import Logo from '@/components/logo.vue';
import Table from '@/components/Table.vue';
import { ref } from 'vue'
// params of the Table component
const nameBase = ref("advertisements")
const moreNameBase = localStorage.getItem('company_id')

</script>

<template>
  <div>
    <Logo />
    <!-- create table component with specifying values -->
    <Table
      :nameBase="[nameBase, moreNameBase, ['id', 'title', 'short_description', 'long_description', 'salary', 'start_date', 'end_date', 'schredule', 'Id_Profil']]"
      ref="childRef" />
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
