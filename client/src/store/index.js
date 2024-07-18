import Vue from 'vue';
import Vuex from 'vuex';

import { auth } from './auth.module';
import {transaction} from './transaction.module'
import VueMaterial from 'vue-material'
import 'vue-material/dist/vue-material.min.css'
import 'vue-material/dist/theme/default.css'

Vue.use(VueMaterial)
Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    auth,
    transaction
  }
});
