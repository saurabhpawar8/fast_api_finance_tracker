import axios from 'axios';
import authHeader from '../auth-header';

const API_URL = 'http://localhost:8000/';

class TransactionService {
  getAll(data) {
    return axios
      .post(API_URL + 'get_all_transaction', {
        category: data.category,
        transaction_type: data.transaction_type,
        from_date:data.from_date,
        to_date:data.to_date,
        account:data.account
      },{ headers: authHeader() })
      .then(response => {         
        return response.data;
      });
  }

  getAllAccount() {
    return axios
      .get(API_URL + 'get_all_accounts',{ headers: authHeader() })
      .then(response => {         
        return response.data;
      });
  }

  createAccount(data){
    return axios.post(API_URL+'account',{
      name:data.name,
      type:data.type,
      starting_balance:Number(data.starting_balance),
      latest_balance:Number(data.latest_balance)
    },{ headers: authHeader() })
  }

  addCategoryService(category){
    return axios.post(API_URL+'category',{
      name:category,
    },{ headers: authHeader() })
  }
  
  getAllCategory(){
    return axios.get(API_URL+'categories',{headers:authHeader()})
  }

  getAllAccountDropdown(){
    return axios.get(API_URL+'accounts_dropdown',{headers:authHeader()})
  }

 

}

export default new TransactionService();
