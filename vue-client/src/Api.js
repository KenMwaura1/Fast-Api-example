import axios from 'axios'

export default() => {
    return axios.get('http://localhost:8002/notes/7/')
    //return fetch('http://localhost:8002/notes/5')
}