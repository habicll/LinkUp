<template>
    <div class="back">
        <div class="glass">
            <form>
                <h1>Sign Up</h1>

                <div class="name">
                    <v-text-field class="input" v-model="state.username"
                        :error-messages="v$.username.$errors.map(e => e.$message)" label="Username" required
                        @blur="v$.username.$touch" @input="v$.username.$touch"></v-text-field>

                    <v-text-field class="input" v-model="state.company_name"
                        :error-messages="v$.company_name.$errors.map(e => e.$message)" label="Company Name" required
                        @blur="v$.company_name.$touch" @input="v$.company_name.$touch" 
                        style="margin-left: 5px;"></v-text-field>
                </div>
                <v-text-field class="input" v-model="state.email"
                    :error-messages="v$.email.$errors.map(e => e.$message)" label="E-mail" required
                    @blur="v$.email.$touch" @input="v$.email.$touch"></v-text-field>

                <h5>Minimum 8 characters</h5>
                
                <v-text-field class="input" v-model="state.password1"
                    :error-messages="v$.password1.$errors.map(e => e.$message)" label="Password" type="password"
                    required @blur="v$.password1.$touch" @input="v$.password1.$touch"></v-text-field>

                <v-text-field class="input" v-model="state.password2"
                    :error-messages="v$.password2.$errors.map(e => e.$message)" label="Confirm password" type="password"
                    required @blur="v$.password2.$touch" @input="v$.password2.$touch"></v-text-field>

                <v-text-field class="input" v-model="state.place"
                    :error-messages="v$.place.$errors.map(e => e.$message)" label="Place" required
                    @blur="v$.place.$touch" @input="v$.place.$touch"></v-text-field>


                <v-textarea class="input" v-model="state.description" label="Description" required rows="2"
                    variant="filled" auto-grow :error-messages="v$.description.$errors.map(e => e.$message)"
                    @blur="v$.description.$touch" @input="v$.description.$touch"></v-textarea>

                <div class="button">
                    <v-btn class="me-3" id="log" @click="goToLogin">
                        Log in
                    </v-btn>
                    <v-btn class="me-4" @click="registerUser" :loading="loading">
                        Sign Up
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
import { reactive, ref } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { email, required } from '@vuelidate/validators'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const loading = ref(false)
const message = ref('')
const error = ref('')

const initialState = {
    username: '',
    company_name:'',
    email: '',
    password1: '',
    password2: '',
    place: '',
    description: '',
}

const state = reactive({
    ...initialState,
})

const rules = {
    username: { required },
    company_name: { required },
    age: { required },
    password1: { required },
    password2: { required },
    email: { required, email },
    place: { required },
    description: { required },
}

const v$ = useVuelidate(rules, state)

async function registerUser() {
    loading.value = true
    message.value = ''
    error.value = ''

    try {
        const response = await axios.post('http://127.0.0.1:8000/dj-rest-auth/registration/', {
            username: state.username,
            companie_name: state.company_name,
            password1: state.password1,
            password2: state.password2,
            email: state.email,
            user_type: 'company',
            place: state.place,
            description: state.description,
        })

        console.log('Réponse du serveur:', response.data)
        message.value = 'Compte créé avec succès ! Redirection...'

        setTimeout(() => {
            router.push('/home')
        }, 2000)

    } catch (err) {
        console.error('Erreur détaillée:', err)
        if (err.response && err.response.data) {
            error.value = err.response.data.error || 'Une erreur est survenue lors de la création du compte'
        } else if (err.request) {
            error.value = 'Impossible de contacter le serveur. Vérifiez votre connexion.'
        } else {
            error.value = 'Erreur inattendue: ' + err.message
        }
    } finally {
        loading.value = false
    }
}

function goToLogin() {
    router.push('/login')
}

function clear() {
    v$.value.$reset()
    for (const [key, value] of Object.entries(initialState)) {
        state[key] = value
    }
    message.value = ''
    error.value = ''
}
</script>

<style scoped>
form h1 {
    text-align: center;
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

.input {
    background-color: transparent;
    height: 100%;
    width: 100%;
}

.inputC {
    background-color: transparent;
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
    width: 70%;
    height: 90%;
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
    transform: scale(1.05);
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

.mt-3 {
    margin-top: 10px;
}

.name {
    display: flex;
}
</style>