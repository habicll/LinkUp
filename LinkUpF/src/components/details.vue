<template>
    <div class="swipe-root">
        <div class="glass">
            <div class="info">
                <h1 class="title">Job Description</h1>

                <div class="content">
                    <div class="desc">
                        <p>{{ data.long_description }}</p>
                    </div>

                    <div class="features">
                        <div class="feature">
                            <v-icon color="primary" />
                            <p><strong>Salary:</strong> {{ data.salary }} €</p>
                        </div>
                        <div class="feature">
                            <v-icon color="primary" icon="mdi-calendar-start" />
                            <p><strong>Start:</strong> {{ data.start_date }}</p>
                        </div>
                        <div class="feature">
                            <v-icon color="primary" icon="mdi-calendar-end" />
                            <p><strong>End:</strong> {{ data.end_date }}</p>
                        </div>
                        <div class="feature">
                            <v-icon color="primary" icon="mdi-clock-outline" />
                            <p><strong>Schedule:</strong> {{ data.schredule }}</p>
                        </div>
                    </div>
                </div>
                <div class="apply">
                    <v-btn color="transparent" size="large" variant="flat" rounded="pill">
                        Apply
                        <v-dialog activator="parent" max-width="500">
                            <template v-slot:default="{ isActive }">
                                <v-card rounded="lg" class="pop">
                                    <v-card-title class="d-flex justify-space-between align-center">
                                        <div class="text-h5 ps-2">
                                            Send your message
                                        </div>
                                        <v-btn variant="text" @click="isActive.value = false" />
                                    </v-card-title>

                                    <v-divider class="mb-4" />

                                    <v-card-text>
                                        <div class="mb-2 text-subtitle-1">Message</div>
                                        <v-textarea v-model="message" :counter="300" class="mb-2" rows="3"
                                            variant="outlined" placeholder="Explain why you’re a great fit..."
                                            persistent-counter />
                                    </v-card-text>

                                    <v-divider class="mt-2" />

                                    <v-card-actions class="my-2 d-flex justify-end">
                                        <v-btn rounded="xl" text="Cancel" @click="isActive.value = false" />
                                        <v-btn rounded="xl" color="primary" text="Send" variant="flat"
                                            @click="sendMessage(isActive)" />
                                    </v-card-actions>
                                </v-card>
                            </template>
                        </v-dialog>
                    </v-btn>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import 'swiper/css'
import 'swiper/css/effect-cards'
import axios from 'axios'


const message = ref('')

defineProps({
    data: {
        default: {
            long_description: "No description provided",
            salary: "N/A",
            startDate: "N/A",
            endDate: "N/A",
            schredule: "N/A"
        }
    }
})

async function sendMessage(isActive) {
    const job = JSON.parse(localStorage.getItem('job'))
    const token = localStorage.getItem('access_token')

    try {
        await axios.post('http://127.0.0.1:8000/applications/', {
            Id_Profil:1,
            Id_Job: job,
            accept: null,
            message: message.value
        },
            {
                headers: {
                    Authorization: `Token ${token}`,
                }
            })
        console.log("message sent")
        isActive.value = false
    }
    catch (err) {
        console.error('Error sending message:', err)
    }

}
</script>

<style scoped>
.swipe-root {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 80vh;
}

.glass {
    width: 65%;
    height: 75%;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: rgba(45, 130, 183, 0.32);
    border-radius: 20px;
    box-shadow: 0 8px 40px rgba(0, 0, 0, 0.25);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    transition: all 0.3s ease-in-out;
    border: 1px solid rgba(255, 255, 255, 0.3);
}

.glass:hover {
    transform: scale(1.02);
    box-shadow: 0 10px 50px rgba(0, 0, 0, 0.3);
}

.info {
    width: 85%;
    text-align: left;
}

.title {
    text-align: center;
    font-size: 2rem;
    margin-bottom: 2rem;
    letter-spacing: 1px;
}

.content {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 1.5rem;
}

.desc {
    flex: 1 1 55%;
    font-size: 1.1rem;
    line-height: 1.6;
    background: rgba(255, 255, 255, 0.1);
    padding: 1.2rem;
    border-radius: 12px;
}

.features {
    flex: 1 1 35%;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.feature {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    background: rgba(255, 255, 255, 0.12);
    padding: 0.8rem 1rem;
    border-radius: 12px;
    transition: background 0.2s;
}

.feature:hover {
    background: rgba(255, 255, 255, 0.2);
}

.apply {
    margin-top: 2rem;
    text-align: center;
}

.pop {
    background-color: rgba(45, 130, 183, 0.6);
    border-radius: 20px;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    transition: all 0.3s ease-in-out;
    color: white;
}

.butt {
    width: 10%;
}
</style>
