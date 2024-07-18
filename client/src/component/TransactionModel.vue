<template>
  <div>
    <button
      class="btn btn-dark"
      @click="showTransactionModel"
      data-toggle="modal"
      data-target="#exampleTransactionModalCenter"
    >
      Create Transaction
    </button>
    <div
      class="modal fade"
      id="exampleTransactionModalCenter"
      tabindex="-1"
      role="dialog"
      aria-labelledby="exampleModalCenterTitle"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLongTitle">
              Create Transaction
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
            <div>
              <div class="form-row">
                <div class="form-group col-md-6">
                  <label for="inputAmount">Amount</label>
                  <input
                    type="text"
                    v-model="formTransaction.amount"
                    class="form-control"
                    id="inputAmount"
                    placeholder="Amount"
                  />
                </div>
                <div class="form-group col-md-6">
                  <label for="inputType">Type</label>
                  <select
                    id="inputType"
                    v-model="formTransaction.transaction_type"
                    class="form-control"
                  >
                    <option selected>Choose...</option>
                    <option>Income</option>
                    <option>Expense</option>
                  </select>
                </div>
              </div>

              <div class="form-group">
                <label for="inputDate">Date</label>
                <input
                  type="date"
                  v-model="formTransaction.date"
                  class="form-control"
                  id="inputDate"
                  placeholder="Date"
                />
              </div>
              <div class="form-group">
                <label for="inputCategory">Category</label>
                <select
                  id="inputCategory"
                  v-model="formTransaction.category"
                  class="form-control"
                >
                  <option v-for="cat in allCategory" :key="cat">
                    {{ cat }}
                  </option>
                </select>
              </div>
              <div class="form-group">
                <label for="inputRemarks">Remarks</label>
                <input
                  type="text"
                  v-model="formTransaction.remarks"
                  class="form-control"
                  id="inputRemarks"
                  placeholder="Remarks"
                />
              </div>
              <div class="form-group">
                <label for="inputAccount">Account</label>
                <select
                  id="inputAccount"
                  v-model="formTransaction.account"
                  class="form-control"
                >
                  <option v-for="acc in allAccount" :key="acc">
                    {{ acc }}
                  </option>
                </select>
               
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="submit" class="btn-green" @click="handleCreateUser">
              Create
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import TransactionService from '../services/transcation/transaction.service';
export default {
  name: 'TransactionModel',
  data() {
    return {
      isTransactionModel: false,
      allCategory: [],
      allAccount:[],
      formTransaction: {
        amount: 0,
        date: '',
        transaction_type: '',
        category: '',
        remarks: '',
        account: '',
      },
    };
  },
  created() {
    TransactionService.getAllCategory().then(
      (res) => (this.allCategory = res.data)
    );
    TransactionService.getAllAccountDropdown().then(
      (res) => (this.allAccount = res.data)
    );
  },
  methods: {
    showTransactionModel() {
      this.isTransactionModel = true;
    },
    hideTransactionModel() {
      this.isTransactionModel = false;
    },
    handleCreateUser() {
      console.log(this.formTransaction);
    },
  },
};
</script>
