<script setup>
const emit = defineEmits(['name-base-advertisements','name-base-companies','name-base-people'])
</script>

<template>
    <div class="nav">
    <button @click="$emit('name-base-advertisements')">Advertisements</button>
        <button @click="$emit('name-base-companies')">Companies</button>
    <button @click="$emit('name-base-people')">People</button>
    </div>
</template>

<style>
.nav{
    position: relative;
    display: flex;
    justify-content: space-around;
    align-items: center;
    height: 100%;
    top : 150px;
    background-color: transparent;
    
}
</style>