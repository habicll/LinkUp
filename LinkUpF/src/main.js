import './assets/main.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import { createPinia } from 'pinia'

const vuetify = createVuetify({
	components,
	directives,
	icons: {
		defaultSet: 'mdi',
		aliases,
		sets: { mdi },
	},
})

const pinia = createPinia({
	
})


createApp(App)
	.use(router)
	.use(vuetify)
	.use(pinia)
	.mount('#app')

import 'swiper/css'