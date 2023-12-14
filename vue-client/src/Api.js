import axios from 'axios'

export default() => {
    return axios.get('http://localhost:8002/notes/')
    //return fetch('http://localhost:8002/notes/5')
}

