<template>
    <div class="back">
        <div class="glass">
            <form>
                <h1>Register yourself</h1>

                <div class="button">
                    <v-btn class="me-3" @click="goToSignupC">
                        <v-icon icon="mdi-domain" size="large"></v-icon>
                        <img src="/company.png" alt="">
                        Company
                    </v-btn>
                    <v-btn class="me-3" @click="goToSignup">
                        <img src="/seek.png" alt="">
                        Job Seeker
                    </v-btn>
                </div>
                <v-btn class="me-4" @click="goToAdmin">
                    <img src="/admin.png" alt="">
                    Admin
                </v-btn>
            </form>
        </div>
    </div>
</template>
<script setup>
import { useRouter } from 'vue-router'


const router = useRouter()

function goToAdmin() {
    window.location.replace("http://127.0.0.1:8000/admin/"); 
}

function goToSignup() {
    router.push('/signup')
}

function goToSignupC() {
    router.push('/signupCompany')
}


</script>

<style scoped>
form h1 {
    text-align: center;
    margin-top: -5%;
    margin-bottom: 4%;
}

form {
    display: flex;
    flex-direction: column;
    align-content: center;
    justify-content: center;
    width: 90%;
    height: 70%;
    margin: auto;
    max-height: 80%;
    max-width: 100%;
}


.back {
    background: linear-gradient(rgb(230, 239, 233), rgb(45, 130, 183));
    width: 100%;
    height: 100%;
    justify-content: center;
    align-items: center;
}

.glass {
    width: 60%;
    height: 50%;
    display: flex;
    justify-content: center;
    background: rgba(255, 255, 255, 0.32);
    border-radius: 16px;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(8.6px);
    -webkit-backdrop-filter: blur(8.6px);
    transition: transform .2s;
}

.glass:hover {
    transform: scale(1.1);
    border: 1px solid rgba(255, 255, 255, 1);
}

.me-3 {
    width: 40%;
    background-color: transparent;
}

.me-4 {
    width: 40%;
    background-color: transparent;
    margin-left: 30%;
}

.me-3:hover {
    background-color: white;
}

.me-4:hover {
    background-color: white;
}


.button {
    display: flex;
    justify-content: space-around;
    align-items: center;
    margin-top: 3%;
    width: 100%;
    height: 40%;
}



img {
    width: 11%;
}

</style>