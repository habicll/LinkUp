<template>
    <div class="profile-container">
        <v-card class="profile-glass" elevation="0" rounded="xl">
            <v-card-title class="profile-header">
                <div class="profile-info">
                    <div>
                        <h2>{{ company.companie_name }}</h2>
                        <p class="email">{{ company.email }}</p>
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
                            <v-text-field label="Company Name" v-model="company.companie_name" :disabled="!editMode"
                                variant="outlined" />
                        </v-col>
                        <v-col cols="12" md="6">
                            <v-text-field label="Location" v-model="company.place" :disabled="!editMode"
                                variant="outlined" />
                        </v-col>
                        <v-col cols="12">
                            <v-textarea label="Description" v-model="company.description" :disabled="!editMode"
                                variant="outlined" rows="4" />
                        </v-col>
                    </v-row>
                </v-form>
            </v-card-text>
            <v-btn color="error" variant="outlined" @click="deleteAccount">
                Delete Account
            </v-btn>
        </v-card>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const company = ref({
    companie_name: '',
    place: '',
    description: '',
})

const userEmail = ref('')
const editMode = ref(false)

function toggleEdit() {
    if (editMode.value) {
        updateCompany()
    }
    editMode.value = !editMode.value
}

async function getCompany() {
    const token = localStorage.getItem('access_token')
    const companyId = localStorage.getItem('company_id')

    try {
        const res = await axios.get(`http://127.0.0.1:8000/companies/${companyId}/`, {
            headers: { Authorization: `Token ${token}` },
        })
        company.value = res.data
        console.log(company.value)
        userEmail.value = res.data.Id_Profil?.user?.email || 'No email found'
    } catch (error) {
        console.error('Erreur lors de la récupération de la compagnie:', error)
    }
}

async function updateCompany() {
    const token = localStorage.getItem('access_token')
    const companyId = localStorage.getItem('company_id')

    try {
        await axios.put(`http://127.0.0.1:8000/companies/${companyId}/`, company.value, {
            headers: { Authorization: `Token ${token}` },
        })
        alert('Profil mis à jour avec succès !')
    } catch (error) {
        console.error('Erreur lors de la mise à jour:', error)
        alert('Erreur lors de la mise à jour.')
    }
}

async function deleteAccount() {
    if (confirm("⚠️ This will permanently delete your account. Continue?")) {
        const token = localStorage.getItem("access_token")
        try {
            await axios.delete("http://127.0.0.1:8000/delete-account/", {
                headers: { Authorization: `Token ${token}` },
            })
            localStorage.clear()
            alert("Your account has been deleted.")
            window.location.href = "/"
        } catch (err) {
            console.error(err)
            alert("Error while deleting account.")
        }
    }
}


onMounted(getCompany)
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
    background: rgba(114, 114, 114, 0);
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
