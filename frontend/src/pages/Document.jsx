import { useEffect, useState } from "react"
import api from "../services/api"
function Documents(){
    const fetchDocuments=async()=>{
        const token = localStorage.getItem("token")
        try{
            const response =await api.get("/documents",
                {
                    headers:{
                        Authorization:`Bearer ${token}`
                    }
            }
        )
        console.log(response.data)
        setDocuments(response.data)

        }
        catch(err){
            console.log(err)
        }
    }
    const [documents, setDocuments] = useState([])
    useEffect(() => {
        fetchDocuments()
    }, [])
    return (
        <div>
            <h2>My Documents</h2>
        </div>
    )
}
export default Documents