<!-- Make a swipe of all jobs with Swiper library for seeker home -->
<template>
    <div class="swipe-root">
        <div v-if="!showDescription">
            <section>
                <Swiper id="swiper" :modules="modules" effect="cards" :grabCursor="true" :loop="true" :initialSlide="0"
                    :speed="50" class="swiper-container" @swiper="onSwiper" @slideChange="onSlideChange">
                    <SwiperSlide v-for="job in jobs" :key="job.id" class="card-slide">
                        <div class="card">
                            <h2>{{ job.title }}</h2>
                            <p>{{ job.short_description }}</p>
                            <img src="/logo.jpeg" alt="logo" />
                            <v-btn class="butt" @click="jobDescriptionShow(job)">
                                learn more
                            </v-btn>
                        </div>
                    </SwiperSlide>
                </Swiper>
            </section>
        </div>
        <v-btn color="transparent" size="large" variant="flat" rounded="pill" @click="dialogActive = true">
        </v-btn>

        <v-dialog v-model="dialogActive" max-width="500">
            <template #default>
                <v-card rounded="lg" class="pop">
                    <v-card-title class="d-flex justify-space-between align-center">
                        <div class="text-h5 ps-2">
                            Send your message
                        </div>
                    </v-card-title>

                    <v-divider class="mb-4" />

                    <v-card-text>
                        <div class="mb-2 text-subtitle-1">Message</div>
                        <v-textarea v-model="message" :counter="300" class="mb-2" rows="3" cols="100" variant="outlined"
                            placeholder="Explain why you’re a great fit..." persistent-counter />
                    </v-card-text>

                    <v-divider class="mt-2" />

                    <v-card-actions class="my-2 d-flex justify-end">
                        <v-btn rounded="xl" text="Cancel" @click="dialogActive = false" />
                        <v-btn rounded="xl" color="primary" text="Send" variant="flat"
                            @click="sendMessage()" />
                    </v-card-actions>
                </v-card>
            </template>
        </v-dialog>
        <div v-if="showDescription" class="description-container">
            <Details v-bind:data="jobDescription" />
            <v-btn class="exit-btn" @click="jobDescriptionUnshow()">
                Exit
            </v-btn>
        </div>
    </div>
</template>
<script setup>
import Details from './details.vue'
import { onMounted, ref } from 'vue'
import { Swiper, SwiperSlide } from 'swiper/vue'
import { EffectCards, Mousewheel } from 'swiper'


import 'swiper/css'
import 'swiper/css/effect-cards'
import axios from 'axios';

const modules = [EffectCards, Mousewheel]
const showDescription = ref(false)
const jobDescription = ref([])
const jobs = ref([])
const slideChange = ref(true)
const message = ref('')
const dialogActive = ref(false)


onMounted(() => {
    getPosts();
});

async function getPosts() {
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
            jobs.value = Response.data;
        })
        .catch(error => {
            console.error(error);
        });
}


function onSlideChange(swiper) {
    const index = swiper.realIndex
    const jobActuel = jobs.value[index]
    if (jobActuel && jobActuel.id !== undefined) {
        localStorage.setItem('job', jobActuel.id)
    }

    if (slideChange.value) {
        slideChange.value = false
        return
    }

    const prevIndex = swiper.previousIndex ?? null
    const currentIndex = swiper.activeIndex ?? swiper.realIndex
    if (prevIndex !== null && typeof prevIndex === 'number') {
        const movedBackward = currentIndex < prevIndex
        if (movedBackward) dialogActive.value = true
    }

    slideChange.value = true
}


function jobDescriptionShow(data) {
    jobDescription.value = data
    showDescription.value = true
}
function jobDescriptionUnshow() {
    showDescription.value = false
}
async function sendMessage() {
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
        dialogActive.value = false
    }
    catch (err) {
        console.error('Error sending message:', err)
    }

}

</script>

<style scoped>
div {
    width: 100%;
    height: 100%;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
}

.swipe-root {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 76vh;
    background-color: transparent;
    overflow: hidden;
    position: relative;
    z-index: 0;
    -webkit-clip-path: inset(0);
    clip-path: inset(0);


}

section {
    margin-top: 5%;
    width: 50%;
    height: 80%;
    overflow: hidden;
    position: relative;
    -webkit-clip-path: inset(0);
    clip-path: inset(0);
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 12px;

}

.swiper-container {
    width: 100%;
    height: 100%;
    overflow: hidden;
    position: relative;
    -webkit-clip-path: inset(0);
    clip-path: inset(0);

}

.card-slide {
    width: 100% !important;
    height: 100% !important;
    display: flex;
    justify-content: center;
    align-items: center;

}

.card {
    background-color: rgb(27, 40, 69);
    color: white;
    width: 90%;
    height: 90%;
    text-align: center;
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 15px 30px rgba(0, 0, 0, 0.4);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    backface-visibility: hidden;
    transform-style: preserve-3d;
}

.card h2 {
    font-size: 1.6rem;
    margin-top: 0.5rem;
}

.card h4 {
    font-size: 1.1rem;
    margin: 0.5rem 0 1rem 0;
}

.card p {
    font-size: 0.95rem;
    line-height: 1.4;
    margin-bottom: 1rem;
}

.card img {
    width: 18%;
    align-self: center;
}

.apply {
    margin-top: 2rem;
    text-align: center;
}

.pop {
    background-color: rgb(27, 40, 69);
    border-radius: 20px;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    transition: all 0.3s ease-in-out;
    color: white;
}

.butt {
    width: 20%;
}

.description-container {
    width: 100%;
    height: 100%;
}

.exit-btn {
    z-index: 1;
}





</style>