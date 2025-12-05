<template>
    <div class="back">
        <div class="glass">
            <form @submit.prevent="login">
                <h1>Log In</h1>

                <v-text-field class="input" v-model="state.username"
                    :error-messages="v$.username.$errors.map(e => e.$message)" label="Username" required
                    @blur="v$.username.$touch" @input="v$.username.$touch"></v-text-field>

                <v-text-field class="input" v-model="state.password"
                    :error-messages="v$.password.$errors.map(e => e.$message)" label="Password" required
                    @blur="v$.password.$touch" @input="v$.password.$touch" type="password"></v-text-field>

                <div class="button">
                    <v-btn class="me-3" id="sign" type="button">
                        Sign up
                    </v-btn>
                    <v-btn class="me-4" type="submit" :loading="loading">
                        Connect
                    </v-btn>
                </div>
                <v-alert v-if="message" type="success" class="mt-3">
                    {{ message }}
                </v-alert>
                <v-alert v-if="error" type="error" class="mt-3">
                    {{ error }}
                </v-alert>
            </form>
        </div>
    </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { email, required } from '@vuelidate/validators'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'


const router = useRouter()
const loading = ref(false)
const message = ref('')
const error = ref('')
const auth = useAuthStore()

const initialState = {
    username: '',
    password: '',
}

const state = reactive({
    ...initialState,
})


const rules = {
    password: { required },
    username: { required },
}


const v$ = useVuelidate(rules, state)




async function login() {

    const isFormCorrect = await v$.value.$validate()
    if (!isFormCorrect) {
        error.value = 'Veuillez corriger les erreurs du formulaire'
        return
    }

    loading.value = true
    message.value = ''
    error.value = ''
    const store = useAuthStore()


    try {
        const res = await axios.post('http://127.0.0.1:8000/dj-rest-auth/login/', {
            username: state.username,
            password: state.password,
        })
        store.token = res.data.access
        console.log(res.data)

        auth.setAuthenticated(true)
        if (res.data.user) auth.setUser(res.data.user)
        message.value = 'Compte Valide ! Redirection...'
            
        localStorage.setItem('access_token', res.data.key)
        localStorage.setItem('company_id', res.data.company_id)
        localStorage.setItem('seeker_id', res.data.seeker_id)
        localStorage.setItem('type',res.data.user_type)


        

        setTimeout(() => {
            router.push('/home')
            console.log('home')
        }, 800)
    } catch (err) {
        console.error('Erreur détaillée:', err)
        if (err.response && err.response.data) {
            error.value = err.response.data.error || 'Une erreur est survenue lors de la connexion au compte'
        } else if (err.request) {
            error.value = 'Impossible de contacter le serveur. Vérifiez votre connexion.'
        } else {
            error.value = 'Erreur inattendue: ' + err.message
        }
    } finally {
        loading.value = false
    }
}




onMounted(() => {
    const sign = document.getElementById('sign')
    if (sign) {
        sign.addEventListener('click', () => {
            goToSign()
        })
    }
})



function goToSign() {
    router.push('/signup')
}


function clear() {
    v$.value.$reset()

    for (const [key, value] of Object.entries(initialState)) {
        state[key] = value
    }
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
    height: 60%;
    margin: auto;
    max-height: 80%;
    max-width: 100%;
}

.input {
    background-color: transparent;
    height: 100%;
    width: 100%;
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
    width: 30%;
    background-color: transparent;
    text-decoration: underline;
    box-shadow: none;
}

.me-4 {
    width: 30%;
}

.button {
    display: flex;
    justify-content: space-around;
    align-items: center;
    margin-top: 3%;
    width: 100%;
}
</style>