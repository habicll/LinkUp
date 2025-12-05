<script setup>
import Login from '@/components/login.vue';
import Logo from '@/components/logo.vue';
import Navbar from '@/components/navbar.vue';
import Signup_company from '@/components/signup_company.vue';
import Signup from '@/components/signup_seek.vue';

</script>

<template>
    <div>
        <Logo />
        <Signup_company />
    </div>
</template>



<style scoped>
div{
    /* background: linear-gradient( rgb(230, 239, 233) , rgb(45, 130, 183)); */
    height: 100vh;
    display: flex;
}
</style>