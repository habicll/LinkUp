<template>
    <div class="form-root">
        <v-card class="form-glass" elevation="0" rounded="xl">
            <v-card-title class="form-title">
                <h2>{{ Datas.NameDatas[1].nameBase[0] }}</h2>
            </v-card-title>

            <v-card-text>
                <v-form ref="formRef">
                    <v-row>
                            <v-col v-for="name in Datas.NameDatas[0]" :key="name" cols="12" md="6"
                            v-show="(name != 'id') && ((Datas.NameDatas[1].nameBase[0] == 'advertisements') && (name != 'Id_Profil') || (Datas.NameDatas[1].nameBase[0] != 'advertisements'))">
                            <v-text-field v-if="name == 'age' || name == 'salary'" :id="name" :name="name" :label="name"
                                type="number" v-model="formData[name]" variant="outlined" color="primary"
                                class="glass-input" density="comfortable" />

                            <v-select v-else-if="(Datas.NameDatas[1].nameBase[0] == 'advertisements') && (name == 'Id_Profil')"
                                :id="name" :name="name" :label="name" :items="[Datas.NameDatas[1].nameBase[1]]"
                                v-model="formData[name]" variant="outlined" color="primary"
                                class="glass-input" density="comfortable" />

                            <v-text-field v-else-if="name == 'end_date' || name == 'start_date'" :id="name" :name="name"
                                :label="name" type="date" v-model="formData[name]" variant="outlined"
                                color="primary" class="glass-input" density="comfortable" />

                            <v-text-field v-else-if="name != 'id'" :id="name" :name="name" :label="name" type="text"
                                v-model="formData[name]" variant="outlined" color="primary"
                                class="glass-input" density="comfortable" />

                            <v-text-field v-else-if="Datas.NameDatas[3] == 'update'" :id="name" :name="name"
                                type="hidden" v-model="formData[name]" style="display: none;" />
                        </v-col>
                    </v-row>
                </v-form>
            </v-card-text>

            <v-card-actions class="form-actions">
                <v-spacer />
                <v-btn v-if="Datas.NameDatas[3] == 'create'" @click="Create()" color="success" variant="elevated"
                    size="large" rounded="pill" class="action-btn">
                    Create
                </v-btn>

                <v-btn v-if="Datas.NameDatas[3] == 'update'" @click="Update()" color="primary" variant="elevated"
                    size="large" rounded="pill" class="action-btn">
                    Update
                </v-btn>
            </v-card-actions>
        </v-card>
    </div>
</template>
<script setup>
import { onMounted, ref } from 'vue'
import 'swiper/css'
import 'swiper/css/effect-cards'
import axios from 'axios';
const emit = defineEmits(['Finish'])
const Datas = defineProps({ NameDatas: Array })
const Companies = ref([])
const formData = ref({})

async function Create() {
    const token = localStorage.getItem('access_token')
    const FormDatas = {}
    
    // Récupérer les données du formulaire depuis formData
    for (const name in Datas.NameDatas[0]) {
        if (Datas.NameDatas[0][name] !== 'id') {
            FormDatas[Datas.NameDatas[0][name]] = formData.value[Datas.NameDatas[0][name]] || ''
        }
    }
    
    console.log('FormDatas to send:', FormDatas)
    
    axios({
        withCredentials: true,
        method: 'post',
        url: "http://127.0.0.1:8000/" + Datas.NameDatas[1].nameBase[0] + "/",
        responseType: 'json',
        data: FormDatas,
        headers: {
            Authorization: `Token ${token}`,
        }
    })
        .then(() => {
            alert("L'élément a été créé avec succès!");
            emit('Finish');
        })
        .catch(error => {
            alert("Erreur lors de la création: " + (error.response?.data?.message || "Valeurs incorrectes"));
            console.error(error);
        });
};

async function Update() {
    const token = localStorage.getItem('access_token')
    const FormDatas = {}
    
    for (const name in Datas.NameDatas[0]) {
        if (Datas.NameDatas[0][name] !== 'id') {
            FormDatas[Datas.NameDatas[0][name]] = formData.value[Datas.NameDatas[0][name]] || ''
        }
    }
    
    console.log('FormDatas to update:', FormDatas)
    
    axios({
        withCredentials: true,
        method: 'PUT',
        url: "http://127.0.0.1:8000/" + Datas.NameDatas[1].nameBase[0] + "/" + Datas.NameDatas[2]['id'] + "/",
        responseType: 'json',
        data: FormDatas,
        headers: {
            Authorization: `Token ${token}`,
        }
    })
        .then(() => {
            alert("L'élément a été mis à jour avec succès!");
            emit('Finish');
        })
        .catch(error => {
            alert("Erreur lors de la mise à jour: " + (error.response?.data?.message || "Valeurs incorrectes"));
            console.error(error);
        });
};


onMounted(() => {
    GetCompanies();
    initializeFormData();
})

function initializeFormData() {
    const initialData = {}
    
    for (const name of Datas.NameDatas[0]) {
        if (name === 'Id_Profil' && Datas.NameDatas[1].nameBase[0] === 'advertisements') {
            initialData[name] = Datas.NameDatas[1].nameBase[1]
        } else {
            initialData[name] = Datas.NameDatas[2][name] || ''
        }
    }
    
    formData.value = initialData
    console.log('Form data initialized:', formData.value)
}

async function GetCompanies() {
    const token = localStorage.getItem('access_token')
    if (Datas.NameDatas[1].nameBase[1] != "") {
        await axios({
            withCredentials: true,
            method: 'get',
            url: "http://127.0.0.1:8000/companies/" + Datas.NameDatas[1].nameBase[1] + "/",
            responseType: 'json',
            headers: {
                Authorization: `Token ${token}`,
            }
        })
            .then(Response => {
                Companies.value = Response.data;
                console.log(Companies.value)
            })
            .catch(error => {
                console.error(error);
            });
    } else {
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
                Companies.value = Response.data;
            })
            .catch(error => {
                console.error(error);
            });
    }
}
</script>
<style scoped>
.form-root {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
}

.form-glass {
    width: 100%;
    max-width: 800px;
    background: rgba(71, 104, 151, 0.15) !important;
    border-radius: 20px !important;
    box-shadow: 0 8px 40px rgba(0, 0, 0, 0.25) !important;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    transition: all 0.3s ease-in-out;
}

.form-glass:hover {
    transform: scale(1.01);
    box-shadow: 0 12px 60px rgba(0, 0, 0, 0.3) !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
}

.form-title {
    text-align: center;
    padding: 30px 24px 20px 24px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.form-title h2 {
    font-size: 2rem;
    font-weight: 600;
    margin: 0;
    color: white !important;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    text-transform: capitalize;
}

.form-actions {
    padding: 20px 24px 30px 24px;
    border-top: 1px solid rgba(255, 255, 255, 0.2);
}

.action-btn {
    font-weight: 500;
    letter-spacing: 0.5px;
    min-width: 120px;
    transition: all 0.3s ease;
}

.action-btn:hover {
    transform: translateY(-2px);
}

/* Vuetify input styling */
:deep(.glass-input .v-field) {
    background: rgba(255, 255, 255, 0.08) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 12px !important;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
}

:deep(.glass-input .v-field:hover) {
    background: rgba(255, 255, 255, 0.12) !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
}

:deep(.glass-input .v-field--focused) {
    background: rgba(255, 255, 255, 0.15) !important;
    border: 2px solid rgba(45, 130, 183, 0.6) !important;
    box-shadow: 0 0 0 2px rgba(45, 130, 183, 0.2) !important;
}

:deep(.glass-input .v-field__input) {
    color: white !important;
    font-weight: 400;
}

:deep(.glass-input .v-field__input::placeholder) {
    color: rgba(255, 255, 255, 0.6) !important;
}

:deep(.glass-input .v-label) {
    color: rgba(255, 255, 255, 0.8) !important;
    font-weight: 500;
}

:deep(.glass-input .v-label.v-field-label--floating) {
    color: rgba(45, 130, 183, 0.9) !important;
}

:deep(.glass-input .v-field__outline) {
    display: none;
}

/* Select dropdown styling */
:deep(.v-select .v-field__append-inner) {
    color: rgba(255, 255, 255, 0.8) !important;
}

:deep(.v-overlay__content) {
    background: rgba(71, 104, 151, 0.95) !important;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 12px !important;
}

:deep(.v-list) {
    background: transparent !important;
}

:deep(.v-list-item) {
    color: white !important;
}

:deep(.v-list-item:hover) {
    background: rgba(45, 130, 183, 0.3) !important;
}

/* Card content styling */
:deep(.v-card-text) {
    color: white !important;
}

/* Responsive design */
@media (max-width: 768px) {
    .form-root {
        padding: 10px;
    }

    .form-title h2 {
        font-size: 1.5rem;
    }

    .action-btn {
        width: 100%;
        margin-top: 10px;
    }
}
</style>