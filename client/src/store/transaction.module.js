import { error } from "jquery";
import TransactionService from "../services/transcation/transaction.service";


const initialState ={
    failure:false,
    getAll:null,
    getAllAccount:null,
}

export const transaction = {
  namespaced: true,
  state: initialState,
  actions: {
    getAllTransaction({ commit }, user) {
      return TransactionService.getAll(user).then(
        user => {
          commit('getAllSuccess', user);
          return Promise.resolve(user);
        },
        error => {
          commit('getAllFailure');
          return Promise.reject(error);
        }
      );
    },
    getAllAccount({ commit }) {
      return TransactionService.getAllAccount().then(
        data => {
          commit('getAllAccountSuccess', data);
          return Promise.resolve(data);
        },
        error => {
          commit('getAllAccountFailure');
          return Promise.reject(error);
        }
      );
    },
    addAccount({commit},user){
      return TransactionService.createAccount(user).then(
        user => {
          commit('createAccountSuccess', user);
          return Promise.resolve(user);
        },
        error => {
          commit('createAccountFailure');
          return Promise.reject(error);
        }
      )
    },
    addCategory({commit},category){
      return TransactionService.addCategoryService(category).then(
        data =>{
          commit("addCategorySuccess",data);
          return Promise.resolve(data)
        },
        error=>{
          commit("addCategoryFailure");
          return Promise.reject(error)
        }
      )
    }
  },
  mutations: {
    getAllSuccess(state, user) {
      state.failure = false;
      state.getAll = user;
    },
    getAllFailure(state) {
      state.failure = true;
      state.getAll = null;
    },
    getAllAccountSuccess(state,data){
        state.getAllAccount= data
    },
    getAllAccountFailure(state){
      state.getAllAccount= null
    },
    createAccountSuccess(state) {
      state.failure = false;
    },
    createAccountFailure(state) {
      state.failure = true;
    },
    addCategorySuccess(state){
      state.failure=false;
    },
    addCategoryFailure(state){
      state.failure=true
    }
  }
};
