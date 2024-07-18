<template>
  <div>
    <div class="d-flex justify-content-between align-items-center">
      <h3 style="margin-top: 50px" class="headingText">All Accounts</h3>
      <div class="d-flex justify-content-start">
        <button
          class="create_account"
          type="button"
          data-toggle="modal"
          data-target="#exampleModalCenter"
          @click="showCreateModel"
        >
          Create Account
        </button>
        <button
          type="button"
          class="btn btn-success"
          data-toggle="modal"
          data-target="#exampleModalCenter"
          @click="hideCreateModel"
        >
          Add Category
        </button>
      </div>
    </div>

    <div class="account-container">
      <div
        class="card"
        style="width: 18rem; margin-top: 30px; margin-right: 20px"
        v-for="account in this.$store.state.transaction.getAllAccount"
        :key="account.id"
      >
        <div class="card-body">
          <div class="account-heading">
            <h5 class="card-title">{{ account.name }}</h5>
            <h6 class="card-subtitle mb-2 text-muted">{{ account.type }}</h6>
          </div>

          <h3 style="text-align: center">
            {{ account.starting_balance }}
            <span class="balance">Starting Balance </span>
          </h3>
          <h3 style="text-align: center">
            {{ account.latest_balance }}
            <span class="balance">Latest Balance </span>
          </h3>
        </div>
      </div>
    </div>

    <div class="button_container">
      <div class="d-flex justify-content-between align-items-center w-100">
        <h3 class="headingText">All Transactions</h3>
        <TransactionModel />
      </div>

      <!-- Modals below  -->

      <Modal v-show="isModalVisible" @close="closeModal" />
      <div
        class="modal fade"
        id="exampleModalCenter"
        tabindex="-1"
        role="dialog"
        aria-labelledby="exampleModalCenterTitle"
        aria-hidden="true"
      >
        <div class="modal-dialog modal-dialog-centered" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="exampleModalLongTitle">
                {{
                  isCreateModel
                    ? 'Create Account'
                    : isTransactionModel
                    ? 'Create Transaction'
                    : 'Add Category'
                }}
              </h5>
              <button
                type="button"
                class="close"
                data-dismiss="modal"
                aria-label="Close"
              
              >
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div class="modal-body">
              <div class="form-group" v-if="!isCreateModel">
                <input
                  type="text"
                  class="form-control"
                  id="inputAddress2"
                  placeholder="Add Category"
                  v-model="category"
                />
              </div>
              <div v-else-if="isCreateModel">
                <div class="form-row">
                  <div class="form-group col-md-6">
                    <label for="inputEmail4">Name</label>
                    <input
                      type="text"
                      v-model="createData.name"
                      class="form-control"
                      id="inputEmail4"
                      placeholder="Name"
                    />
                  </div>
                  <div class="form-group col-md-6">
                    <label for="inputState">Account</label>
                    <select
                      id="inputState"
                      v-model="createData.type"
                      class="form-control"
                    >
                      <option selected>Choose...</option>
                      <option v-for="acc in allAccount" :key="acc">{{ acc }}</option>
                    </select>
                  </div>
                </div>

                <div class="form-group">
                  <label for="inputAddress2">Starting Balance</label>
                  <input
                    type="number"
                    v-model="createData.starting_balance"
                    class="form-control"
                    id="inputAddress2"
                    placeholder="Starting Balance"
                  />
                </div>
                <div class="form-group">
                  <label for="inputAddress2">Latest Balance</label>
                  <input
                    type="number"
                    v-model="createData.latest_balance"
                    class="form-control"
                    id="inputAddress2"
                    placeholder="Starting Balance"
                  />
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button
                type="submit"
                class="btn-green"
                v-if="isCreateModel"
                @click="handleCreateUser"
              >
                Create
              </button>
              <button
                type="button"
                class="btn btn-primary"
                v-else-if="!isCreateModel"
                @click="handleCreateCaegory"
              >
                Add Category
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <table
      class="table alltransactioncontainer"
      v-if="this.$store.state.transaction.getAll"
    >
      <thead>
        <tr>
          <th scope="col">Date</th>
          <th scope="col">Account</th>
          <th scope="col">Category</th>
          <th scope="col">Amount</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="transaction in this.$store.state.transaction.getAll
            .transactions"
          :key="transaction.id"
        >
          <th scope="row">{{ transaction.date }}</th>
          <td>{{ transaction.account }}</td>
          <td>{{ transaction.category }}</td>
          <td>{{ transaction.amount }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import Modal from '../component/Modal.vue';
import TransactionModel from '../component/TransactionModel.vue';
import TransactionService from '../services/transcation/transaction.service';

export default {
  name: 'Profile',

  components: {
    Modal,
    TransactionModel,
  },
  data() {
    return {
      isModalVisible: false,
      isCreateModel: false,
      category:"",
      allAccount:[],
      createData: {
        name: '',
        type: '',
        starting_balance: 0,
        latest_balance: 0,
      },
    };
  },
  created() {
    this.$store.dispatch('transaction/getAllTransaction', {
      category: 'ALL',
      transaction_type: 'ALL',
      from_date: '',
      to_date: '',
      account: 'ALL',
    });
    this.$store.dispatch('transaction/getAllAccount');
    TransactionService.getAllAccountDropdown().then(
      (res) => (this.allAccount = res.data)
    );
  },
  methods: {
    showCreateModel() {
      this.isCreateModel = true;
    },
    hideCreateModel() {
      this.isCreateModel = false;
    },

    showModal() {
      this.isModalVisible = true;
    },
    closeModal() {
      this.isModalVisible = false;
      this.isTransactionModel = false;
    },
    handleCreateUser() {
      this.$store.dispatch('transaction/addAccount', this.createData);
      this.closeModal();
    },
    handleCreateCaegory(){
      this.$store.dispatch('transaction/addCategory', this.category);
      this.closeModal();
    }
  },
  computed: {
    currentUser() {
      return this.$store.state.auth.user;
    },
  },
  mounted() {
    if (!this.currentUser) {
      this.$router.push('/login');
    }
  },
};
</script>

<style scoped>
.alltransactioncontainer {
  margin-top: 50px;
}
.headingText{
  font-weight: 400;
  color: rgba(0,0,0,0.8);
  font-size: 20px;
}
.account-container {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  width: 100%;
}
.balance {
  font-size: 8px;
  font-weight: 400;
  color: green;
}
.card {
  border-radius: 20px;
}
.account-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 30px;
}
.button_container {
  display: flex;
  align-items: center;
  margin-top: 40px;
  justify-content: space-between;
}
.create_account {
  background-color: black;
  color: white;
  box-shadow: 1px 1px 1px gray;
  border-radius: 5px;
  padding: 5px 10px;
  width: 200px;
}
.btn-green {
  color: white;
  background: black;
  border-radius: 5px;
  width: 100%;
  padding: 4px 0;
}
</style>
