<!-- make the status of seeker -->
<template>
    <div class="status-back">
        <div class="status-glass">
            <h1>Status Board</h1>

            <v-list class="status-list">
                <template v-for="(item,key) in items" :key="index">
                    <v-list-item class="status-item" ripple>
                            <template v-slot:title>
                                <div class="companie-title">{{ item.Id_Job.Id_Profil.companie_name }}</div>
                                <div class="job-title">{{ item.Id_Job.title }}</div>
                            </template>

                            <template v-slot:subtitle>
                                <div class="job-message">{{ item.message }}</div>
                            </template>

                            <template v-slot:append>
                                <v-chip :color="getStatusColor(item.accept)[0]" text-color="white" class="status-chip">
                                    {{ getStatusColor(item.accept)[1]}}
                                </v-chip>
                            </template>
                    </v-list-item>

                    <v-divider class="my-2"></v-divider>
                </template>
            </v-list>
        </div>
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import axios from 'axios';

const companies = ref([])
const jobs = ref([])
const items = ref([])

onMounted(() => {
    getCompanies();
    getJobs();
    getStatus();
})

// get a applications with all reliatable table in database to facilite the print
async function getStatus() {
    const token = localStorage.getItem('access_token')
    await axios({
        withCredentials: true,
        method: 'get',
    url: "http://127.0.0.1:8000/applications/",
        responseType: 'json',
        headers: {
            Authorization: `Token ${token}`,
        }
    })
    .then(Response => {
        for(const data in Response.data){
            if(Response.data[data].Id_Profil == localStorage.getItem('seeker_id')){
                for(const job in jobs.value){
                    if(jobs.value[job].id == Response.data[data].Id_Job){
                        Response.data[data].Id_Job = jobs.value[job]
                        for(const companie in companies.value){
                            if(companies.value[companie].id == jobs.value[job].Id_Profil){
                                console.log(jobs.value[job].Id_Profil)
                                jobs.value[job].Id_Profil = companies.value[companie]
                                console.log(jobs.value[job].Id_Profil)
                            }
                        }
                    }
                }
                items.value.push(Response.data[data]);
                console.log(items.value)
            }
        }
    })
    .catch(error => {
        console.error(error);
    });
}
async function getJobs() {
    const token = localStorage.getItem('access_token')
    await axios({
        withCredentials: true,
        method: 'get',
    url: "http://127.0.0.1:8000/advertisements/",
        responseType: 'json',
        headers: {
            Authorization: `Token ${token}`,
        }
    })
        .then(Response => {
            jobs.value = Response.data
        })
        .catch(error => {
            console.error(error);
        });
}
async function getCompanies() {
    const token = localStorage.getItem('access_token')
    await axios({
        withCredentials: true,
        method: 'get',
        url: "http://127.0.0.1:8000/companies/",
        responseType: 'json',
        headers: {
            Authorization: `Token ${token}`,
        }
    })
        .then(Response => {
            companies.value = Response.data
        })
        .catch(error => {
            console.error(error);
        });
}
function getStatusColor(status) {
    switch (status) {
        case true:
            return ["green","accepted"]
        case false:
            return ["red","refused"]
        case null:
            return ["orange","waiting..."]
        default:
            return "grey"
    }
}
</script>

<style scoped>
.status-back {
    width: 100%;
    height: 80vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

.status-glass {
    width: 70%;
    height: 75%;
    background: rgba(71, 104, 151, 0.132);
    border-radius: 20px;
    box-shadow: 0 8px 40px rgba(0, 0, 0, 0.2);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    padding: 30px;
    overflow-y: auto;
    transition: transform 0.3s;
    
}

.status-glass:hover {
    transform: scale(1.02);
    box-shadow: 0 12px 60px rgba(0, 0, 0, 0.3);
    border: 1px solid white;
}

.status-glass h1 {
    text-align: center;
    margin-bottom: 25px;
    font-size: 2em;
    font-weight: 600;
    letter-spacing: 1px;
}

.status-list {
    background: transparent !important;
    
}

.status-item {
    display: flex;
    align-items: center;
    transition: background 0.3s ease;
    justify-content: space-between;

}

.status-item:hover {
    background: rgba(0, 0, 0, 0.1);
    border-radius: 12px;
}

.companie-title {
    font-weight: 600;
    font-size: 1.1em;
    margin-bottom: 3px;
}

.job-message {
    font-size: 0.9em;
}

.status-chip {
    font-weight: bold;
    text-transform: uppercase;
}
</style>