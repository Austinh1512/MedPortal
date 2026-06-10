import { Routes, Route } from "react-router-dom"
import Dashboard from "./pages/Dashboard"
import Login from "./pages/Login"
import Register from "./pages/Register"
import PatientExplorer from "./pages/PatientExplorer"
import PatientDetail from "./pages/PatientDetail"
import useAxiosInterceptors from "./hooks/useAxiosInterceptors"

function App() {
  useAxiosInterceptors();

  return (
    <Routes>
     <Route index element={<Dashboard />} />
     <Route path="login" element={<Login />} />
     <Route path="register" element={<Register />} />
     <Route path="patients" element={<PatientExplorer />} />
     <Route path="patients/:id" element={<PatientDetail />} />
    </Routes>
  )
}

export default App
