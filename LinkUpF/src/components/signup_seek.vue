<template>
    <div class="back">
        <div class="glass">
            <form>
                <h1>Sign Up</h1>

                <div class="name">

                    <v-text-field class="input1" v-model="state.username"
                        :error-messages="v$.username.$errors.map(e => e.$message)" label="Username" required
                        @blur="v$.username.$touch" @input="v$.username.$touch" style="width: 20%;">

                    </v-text-field><v-text-field class="input1" v-model="state.name"
                        :error-messages="v$.name.$errors.map(e => e.$message)" label="Name" required
                        @blur="v$.name.$touch" @input="v$.name.$touch"
                        style="width: 20%; margin-left: 5px;"></v-text-field>

                </div>

                <h5>Min:16/Max:99</h5>

                <v-number-input class="input" v-model="state.age" :max="99" :min="16" label="Age" :model-value="16"
                    required @blur="v$.age.$touch" @input="v$.age.$touch"></v-number-input>

                <v-text-field class="input" v-model="state.email"
                    :error-messages="v$.email.$errors.map(e => e.$message)" label="E-mail" required
                    @blur="v$.email.$touch" @input="v$.email.$touch"></v-text-field>


                <h5>Minimum 8 characters</h5>

                <v-text-field class="input" v-model="state.password1"
                    :error-messages="v$.password1.$errors.map(e => e.$message)" label="Password" type="password" required
                    @blur="v$.password1.$touch" @input="v$.password1.$touch"></v-text-field>
                    
                <v-text-field class="input" v-model="state.password2"
                    :error-messages="v$.password2.$errors.map(e => e.$message)" label="Confirm password" type="password" required
                    @blur="v$.password2.$touch" @input="v$.password2.$touch"></v-text-field>

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
    name: '',
    age: 16,
    email: '',
    password1: '',
    password2: '',
}

const state = reactive({
    ...initialState,
})

const rules = {
    username: { required },
    name: { required },
    age: { required },
    password1: { required },
    password2: { required },
    email: { required, email },
}

const v$ = useVuelidate(rules, state)

async function registerUser() {
    const isFormCorrect = await v$.value.$validate()
    if (!isFormCorrect) {
        error.value = 'Veuillez corriger les erreurs du formulaire'
        return
    }

    loading.value = true
    message.value = ''
    error.value = ''

    try {
        const response = await axios.post('http://127.0.0.1:8000/dj-rest-auth/registration/', {
            username: state.username,
            name: state.name,
            password1: state.password1,
            password2: state.password2,
            email: state.email,
            user_type: 'seeker',
            age: state.age,
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
    margin-bottom: 1%
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

.input1 {
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
    width: 70%;
    height: 75%;
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

.mt-3 {
    margin-top: 10px;
}

.name {
    display: flex;
}
</style>