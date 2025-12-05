<!-- Table component create a reactive table with element from the database. -->
<template>
  <div class="table-root">
    <div v-if="(!formActivateCreate) && (!formActivateUpdate)" class="table-glass">
      <div class="table-header">
        <h2>{{ nameBase.nameBase[0] }} Management</h2>
        <v-btn @click="Create()" color="primary" variant="elevated" rounded="pill" size="large" class="elevation-4">
          Create {{ nameBase.nameBase[0] }}
        </v-btn>
      </div>

      <v-card class="table-card" elevation="0" rounded="lg">
        <v-data-table :headers="tableHeaders" :items="datas" :items-per-page="10" class="glass-table"
          hide-default-footer>
          <template v-slot:[`item.actions`]="{ item }">
            <div class="d-flex ga-2">
              <v-btn @click="Update(item)" color="success" variant="elevated" size="small" rounded="pill">
                Edit
              </v-btn>
              <v-btn @click="Delete(item.id)" color="error" variant="elevated" size="small" rounded="pill">
                Delete
              </v-btn>
            </div>
          </template>
        </v-data-table>
      </v-card>
    </div>

    <div v-if="formActivateCreate" class="form-glass">
      <div class="form-header">
        <h3>Create {{ nameBase.nameBase[0] }}</h3>
        <v-btn @click="UnCreate()" color="error" variant="outlined" size="small" rounded="pill">
          Cancel
        </v-btn>
      </div>
      <Form :NameDatas="[nameDatas, nameBase, [], 'create']" @Finish="UnCreate()" />
    </div>

    <div v-if="formActivateUpdate" class="form-glass">
      <div class="form-header">
        <h3>Update {{ nameBase.nameBase[0] }}</h3>
        <v-btn @click="UnUpdate()" color="error" variant="outlined" size="small" rounded="pill">
          Cancel
        </v-btn>
      </div>
      <Form :NameDatas="[nameDatas, nameBase, UpdateValue, 'update']" @Finish="UnUpdate()" />
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import 'swiper/css'
import 'swiper/css/effect-cards'
import axios from 'axios';
import Form from './Form.vue';

// initiate all reactive variable the table will use 
const nameBase = defineProps({ nameBase: Array })
const datas = ref([])
const nameDatas = ref([])
const UpdateValue = ref([])
const formActivateCreate = ref(false)
const formActivateUpdate = ref(false)

const tableHeaders = computed(() => {
  if (nameDatas.value.length === 0) return []

  const headers = nameDatas.value
    .filter(name => name !== 'id' && name !== 'Id_Profil')
    .map(name => ({
      title: name,
      key: name,
      align: 'start',
      sortable: true
    }))

  headers.push({
    title: 'Actions',
    key: 'actions',
    align: 'center',
    sortable: false
  })

  return headers
})

// get the emit from the parent component to reactivity
const sayGetPosts = () => {
  GetPosts()
}
defineExpose({ sayGetPosts })

// do it first
onMounted(() => {
  GetPosts()
});

// get all with a path
async function GetPosts() {
  const token = localStorage.getItem('access_token')
  let oldNameBase = nameBase.nameBase[0]
  await axios({
    withCredentials: true,
    method: 'get',
    url: "http://127.0.0.1:8000/" + nameBase.nameBase[0],
    responseType: 'json',
    headers: {
      Authorization: `Token ${token}`,
    }

  })
    .then(Response => {
      if (oldNameBase != nameBase.nameBase[0]) {
        GetPosts()
      } else {
        if (Response.data[0] != null) {
          for (const index in Response.data) {
            if (Response.data[index].Id_Profil == nameBase.nameBase[1]) {
              datas.value.push(Response.data[index]);
            }
          }
          nameDatas.value = Object.keys(Response.data[0])
        } else {
          nameDatas.value = nameBase.nameBase[2]
        }
      }
    })
    .catch(error => {
      console.error(error);
    });

}
function Create() {
  formActivateCreate.value = true
}
function UnCreate() {
  formActivateCreate.value = false
}
function Update(value) {
  UpdateValue.value = value
  formActivateUpdate.value = true
}
function UnUpdate() {
  formActivateUpdate.value = false
}

// del a line with a path
function Delete(value) {
  const token = localStorage.getItem('access_token')
  axios({
    withCredentials: true,
    method: 'delete',
    url: "http://127.0.0.1:8000/" + nameBase.nameBase[0] + "/" + value + "/",
    responseType: 'json',
    headers: {
      Authorization: `Token ${token}`,
    }
  })
    .catch(error => {
      console.error(error);
    });

}
</script>

<style scoped>
.table-root {
  width: 100%;
  height: 82vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.table-glass,
.form-glass {
  width: 90%;
  max-width: 1200px;
  min-height: 75%;
  background: rgba(71, 104, 151, 0.15) !important;
  border-radius: 20px !important;
  box-shadow: 0 8px 40px rgba(0, 0, 0, 0.25) !important;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  padding: 30px;
  transition: all 0.3s ease-in-out;
  border: 1px solid rgba(255, 255, 255, 0.2) !important;
  color: white !important;
}

.table-glass:hover,
.form-glass:hover {
  transform: scale(1.01);
  box-shadow: 0 12px 60px rgba(0, 0, 0, 0.3) !important;
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
}

.table-header,
.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.table-header h2,
.form-header h3 {
  font-size: 2rem;
  font-weight: 600;
  margin: 0;
  color: white !important;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.form-header h3 {
  font-size: 1.5rem;
}

.table-card {
  background: rgba(255, 255, 255, 0.05) !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

/* Vuetify data table styling */
:deep(.v-data-table) {
  background: transparent !important;
  color: white !important;
}

:deep(.v-data-table__wrapper) {
  background: transparent !important;
}

:deep(.v-data-table-header) {
  background: rgba(45, 130, 183, 0.2) !important;
}

:deep(.v-data-table-header th) {
  color: rgba(255, 255, 255, 0.9) !important;
  font-weight: 600 !important;
  text-transform: uppercase;
  letter-spacing: 1px;
  border-bottom: 2px solid rgba(255, 255, 255, 0.2) !important;
}

:deep(.v-data-table__tr:hover) {
  background: rgba(45, 130, 183, 0.15) !important;
}

:deep(.v-data-table__td) {
  color: rgba(255, 255, 255, 0.85) !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
}

:deep(.v-data-table__tr:nth-child(even)) {
  background: rgba(255, 255, 255, 0.03) !important;
}

/* Responsive design */
@media (max-width: 768px) {
  .table-root {
    padding: 10px;
  }

  .table-glass,
  .form-glass {
    width: 95%;
    padding: 20px;
  }

  .table-header,
  .form-header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }
}
</style>