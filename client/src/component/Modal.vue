<template>
  <div class="modal-backdrop">
    <div class="modal-account">
      <header class="modal-header">
        <button
          type="button"
          class="btn-close"
          @click="close"
        >
          x
        </button>
      </header>

      <section class="modal-body">
        <form>
          <div class="form-row">
            <div class="form-group col-md-6">
              <label for="inputEmail4">Name</label>
              <input
                type="text"
                class="form-control"
                id="inputEmail4"
                placeholder="Name"
              />
            </div>
            <div class="form-group col-md-6">
              <label for="inputState">Type</label>
              <select id="inputState" class="form-control">
                <option selected>Choose...</option>
                <option>...</option>
              </select>
            </div>
          
            <!-- <div class="form-group col-md-6">
              <label for="inputPassword4">Type</label>
              <input
                type="text"
                class="form-control"
                id="inputPassword4"
                placeholder="Password"
              />
            </div> -->
          </div>
         
          <!-- <div class="form-group">
            <label for="inputAddress">Type</label>
            <input
              type="text"
              class="form-control"
              id="inputAddress"
              placeholder="Type"
            />
          </div> -->
          <div class="form-group">
            <label for="inputAddress2">Starting Balance</label>
            <input
              type="text"
              class="form-control"
              id="inputAddress2"
              placeholder="Starting Balance"
            />
          </div>
          <div class="form-group">
            <label for="inputAddress2">Latest Balance</label>
            <input
              type="text"
              class="form-control"
              id="inputAddress2"
              placeholder="Starting Balance"
            />
          </div>
          <!-- <div class="form-row">
            <div class="form-group col-md-6">
              <label for="inputCity">City</label>
              <input type="text" class="form-control" id="inputCity" />
            </div>
           
            <div class="form-group col-md-2">
              <label for="inputZip">Zip</label>
              <input type="text" class="form-control" id="inputZip" />
            </div>
          </div> -->
          <div class="form-group">
           
          </div>
          <button type="submit" class="btn-green" @click="close">Create</button>
        </form>
      </section>

      <footer class="modal-footer">

      </footer>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Modal',
  methods: {
    close() {
      this.$emit('close');
    },
  },
};
</script>

<style>
.modal-backdrop {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: rgba(0, 0, 0, 0.3);
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

.modal-account {
  background: #ffffff;
  box-shadow: 2px 2px 20px 1px;
  overflow-x: auto;
  display: flex;
  flex-direction: column;
  width: fit-content;
  height: fit-content;
  margin-left: calc(100% - 70%);
  margin-top: calc(100% - 95%);
}

.modal-header,
.modal-footer {
  padding: 15px;
  display: flex;
}

.modal-header {
  position: relative;
  border-bottom: 1px solid #eeeeee;
  color: #4aae9b;
  justify-content: space-between;
}

.modal-footer {
  border-top: 1px solid #eeeeee;
  flex-direction: column;
  justify-content: flex-end;
}

.modal-body {
  position: relative;
  padding: 20px 10px;
}

.btn-close {
  position: absolute;
  top: 0;
  right: 0;
  border: none;
  font-size: 20px;
  padding: 10px;
  cursor: pointer;
  font-weight: bold;
  color: #4aae9b;
  background: transparent;
}

.btn-green {
  color: white;
  background: black;
  border-radius: 5px;
  width: 100%;
  padding: 4px 0;
}
</style>
