<template>
    <div class="profile-container">
        <v-card class="profile-glass" elevation="0" rounded="xl">
            <v-card-title class="profile-header">
                <div class="profile-info">
                    <div>
                        <h2>{{ people.name }}</h2>
                        <p class="email">{{ people.email }}</p>
                    </div>
                </div>
                <v-btn color="primary" @click="toggleEdit" rounded="pill">
                    {{ editMode ? "Save" : "Edit" }}
                </v-btn>

            </v-card-title>

            <v-card-text>
                <v-form>
                    <v-row>
                        <v-col cols="12" md="6">
                            <v-text-field label="Name" v-model="people.name" :disabled="!editMode" variant="outlined" />
                        </v-col>
                        <v-col cols="12" md="6">
                            <v-text-field label="Age" v-model="people.age" :disabled="!editMode" variant="outlined" />
                        </v-col>
                    </v-row>
                </v-form>
            </v-card-text>
            <v-btn color="error" variant="outlined" @click="deletePeople()">
                Delete Account
            </v-btn>
        </v-card>
    </div>
</template>


<script setup>
import { onMounted, ref } from 'vue';
import axios from 'axios';

const people = ref([])
const editMode = ref(false)

function toggleEdit() {
    if (editMode.value) {
        updatePeople()
    }
    editMode.value = !editMode.value
}

onMounted(() => {
    getPeople();
})
async function getPeople() {
    const token = localStorage.getItem('access_token')
    await axios({
        withCredentials: true,
        method: 'get',
        url: "http://127.0.0.1:8000/people/" + localStorage.getItem('seeker_id') + "/",
        responseType: 'json',
        headers: {
            Authorization: `Token ${token}`,
        }
    })
        .then(Response => {
            people.value = Response.data
        })
        .catch(error => {
            console.error(error);
        });
}
async function deletePeople() {
    const token = localStorage.getItem('access_token')
    await axios({
        withCredentials: true,
        method: 'delete',
        url: "http://127.0.0.1:8000/people/" + localStorage.getItem('seeker_id') + "/",
        responseType: 'json',
        headers: {
            Authorization: `Token ${token}`,
        }
    })
        .then(Response => {
            people.value = Response.data
        })
        .catch(error => {
            console.error(error);
        });
}
async function updatePeople() {
    const token = localStorage.getItem('access_token')
    await axios.put(`http://127.0.0.1:8000/people/${localStorage.getItem('seeker_id')}/`, people.value, {
        responseType: 'json',
        headers: {
            Authorization: `Token ${token}`,
        }
    })
        .then(Response => {
            people.value = Response.data
        })
        .catch(error => {
            console.error(error);
        });
}
</script>

<style scoped>
.profile-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 40px;
}

.profile-glass {
    width: 100%;
    max-width: 900px;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: 20px;
    box-shadow: 0 8px 40px rgba(0, 0, 0, 0.25);
    padding: 30px;
    transition: 0.3s;
    display: flex;
    flex-direction: column ;
}

.profile-glass:hover {
    transform: scale(1.01);
}

.profile-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.profile-info {
    display: flex;
    align-items: center;
    gap: 20px;
}

.avatar {
    border: 2px solid white;
}

.email {
    margin-top: 4px;
}

.v-text-field,
.v-textarea {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 12px;
}

h2 {
    font-weight: 600;
}
</style>