import {useState} from "react"
import api from "../services/api"
function Login(){
    const[password,setPassword]=useState("")
    const[email,setEmail]=useState("")
    const handleSubmit=async (e) => {
        e.preventDefault()
        try{
            const response=await api.post("/login",
                {
                    email,password
                }
            )
            localStorage.setItem(
                "token",
                response.data.access_token
            )
            console.log("Token stored")
        }catch(error){
            console.log(error)
        }
        
    }

    return (
        <div>
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <input type="email" placeholder="Email" value={email} onChange={(e)=>{
                        setEmail(e.target.value)
                    }}/>
                    
                </div>
                <div>
                    <input type="password" placeholder="Password" value={password} onChange={(e)=>{
                        setPassword(e.target.value)
                    }}/>
                    
                </div>
                <button type="submit">
                        Login
                </button>

            </form>
        </div>
    )
}
export default Login